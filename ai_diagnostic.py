import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
import time

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")

print(f"Key Found: {bool(key)}")
key_str = str(key or "")
if key: print(f"Key Prefix: {key_str[:10]}...") # type: ignore

genai.configure(api_key=key)

models = ['gemini-1.5-flash', 'gemini-flash-latest', 'gemini-2.0-flash-lite', 'gemini-1.5-pro']

for m_name in models:
    print(f"\nTesting {m_name}...")
    try:
        model = genai.GenerativeModel(m_name)
        start = time.time()
        response = model.generate_content("Hello", request_options={"timeout": 10})
        print(f"  SUCCESS in {time.time()-start:.2f}s: {response.text.strip()}")
    except Exception as e:
        print(f"  FAILURE: {str(e)}")
