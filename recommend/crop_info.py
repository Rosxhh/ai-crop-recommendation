# Alphabetical mapping for the 22 crops in the standard recommendation dataset
CROP_MAPPING = {
    0: "apple",
    1: "banana",
    2: "blackgram",
    3: "chickpea",
    4: "coconut",
    5: "coffee",
    6: "cotton",
    7: "grapes",
    8: "jute",
    9: "kidneybeans",
    10: "lentil",
    11: "maize",
    12: "mango",
    13: "mothbeans",
    14: "mungbean",
    15: "muskmelon",
    16: "orange",
    17: "papaya",
    18: "pigeonpeas",
    19: "pomegranate",
    20: "rice",
    21: "watermelon"
}

# Metadata for each crop - Centralized Decision Intelligence
CROP_DETAILS = {
    "apple": {
        "icon": "fa-solid fa-apple-whole",
        "description": "Apples grow best in temperate climates with cold winters.",
        "tips": "Prune trees annually and ensure well-drained soil rich in organic matter.",
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [100, 60, 120], 
            "growth_days": 150, 
            "pests": ["Aphids", "Codling Moth"], 
            "weeds": ["Dandelion", "Thistle"], 
            "organic": "Neem oil spray and pheromone traps.",
            "planting": "January - February",
            "harvest": "August - September",
            "market_price": 8500, # per quintal
            "yield_per_ha": 25, # tons
            "costs": {"seeds": 45000, "labour": 60000, "irrigation": 12000, "other": 15000},
            "fertilizer_plan": "Apply balanced NPK in early spring. Supplement with Calcium for fruit firmness.",
            "irrigation_freq": "Weekly during fruit set",
            "sustainability": 85,
            "suitability_score": 92
        }
    },
    "banana": {
        "icon": "fa-solid fa-lemon",
        "description": "Bananas are high-yield tropical fruits that love humidity and heat.",
        "tips": "Provide plenty of water and heavy mulching. Protect from strong winds.",
        "image": "https://images.unsplash.com/photo-1571771894821-ad99621139c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [250, 100, 600], 
            "growth_days": 300, 
            "pests": ["Banana Weevil", "Aphids"], 
            "weeds": ["Bermuda Grass"], 
            "organic": "Regular weeding and biological control.",
            "market_price": 2500,
            "yield_per_ha": 40,
            "costs": {"seeds": 30000, "labour": 50000, "irrigation": 25000, "other": 10000},
            "fertilizer_plan": "Heavy Potassium required. Split N in 4 doses across growth cycle.",
            "irrigation_freq": "Every 2-3 days",
            "sustainability": 70,
            "suitability_score": 88
        }
    },
    "rice": {
        "icon": "fa-solid fa-water",
        "description": "Rice is a staple crop that grows best in standing water or flooded fields.",
        "tips": "Maintain a consistent water level and use nitrogen-rich fertilizers.",
        "image": "https://images.unsplash.com/photo-1586201321503-4556488bc110?auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [120, 60, 40], 
            "growth_days": 120, 
            "planting": "June - July", 
            "harvest": "October - November",
            "market_price": 2200,
            "yield_per_ha": 4.5,
            "costs": {"seeds": 5000, "labour": 15000, "irrigation": 8000, "other": 4000},
            "fertilizer_plan": "Apply N in 3 splits: 50% basal, 25% at tillering, 25% at panicle initiation.",
            "irrigation_freq": "Continuous standing water (3-5cm)",
            "sustainability": 60,
            "suitability_score": 95
        }
    },
    "maize": {
        "icon": "fa-solid fa-wheat-awn",
        "description": "Maize (Corn) is a versatile cereal that needs warm weather and nitrogen.",
        "tips": "Plant in blocks for better pollination. Control weeds for the first 4 weeks.",
        "image": "https://images.unsplash.com/photo-1601648764658-cf37e8c89b70?auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [120, 60, 40], 
            "growth_days": 100, 
            "planting": "June - July", 
            "harvest": "September - October",
            "market_price": 1900,
            "yield_per_ha": 5.0,
            "costs": {"seeds": 6000, "labour": 12000, "irrigation": 4000, "other": 3000},
            "fertilizer_plan": "Apply P+K at sowing; split N into 3 applications across the season.",
            "irrigation_freq": "Every 7-10 days",
            "sustainability": 75,
            "suitability_score": 90
        }
    },
    "wheat": {
        "icon": "fa-solid fa-wheat-awn",
        "description": "Wheat is a globally important cereal that thrives in temperate regions.",
        "tips": "Ensure the field is well-prepared and level. Monitor for rust diseases.",
        "image": "https://images.unsplash.com/photo-1501436513145-30f24e19fcc8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [100, 50, 40], 
            "growth_days": 130, 
            "planting": "October - November", 
            "harvest": "March - April",
            "market_price": 2275,
            "yield_per_ha": 4.0,
            "costs": {"seeds": 4000, "labour": 10000, "irrigation": 5000, "other": 2000},
            "fertilizer_plan": "Apply 50% N + full P+K as basal, remaining N at first irrigation.",
            "irrigation_freq": "4-6 times per cycle",
            "sustainability": 80,
            "suitability_score": 94
        }
    },
    "pomegranate": {
        "icon": "fa-solid fa-circle-nodes",
        "description": "A fruit that thrives in dry, semi-arid climates.",
        "tips": "Perform thinning to get larger fruits. Monitor for fruit borer pests.",
        "image": "https://images.unsplash.com/photo-1541344999736-83eca272f6fc?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [120, 60, 60], 
            "growth_days": 150,
            "market_price": 12000,
            "yield_per_ha": 15,
            "costs": {"seeds": 80000, "labour": 40000, "irrigation": 10000, "other": 10000},
            "fertilizer_plan": "Apply organic manure + NPK twice a year (Jan/June).",
            "irrigation_freq": "Drip irrigation (20L/day)",
            "sustainability": 90,
            "suitability_score": 85
        }
    },
    "mango": {
        "icon": "fa-solid fa-fruit-citrus",
        "description": "The king of fruits, mangoes thrive in tropical and subtropical heat.",
        "tips": "Avoid irrigation during the flowering period to improve fruit set.",
        "image": "https://images.unsplash.com/photo-1553279768-865429fa0078?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {
            "ideal_npk": [100, 50, 100], 
            "growth_days": 180,
            "market_price": 6000,
            "yield_per_ha": 12,
            "costs": {"seeds": 50000, "labour": 30000, "irrigation": 5000, "other": 5000},
            "fertilizer_plan": "Basal dose in Oct/Nov. NPK spray during fruit development.",
            "irrigation_freq": "Once in 15 days",
            "sustainability": 95,
            "suitability_score": 82
        }
    }
}

