# crop_project/soil/recommendations.py

SOIL_DATA = {
    "Sandy": {
        "characteristics": [
            "Excellent drainage, dries out quickly",
            "Warms up fast in spring",
            "Low in essential nutrients (needs frequent fertilizing)"
        ],
        "crops": ["Carrot", "Potato", "Groundnut", "Radish", "Cucumber"],
        "ideal_weather": {
            "temperature": "20°C - 30°C (Warm/Moderate)",
            "humidity": "40% - 60% (Low to Moderate)",
            "rainfall": "Requires frequent, light showers or constant irrigation."
        },
        "tips": "Add organic matter like compost to improve water retention. Irrigate lightly but frequently."
    },
    "Clay": {
        "characteristics": [
            "High water retention (heavy and sticky when wet)",
            "Nutrient-rich, holds minerals well",
            "Slow to warm up in spring, poor drainage"
        ],
        "crops": ["Rice", "Broccoli", "Cabbage", "Peas", "Aster"],
        "ideal_weather": {
            "temperature": "15°C - 25°C (Cool/Moderate)",
            "humidity": "60% - 80% (Moderate to High)",
            "rainfall": "Requires consistent but well-spaced rainfall. Too much causes waterlogging."
        },
        "tips": "Avoid working the soil when it's wet to prevent compaction. Add gypsum to improve structure."
    },
    "Loamy": {
        "characteristics": [
            "Ideal agricultural soil (perfect mix of sand, silt, and clay)",
            "Great moisture retention and drainage",
            "High fertility and organic matter"
        ],
        "crops": ["Wheat", "Sugarcane", "Cotton", "Tomato", "Most vegetables"],
        "ideal_weather": {
            "temperature": "18°C - 32°C (Highly Versatile)",
            "humidity": "50% - 75% (Adaptable)",
            "rainfall": "Thrives in balanced weather, withstands both dry spells and heavy rain well."
        },
        "tips": "Maintain fertility by rotating crops and adding light compost annually."
    },
    "Silty": {
        "characteristics": [
            "Smooth, slippery texture",
            "Moisture retentive and typically very fertile",
            "Prone to compaction and crusting"
        ],
        "crops": ["Lettuce", "Onion", "Turmeric", "Ginger", "Cabbage"],
        "ideal_weather": {
            "temperature": "18°C - 28°C (Moderate/Cool)",
            "humidity": "50% - 70% (Moderate)",
            "rainfall": "Requires steady rain. Heavy downpours can easily wash this soil away."
        },
        "tips": "Avoid walking on wet silty soil. Incorporate organic matter to prevent crusting on the surface."
    },
    "Peaty": {
        "characteristics": [
            "High in organic matter and moisture",
            "Often acidic nature",
            "Dark color, warms up slowly"
        ],
        "crops": ["Root crops", "Legumes", "Spinach", "Brassicas"],
        "ideal_weather": {
            "temperature": "12°C - 22°C (Cool/Cold)",
            "humidity": "70% - 90% (High Wetness)",
            "rainfall": "Naturally wet environments. Requires significant drainage during heavy monsoons."
        },
        "tips": "You may need to add lime to reduce acidity. Excellent for crops once drained properly."
    },
    "Chalky": {
        "characteristics": [
            "Highly alkaline (high pH)",
            "Often stony, drains rapidly",
            "Can lead to stunted growth due to iron/manganese lockup"
        ],
        "crops": ["Spinach", "Sweet Corn", "Beetroot", "Cabbage", "Lilac"],
        "ideal_weather": {
            "temperature": "15°C - 28°C (Moderate/Warm)",
            "humidity": "40% - 65% (Low to Moderate)",
            "rainfall": "Needs frequent watering. Heavy rains immediately drain away, leaving crops thirsty."
        },
        "tips": "Use acidifying fertilizers. Regularly add bulky organic matter to improve structure and moisture retention."
    }
}
