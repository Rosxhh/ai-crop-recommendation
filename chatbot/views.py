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
    import google.generativeai as genai
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

def chatbot_page(request):
    return render(request, "chatbot.html")

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
            db_history = list(ChatMessage.objects.filter(session_id=session_id).order_by('-timestamp')[:5])
            db_history.reverse()
            gemini_history = []
            for m in db_history[:-1]:
                h_text = m.text if m.text != "[Image Content]" else "User shared an image."
                gemini_history.append({"role": "model" if m.role == "assistant" else "user", "parts": [h_text]})

            # DYNAMIC FALLBACK CHAIN (Prioritize Vision models if image exists)
            has_image = img_data is not None
            if has_image:
                model_names = ['gemini-1.5-flash-8b', 'gemini-flash-lite-latest', 'gemini-1.5-flash', 'gemma-3-4b-it']
            else:
                model_names = ['gemma-3-4b-it', 'gemini-1.5-flash-8b', 'gemini-flash-lite-latest']
            
            system_instruction = f"""You are 'AgriCore AI Master', the ultimate agriculture expert.
            Provide expert farming advice in {lang}. 
            Identify crops/issues in images. Suggest NPK, irrigation, and pest control. 
            STRICT RULES: bold text, farming emojis 🌾, Respond ONLY in {lang}."""
            
            reply = "I apologize, but my high-level knowledge systems are temporarily busy. Please try again in 10-20 seconds! 🚜"
            success = False
            
            for m_name in model_names:
                try:
                    model = genai.GenerativeModel(
                        model_name=m_name,
                        tools=[get_weather] if "gemma" not in m_name and "8b" not in m_name else None,
                        system_instruction=system_instruction if "gemma" not in m_name else None
                    )
                    
                    if "gemma" in m_name:
                        full_req = [system_instruction] + content_parts
                        response = model.generate_content(full_req, request_options={"timeout": 15})
                    else:
                        chat = model.start_chat(history=gemini_history, enable_automatic_function_calling=True)
                        response = chat.send_message(content_parts, request_options={"timeout": 15})
                    
                    if response and response.text:
                        reply = response.text
                        success = True
                        break
                except Exception as inner_e:
                    print(f"FALLBACK DEBUG: {m_name} failed: {inner_e}")
                    continue
            
            if not success:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(content_parts)
                    if response.text: reply = response.text
                except: pass

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
