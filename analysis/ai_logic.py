import os
import google.generativeai as genai  # type: ignore

def get_agronomist_strategy(soil_type, temp, humidity):
    """
    Generates a 3-sentence farming strategy based on environmental parameters.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Configure GEMINI_API_KEY to receive advanced AI agronomist insights."

    try:
        genai.configure(api_key=api_key)
        
        # Try multiple model names for robustness (order matters: latest -> stable -> legacy)
        model_names = [
            "gemini-1.5-flash", 
            "gemini-1.5-flash-latest", 
            "gemini-1.5-pro", 
            "gemini-1.5-flash-8b", 
            "gemini-pro"
        ]
        model = None
        
        prompt = f"""You are a professional agronomist. Given:
        Soil: {soil_type}
        Temperature: {temp}°C
        Humidity: {humidity}%
        
        Provide a 3-sentence expert farming strategy for this specific condition. 
        Focus on irrigation and soil management. Be concise and professional."""
        
        for name in model_names:
            try:
                full_name = f"models/{name}" if not name.startswith("models/") else name
                model = genai.GenerativeModel(full_name)
                response = model.generate_content(prompt)
                
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                # If a model fails due to 404/quota, retry with the next one
                continue

        # Fallback strategy if all AI models fail (Zero downtime UX)
        fallbacks = {
            "Sandy": f"Sandy soil drains rapidly, so frequent, light irrigation is essential in {temp}°C weather. Apply organic compost regularly to improve water retention and boost crop vitality. Monitor topsoil moisture closely during dry spells.",
            "Clay": f"Clay soil holds moisture well but risks waterlogging, especially if humidity levels reach {humidity}%. Ensure fields have proper drainage channels to protect roots. Deep plowing before planting will help aerate the structure.",
            "Loamy": f"Loamy soil provides an excellent balance; maintain its structure with minimal tillage. Standard irrigation schedules apply, but monitor topsoil dryness at {temp}°C. Use organic mulch to suppress weeds and lock in moisture.",
            "Silty": f"Silty soil is highly fertile but prone to compaction and crusting under heavy rain. Practice crop rotation and avoid walking on wet beds to preserve soil structure. A balanced irrigation system ensures roots remain adequately oxygenated.",
            "Peaty": f"Peaty soil is highly organic but can be naturally acidic; test pH levels regularly. Maintain consistent moisture without causing waterlogging. Consider adding lime to balance acidity for optimal vegetable growth.",
            "Chalky": f"Chalky soil is alkaline and stony, meaning water drains away very quickly. Use deep-rooted crops and apply significant organic matter to improve fertility. Regular, deep watering is necessary to prevent severe drought stress."
        }
        
        return fallbacks.get(soil_type, f"Maintain standard irrigation for {temp}°C weather. Ensure proper drainage and monitor soil moisture levels as a baseline strategy. Apply balanced fertilizers according to crop-specific needs.")
        
    except Exception:
        pass
        
    # Final safety fallback
    return f"Maintain standard irrigation for {temp}°C weather. Ensure proper drainage and monitor soil moisture levels as a baseline strategy."
