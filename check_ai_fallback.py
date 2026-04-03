import os
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=key)
    # Check 1.5 Flash
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("ONE word: 'OK'")
    print(f"1.5-FLASH RESULT: {response.text.strip()}")
except Exception as e:
    print(f"1.5-FLASH FAILURE: {str(e)}")
