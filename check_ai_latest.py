import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("ONE word: 'OK'")
    print(f"FLASH-LATEST RESULT: {response.text.strip()}")
except Exception as e:
    print(f"FLASH-LATEST FAILURE: {str(e)}")
