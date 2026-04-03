import os
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=key)  # type: ignore

print("Emergency Model Scan...")
models_to_test = [
    'gemini-1.5-flash-8b', 
    'gemini-flash-lite-latest',
    'gemini-2.5-flash-lite',
    'gemma-3-4b-it',
    'gemma-2-9b-it',
    'gemma-2-2b-it'
]

for name in models_to_test:
    try:
        model = genai.GenerativeModel(name)  # type: ignore
        response = model.generate_content("Hi", request_options={"timeout": 7})  # type: ignore
        print(f"WORKS: {name}")
    except Exception as e:
        error_msg = str(e)  # type: ignore
        print(f"FAILED ({name}): {error_msg[:50]}...")
