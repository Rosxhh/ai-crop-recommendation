import os
    from ..ai import free_ai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv(r'c:\Users\acer\Desktop\CropYieldProject\crop_project\.env')
key = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=key)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"ERROR: {str(e)}")
