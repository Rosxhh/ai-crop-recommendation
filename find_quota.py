import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)

print("Checking ALL available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        name = m.name
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Hi", request_options={"timeout": 5})
            print(f"✅ WORKS: {name}")
            break
        except Exception as e:
            if "429" in str(e):
                print(f"❌ QUOTA: {name}")
            else:
                print(f"⚠️ ERROR ({name}): {(str(e) or '')[:50]}...") # type: ignore
