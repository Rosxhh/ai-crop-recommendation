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

# Metadata for each crop
CROP_DETAILS = {
    "apple": {
        "icon": "fa-solid fa-apple-whole",
        "description": "Apples grow best in temperate climates with cold winters.",
        "tips": "Prune trees annually and ensure well-drained soil rich in organic matter.",
        "image": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 60, 120], "growth_days": 150, "pests": ["Aphids", "Codling Moth"], "weeds": ["Dandelion", "Thistle"], "organic": "Neem oil spray and pheromone traps."}
    },
    "banana": {
        "icon": "fa-solid fa-lemon", # FA doesn't have a good banana icon in free, lemon/leaf fallback
        "description": "Bananas are high-yield tropical fruits that love humidity and heat.",
        "tips": "Provide plenty of water and heavy mulching. Protect from strong winds.",
        "image": "https://images.unsplash.com/photo-1571771894821-ad99621139c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [250, 100, 600], "growth_days": 300, "pests": ["Banana Weevil", "Aphids"], "weeds": ["Bermuda Grass"], "organic": "Regular weeding and biological control with predatory beetles."}
    },

    "blackgram": {
        "icon": "fa-solid fa-seedling",
        "description": "A nutritious pulse crop that restores nitrogen to the soil.",
        "tips": "Requires moderate rainfall. Avoid waterlogging at all stages.",
        "image": "https://images.unsplash.com/photo-1599596001004-972172778007?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [40, 60, 40], "growth_days": 80, "pests": ["Pod Borer", "Whitefly"], "weeds": ["Parthenium"], "organic": "Intercropping with maize and using light traps."}
    },
    "chickpea": {
        "icon": "fa-solid fa-bowl-food",
        "description": "A drought-tolerant legume that grows well in cool, dry conditions.",
        "tips": "Plant in well-drained soil. Avoid excess nitrogen fertilizer as it's a legume.",
        "image": "https://images.unsplash.com/photo-1515544867663-70aa109d949c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [30, 60, 40], "growth_days": 100, "pests": ["Gram Pod Borer", "Cutworm"], "weeds": ["Chenopodium"], "organic": "Pheromone traps and early sowing."}
    },
    "coconut": {
        "icon": "fa-solid fa-tree",
        "description": "Coconuts thrive in coastal tropical regions with loamy or sandy soil.",
        "tips": "Keep the basin moist and apply organic manure regularly.",
        "image": "https://images.unsplash.com/photo-1522858100529-61f4fa0f12ad?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 150], "growth_days": 365}
    },
    "coffee": {
        "icon": "fa-solid fa-mug-hot",
        "description": "Coffee requires high altitudes, cool temperatures, and consistent rainfall.",
        "tips": "Provide shade trees and maintain slightly acidic soil pH.",
        "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [150, 80, 120], "growth_days": 300}
    },
    "cotton": {
        "icon": "fa-solid fa-cloud",
        "description": "A cash crop that needs warm temperatures and moderate rainfall.",
        "tips": "Ensure full sunlight and keep the field weed-free during early growth.",
        "image": "https://images.unsplash.com/photo-1593105541509-e8201ea8381f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 60], "growth_days": 160, "pests": ["Bollworm", "Jassids"], "weeds": ["Nut Grass"], "organic": "Release of Trichogramma parasites and neem seed kernel extract."}
    },
    "grapes": {
        "icon": "fa-solid fa-grapes",
        "description": "Grapes grow on vines and require warm, dry summers for sweet fruit.",
        "tips": "Implement a trellis system and prune heavily in winter.",
        "image": "https://images.unsplash.com/photo-1533435328003-903dfc6a3809?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [60, 40, 120], "growth_days": 150}
    },
    "jute": {
        "icon": "fa-solid fa-lines-leaning",
        "description": "A fiber crop that grows in hot, humid climates with heavy rainfall.",
        "tips": "Best grown in alluvial soil. Requires significant water for retting.",
        "image": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=1000&q=80",  # ✅ Verified Jute image
        "meta": {"ideal_npk": [80, 40, 40], "growth_days": 120, "pests": ["Jute Semilooper", "Yellow Mite"], "weeds": ["Sedge"], "organic": "Manual weeding and spray of garlic-chili extract."}
    },
    "kidneybeans": {
        "icon": "fa-solid fa-beans",
        "description": "A protein-rich pulse that likes cool to moderate temperatures.",
        "tips": "Maintain consistent moisture but avoid soaking the leaves to prevent rot.",
        "image": "https://images.unsplash.com/photo-1551462147-37885acc3c41?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [40, 60, 40], "growth_days": 90}
    },
    "lentil": {
        "icon": "fa-solid fa-droplet",
        "description": "A hardy pulse crop that can survive in relatively low moisture.",
        "tips": "Sow in early winter. Harvest when pods turn golden brown.",
        "image": "https://images.unsplash.com/photo-1547592166-239dece26e82?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [30, 50, 30], "growth_days": 110}
    },
    "maize": {
        "icon": "fa-solid fa-wheat-awn",
        "description": "Maize (Corn) is a versatile cereal that needs warm weather and nitrogen.",
        "tips": "Plant in blocks for better pollination. Control weeds for the first 4 weeks.",
        "image": "https://images.unsplash.com/photo-1601648764658-cf37e8c89b70?auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 40], "growth_days": 100, "pests": ["Stem Borer", "Fall Armyworm"], "weeds": ["Cyperus"], "organic": "Deep summer plowing and bird perches."}
    },
    "mango": {
        "icon": "fa-solid fa-fruit-citrus",
        "description": "The king of fruits, mangoes thrive in tropical and subtropical heat.",
        "tips": "Avoid irrigation during the flowering period to improve fruit set.",
        "image": "https://images.unsplash.com/photo-1553279768-865429fa0078?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 100], "growth_days": 180}
    },

    "mothbeans": {
        "icon": "fa-solid fa-seedling",
        "description": "An extremely drought-resistant pulse crop for arid regions.",
        "tips": "Grows well even in sandy soil with minimal water.",
        "image": "https://images.unsplash.com/photo-1592911225530-01d71da7008e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [20, 40, 20], "growth_days": 75}
    },
    "mungbean": {
        "icon": "fa-solid fa-seedling",
        "description": "A fast-growing pulse crop that serves as excellent green manure.",
        "tips": "Short duration crop. Suitable for intercropping with longer-season crops.",
        "image": "https://images.unsplash.com/photo-1599596001004-972172778007?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [20, 45, 20], "growth_days": 65}
    },
    "muskmelon": {
        "icon": "fa-solid fa-circle",
        "description": "Melons love heat and well-drained sandy loams.",
        "tips": "Use mulching to keep fruits off the ground and maintain moisture.",
        "image": "https://images.unsplash.com/photo-1590005176489-db2ee0d41f70?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 100], "growth_days": 90}
    },
    "orange": {
        "icon": "fa-solid fa-sun",
        "description": "Citrus fruits like oranges need plenty of sunlight and well-aerated soil.",
        "tips": "Prune dead wood and provide consistent water during fruit development.",
        "image": "https://images.unsplash.com/photo-1582967788606-a171c1080cb0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 100], "growth_days": 240}
    },
    "papaya": {
        "icon": "fa-solid fa-circle-dot",
        "description": "A fast-growing tropical fruit that needs excellent drainage.",
        "tips": "Avoid waterlogging as it causes root rot. Apply organic potassium.",
        "image": "https://images.unsplash.com/photo-1517282001574-fbf00ad3a9a0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [150, 150, 200], "growth_days": 270}
    },
    "pigeonpeas": {
        "icon": "fa-solid fa-seedling",
        "description": "A deep-rooted legume that improves soil structure and fertility.",
        "tips": "Requires very little water. Good for field bunding.",
        "image": "https://images.unsplash.com/photo-1599596001004-972172778007?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [25, 50, 25], "growth_days": 180}
    },
    "pomegranate": {
        "icon": "fa-solid fa-circle-nodes",
        "description": "A fruit that thrives in dry, semi-arid climates.",
        "tips": "Perform thinning to get larger fruits. Monitor for fruit borer pests.",
        "image": "https://images.unsplash.com/photo-1541344999736-83eca272f6fc?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 60], "growth_days": 150}
    },
    "rice": {
        "icon": "fa-solid fa-water",
        "description": "Rice is a staple crop that grows best in standing water or flooded fields.",
        "tips": "Maintain a consistent water level and use nitrogen-rich fertilizers.",
        "image": "https://images.unsplash.com/photo-1586201321503-4556488bc110?auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 40], "growth_days": 120, "pests": ["Stem Borer", "Brown Plant Hopper"], "weeds": ["Barnyard Grass"], "organic": "Maintain standing water and use Azolla."}
    },
    "watermelon": {
        "icon": "fa-solid fa-van-shuttle", # Fallback or circle
        "description": "Watermelons grow on the ground and need hot days and sandy soil.",
        "tips": "Give plenty of space for vines to spread. Stop watering a week before harvest for higher sugar.",
        "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 100], "growth_days": 95}
    },

    "carrot": {
        "icon": "fa-solid fa-carrot",
        "description": "Carrots need deep, loose soil to grow long and straight.",
        "tips": "Thin out seedlings early. Avoid excess nitrogen which causes hairy roots.",
        "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [60, 60, 100], "growth_days": 80}
    },
    "potato": {
        "icon": "fa-solid fa-circle",
        "description": "Potatoes are versatile tubers that grow well in loose, acidic soil.",
        "tips": "Hill the soil around plants as they grow to prevent green tubers.",
        "image": "https://images.pexels.com/photos/144248/potatoes-vegetables-erdfrucht-bio-144248.jpeg?auto=compress&cs=tinysrgb&w=800",
        "meta": {"ideal_npk": [120, 120, 200], "growth_days": 110}
    },
    "wheat": {
        "icon": "fa-solid fa-wheat-awn",
        "description": "Wheat is a globally important cereal that thrives in temperate regions.",
        "tips": "Ensure the field is well-prepared and level. Monitor for rust diseases.",
        "image": "https://images.unsplash.com/photo-1501436513145-30f24e19fcc8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 40], "growth_days": 130}
    },
    "tomato": {
        "icon": "fa-solid fa-apple-whole",
        "description": "Tomatoes love sun and consistent moisture. They are heavy feeders.",
        "tips": "Support with stakes or cages. Water at the base to avoid leaf diseases.",
        "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 100, 200], "growth_days": 90}
    },
    "onion": {
        "icon": "fa-solid fa-circle",
        "description": "Onions are bulb vegetables that need well-drained, fertile soil.",
        "tips": "Keep the area weed-free. Harvest when the tops fall over and turn brown.",
        "image": "https://images.unsplash.com/photo-1508747703725-719777637510?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [80, 40, 100], "growth_days": 100}
    },

    # --- NEW EXTENDED CROPS ---
    "groundnut": {
        "icon": "fa-solid fa-peanut",
        "description": "Groundnuts (Peanuts) are nitrogen-fixing legumes that mature underground.",
        "tips": "Ensure the soil is loose to allow pegs to enter. Avoid waterlogging during harvest.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Peanuts.jpg/800px-Peanuts.jpg",
        "meta": {"ideal_npk": [25, 50, 50], "growth_days": 120, "pests": ["Aphids", "Leaf Miner"], "weeds": ["Cynodon"], "organic": "Crop rotation and light pheromone traps."}
    },
    "radish": {
        "icon": "fa-solid fa-seedling",
        "description": "Radishes are fast-growing root vegetables that prefer cool weather.",
        "tips": "Thin out early to give roots space. Keep soil consistently moist for crunchy texture.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Radish_3371103037_1333d102e3_o.jpg/800px-Radish_3371103037_1333d102e3_o.jpg",
        "meta": {"ideal_npk": [40, 40, 60], "growth_days": 40}
    },
    "cucumber": {
        "icon": "fa-solid fa-cloud-sun",
        "description": "Cucumbers are hydrating vine crops that love warmth and vertical support.",
        "tips": "Provide a trellis to keep fruit off the ground. Mulch to retain soil moisture.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Cucumber_and_cross_section.jpg/800px-Cucumber_and_cross_section.jpg",
        "meta": {"ideal_npk": [50, 50, 100], "growth_days": 60}
    },
    "broccoli": {
        "icon": "fa-solid fa-leaf",
        "description": "Broccoli is a nutrient-dense brassica that thrives in cool, fertile soil.",
        "tips": "Apply organic compost before planting. Harvest the main head while it is tight.",
        "image": "https://images.unsplash.com/photo-1459411621453-7b03977f4bfc?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [150, 100, 150], "growth_days": 85}
    },
    "cabbage": {
        "icon": "fa-solid fa-leaf",
        "description": "Cabbage is a hardy vegetable that needs consistent moisture and nitrogen.",
        "tips": "Protect from caterpillars using organic neem spray. Harvest when heads are firm.",
        "image": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 80, 100], "growth_days": 90}
    },
    "peas": {
        "icon": "fa-solid fa-seedling",
        "description": "Peas are cool-season legumes that provide sweet, nutritious pods.",
        "tips": "Sow early in spring. Provide a small fence or mesh for climbing varieties.",
        "image": "https://images.unsplash.com/photo-1592394533824-9440e5d68530?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [30, 60, 40], "growth_days": 70}
    },
    "sugarcane": {
        "icon": "fa-solid fa-lines-leaning",
        "description": "Sugarcane is a tall, tropical perennial grass used for sugar and ethanol.",
        "tips": "Requires heavy irrigation and a long frost-free growing season.",
        "image": "https://images.unsplash.com/photo-1595167660456-12182747306b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [250, 100, 150], "growth_days": 365}
    },
    "lettuce": {
        "icon": "fa-solid fa-leaf",
        "description": "Lettuce is a high-demand salad crop that grows rapidly in cool weather.",
        "tips": "Keep roots cool and shaded in warmer months to prevent bolting.",
        "image": "https://images.unsplash.com/photo-1622206141540-5845044c5034?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 50, 50], "growth_days": 45}
    },
    "turmeric": {
        "icon": "fa-solid fa-hand-sparkles",
        "description": "Turmeric is a golden spice grown from rhizomes in humid, tropical regions.",
        "tips": "Requires well-drained, sandy loam. Maintain constant soil moisture.",
        "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [60, 50, 120], "growth_days": 270}
    },
    "ginger": {
        "icon": "fa-solid fa-hand-holding-hand",
        "description": "Ginger is a pungent rhizome used as a spice and for its medicinal properties.",
        "tips": "Grows best in partial shade. Avoid heavy clay soil to prevent rotting.",
        "image": "https://images.unsplash.com/photo-1591854238171-ec46aa670afb?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [75, 50, 50], "growth_days": 240}
    },
    "spinach": {
        "icon": "fa-solid fa-leaf",
        "description": "Spinach is a nutrient-rich leafy green that loves cooler temperatures.",
        "tips": "Keep soil fertile and damp. Harvest older leaves to encourage new growth.",
        "image": "https://images.unsplash.com/photo-1510627489930-0c1b0ba0c417?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 40, 40], "growth_days": 40}
    },
    "beetroot": {
        "icon": "fa-solid fa-seedling",
        "description": "Beetroot is a deep-red root crop packed with vitamins and minerals.",
        "tips": "Avoid high nitrogen fertilizers to prevent excess leaf growth at the expense of the root.",
        "image": "https://images.unsplash.com/photo-1590779033100-9f60705a2f3a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [60, 100, 100], "growth_days": 60}
    },
    "aster": {
        "icon": "fa-solid fa-sun",
        "description": "Asters are beautiful autumn-flowering perennials for diversified farming.",
        "tips": "Prefers well-drained soil and full sun. Remove faded flowers to extend blooming.",
        "image": "https://images.unsplash.com/photo-1597848212624-a19eb35e2651?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [50, 50, 50], "growth_days": 90}
    },
    "lilac": {
        "icon": "fa-solid fa-sun",
        "description": "Lilacs are fragrant shrubs that bloom in the late spring.",
        "tips": "Needs slightly alkaline soil and excellent drainage. Mulch in the summer.",
        "image": "https://images.unsplash.com/photo-1526315570773-45840d467972?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [30, 30, 30], "growth_days": 365}
    },
    "sweet corn": {
        "icon": "fa-solid fa-wheat-awn",
        "description": "Sweet corn is a popular variety of maize with high sugar content.",
        "tips": "Harvest when kernels are plump and milky. Plant in blocks for pollination.",
        "image": "https://images.unsplash.com/photo-1551729068-a974958ce3e4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [120, 60, 40], "growth_days": 90}
    },
    "most vegetables": {
        "icon": "fa-solid fa-leaf",
        "description": "A diverse range of garden vegetables suitable for balanced soil.",
        "tips": "Ensure consistent watering and regular organic fertilization.",
        "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [80, 80, 80], "growth_days": 60}
    },
    "brassicas": {
        "icon": "fa-solid fa-leaf",
        "description": "Brassicas (Cabbage/Broccoli family) are cool-season staples.",
        "tips": "Maintain soil pH around 6.5. Monitor for cabbage loopers.",
        "image": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [100, 80, 80], "growth_days": 90}
    },
    "legumes": {
        "icon": "fa-solid fa-seedling",
        "description": "Legumes (Beans/Peas) restore nitrogen to your field naturally.",
        "tips": "Inoculate seeds with Rhizobium for better yield and soil health.",
        "image": "https://images.unsplash.com/photo-1599596001004-972172778007?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [20, 60, 40], "growth_days": 70}
    },
    "root crops": {
        "icon": "fa-solid fa-carrot",
        "description": "Root crops provide stable yields and high calorie density.",
        "tips": "Keep soil light and loose. Ensure deep watering for robust roots.",
        "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
        "meta": {"ideal_npk": [60, 60, 100], "growth_days": 80}
    }
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
        "meta": {"ideal_npk": [100, 50, 50], "growth_days": 120}
    })
    return {
        "name": name.capitalize(),
        "icon": details["icon"],
        "description": details["description"],
        "tips": details["tips"],
        "image": details.get("image", "https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"),
        "meta": details.get("meta", {"ideal_npk": [100, 50, 50], "growth_days": 120})
    }