# Fallback defaults for missing data
DEFAULT_META = {
    "ideal_npk": [100, 50, 50],
    "growth_days": 120,
    "planting": "Seasonal",
    "harvest": "End of cycle",
    "market_price": 3000,
    "yield_per_ha": 3.0,
    "costs": {"seeds": 5000, "labour": 10000, "irrigation": 5000, "other": 3000},
    "fertilizer_plan": "Balanced NPK application based on soil test.",
    "irrigation_freq": "As per local weather",
    "sustainability": 75,
    "suitability_score": 80
}

def get_crop_data(class_idx_or_name):
    if isinstance(class_idx_or_name, int):
        name = CROP_MAPPING.get(class_idx_or_name, "Unknown").lower()
    else:
        name = class_idx_or_name.lower()
        
    details = CROP_DETAILS.get(name, {
        "icon": "fa-solid fa-question",
        "description": "No additional details available.",
        "tips": "Consult a local agricultural expert for guidance.",
        "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": DEFAULT_META
    })
    
    # Merge with defaults for missing keys in meta
    meta = DEFAULT_META.copy()
    meta.update(details.get("meta", {}))
    
    return {
        "name": name.capitalize(),
        "icon": details["icon"],
        "description": details["description"],
        "tips": details["tips"],
        "image": details.get("image", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"),
        "meta": meta
    }
