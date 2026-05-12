from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Max, OuterRef, Subquery
import os
import json
import base64
import io
import time
from PIL import Image
from dotenv import load_dotenv
import uuid
from .models import ChatMessage

# Initialize Environment
load_dotenv()
try:
    from ..ai import free_ai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def get_weather(location: str) -> str:
    """Agricultural weather tool."""
    import requests
    API_KEY = "946a968623cdfce53a6c3cc031c29580"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            d = response.json()
            return f"Weather in {location}: {d['weather'][0]['description']}, {d['main']['temp']}°C, Humidity: {d['main']['humidity']}%."
    except: pass
    return f"Weather information for {location} unavailable."

from recommend.models import CropRecommendation

def chatbot_page(request):
    context_id = request.GET.get('context_id')
    initial_message = ""
    if context_id:
        try:
            rec = CropRecommendation.objects.get(id=context_id)
            initial_message = f"Hello! I just received a soil recommendation report from AgriCore.\n\nHere are my details:\n- Crop Recommended: **{rec.predicted_crop}**\n- Nitrogen: {rec.nitrogen}\n- Phosphorus: {rec.phosphorus}\n- Potassium: {rec.potassium}\n- Soil pH: {rec.ph}\n- Temperature: {rec.temperature}°C\n- Humidity: {rec.humidity}%\n- Rainfall: {rec.rainfall}mm\n\nCan you analyze these details and give me some expert farming advice to get started?"
            
            # Force a fresh chat session for this new context
            request.session['chat_session_id'] = str(uuid.uuid4())
        except Exception as e:
            print(f"Error loading context: {e}")
            pass
            
    return render(request, "chatbot.html", {"initial_message": initial_message})

@csrf_exempt
def chatbot_api(request):
    # 1. New Chat / Reset
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            # Start New Chat
            if body.get("new_chat"):
                request.session['chat_session_id'] = str(uuid.uuid4())
                return JsonResponse({"status": "new_chat_started", "session_id": request.session['chat_session_id']})
            
            # DELETE CHAT
            if body.get("delete_chat"):
                sid = body.get("session_id")
                if sid:
                    ChatMessage.objects.filter(session_id=sid).delete()
                    # If deleted the current session, reset it
                    if request.session.get('chat_session_id') == sid:
                        request.session['chat_session_id'] = str(uuid.uuid4())
                    return JsonResponse({"status": "deleted", "session_id": request.session['chat_session_id']})
        except: pass

    # 2. List Conversations for Sidebar
    if request.method == "GET" and request.GET.get("list_chats"):
        first_messages = ChatMessage.objects.filter(role='user').values('session_id').annotate(
            first_text=Subquery(
                ChatMessage.objects.filter(session_id=OuterRef('session_id'), role='user').order_by('timestamp').values('text')[:1]
            ),
            last_timestamp=Max('timestamp')
        ).order_by('-last_timestamp')
        
        history_list = []
        for chat in first_messages:
            text = chat['first_text'] or "New Conversation"
            history_list.append({
                "session_id": chat['session_id'],
                "title": text[:40] + ("..." if len(text) > 40 else ""),
                "timestamp": chat['last_timestamp'].strftime("%Y-%m-%d %H:%M")
            })
        return JsonResponse({"chats": history_list})

    # 3. Handle Chat logic
    if 'chat_session_id' not in request.session:
        request.session['chat_session_id'] = str(uuid.uuid4())
    
    session_id = request.GET.get("session_id") or request.session.get('chat_session_id')
    if request.GET.get("session_id"):
        request.session['chat_session_id'] = session_id

    lang = "English"
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            msg = data.get("message", "").strip()
            img_data = data.get("image", None)
            lang = data.get("language", "English")
            
            # Save User Message with Image Data
            stored_text = msg or "[Image Content]"
            ChatMessage.objects.create(session_id=session_id, role='user', text=stored_text, image_data=img_data)
            
            # Prepare Multimodal Parts
            content_parts = []
            if msg: content_parts.append(msg)
            if img_data:
                try:
                    if 'base64,' in img_data: _, b64 = img_data.split('base64,')
                    else: b64 = img_data
                    img_bytes = base64.b64decode(b64)
                    img = Image.open(io.BytesIO(img_bytes))
                    content_parts.append(img)
                except: pass
            
            if not content_parts:
                return JsonResponse({"reply": "I'm ready! Please type a message or paste an image. 🚜"})

            token = os.getenv("GEMINI_API_KEY")
            if not token or not GEMINI_AVAILABLE:
                return JsonResponse({"reply": "AI Knowledge base needs configuration. ⚠️"})

            genai.configure(api_key=token)
            
            # CONTEXT & HISTORY
            db_history = list(ChatMessage.objects.filter(session_id=session_id).order_by('-timestamp')[:10])
            db_history.reverse()
            gemini_history = []
            for m in db_history[:-1]:
                h_text = m.text if m.text != "[Image Content]" else "User shared an image."
                gemini_history.append({"role": "model" if m.role == "assistant" else "user", "parts": [h_text]})

            # MODERN MODELS & SAFETY
            model_names = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash']
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            system_instruction = f"""You are 'AgriCore Master', a helpful and expert agricultural assistant.
            Provide detailed farming advice in {lang}. 
            Identify crops, soil issues, and diseases from images.
            Suggest NPK ratios, irrigation, and pest control.
            Use bold text and farming emojis 🌾🚜. Respond in {lang}."""
            
            success = False
            reply = ""
            
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(
                        model_name=m_name,
                        system_instruction=system_instruction,
                        safety_settings=safety_settings
                    )
                    chat = model.start_chat(history=gemini_history)
                    response = chat.send_message(content_parts, request_options={"timeout": 30})
                    
                    if response and response.text:
                        reply = response.text
                        success = True
                        break
                except Exception as e:
                    print(f"Model {m_name} failed: {e}")
                    continue

            if not success:
                # Final Emergency Fallback
                try:
                    model = genai.GenerativeModel('gemini-flash-latest')
                    response = model.generate_content([system_instruction] + content_parts)
                    reply = response.text
                except Exception as e_final:
                    print(f"CRITICAL: All models failed: {e_final}")
                    reply = "I am currently online and ready to help! Please ask your farming questions. 🌾"

            ChatMessage.objects.create(session_id=session_id, role='assistant', text=reply)
            return JsonResponse({"reply": reply})
            
        else:
            db_history = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
            return JsonResponse({
                "history": [{"role": m.role, "content": m.text, "image_data": m.image_data} for m in db_history],
                "session_id": session_id
            })
            
    except Exception as e:
        print(f"AgriCore CRITICAL ERROR: {e}")
        return JsonResponse({"reply": "Something went wrong. Please refresh and try again. 🚜"})
