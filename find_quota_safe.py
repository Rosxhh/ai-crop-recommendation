import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)

print("Checking ALL available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        name = m.name
        try:
            model = genai.GenerativeModel(name)
            # Short test
            response = model.generate_content("Hi", request_options={"timeout": 5})
            print(f"SUCCESS: {name}")
            # If we find one that works, stop
            break
        except Exception as e:
            msg = str(e)
            if "429" in msg:
                print(f"QUOTA EXCEEDED: {name}")
            else:
                print(f"ERROR ({name}): {msg[:50]}...")
