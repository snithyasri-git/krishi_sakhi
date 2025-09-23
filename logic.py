from language_support import language_manager
# Agricultural knowledge base - Enhanced for Kerala crops
CROP_ADVICE_KNOWLEDGE = {
    "paddy": {
        "ideal_temp": (20, 35),
        "ideal_rainfall": (150, 300),
        "advice": {
            "high_temp": "Provide adequate water to prevent heat stress. Consider scheduling irrigation during cooler parts of the day.",
            "low_temp": "Protect seedlings with covers if temperature drops significantly.",
            "high_rain": "Ensure proper drainage to prevent waterlogging. Check field bunds regularly.",
            "low_rain": "Implement water conservation techniques. Consider supplemental irrigation.",
            "normal": "Continue regular maintenance. Monitor for pests and diseases."
        }
    },
    "coconut": {
        "ideal_temp": (20, 35),
        "ideal_rainfall": (100, 200),
        "advice": {
            "high_temp": "Increase irrigation frequency. Mulch around trees to retain soil moisture.",
            "low_temp": "Young palms may need protection from cold winds.",
            "high_rain": "Ensure good drainage to prevent root rot.",
            "low_rain": "Implement drip irrigation for water efficiency.",
            "normal": "Continue regular care. Apply balanced fertilizers as needed."
        }
    },
    "banana": {
        "ideal_temp": (22, 32),
        "ideal_rainfall": (120, 220),
        "advice": {
            "high_temp": "Provide regular irrigation. Use mulch to conserve soil moisture.",
            "low_temp": "Protect plants with covers during cold periods.",
            "high_rain": "Ensure good drainage to prevent waterlogging and root diseases.",
            "low_rain": "Increase irrigation frequency. Drip irrigation is recommended.",
            "normal": "Continue regular care. Remove diseased leaves promptly."
        }
    },
    "rubber": {
        "ideal_temp": (22, 35),
        "ideal_rainfall": (200, 300),
        "advice": {
            "high_temp": "Ensure adequate soil moisture. Young trees may need shading.",
            "low_temp": "Mature trees are generally tolerant but monitor for cold damage.",
            "high_rain": "Ensure good drainage. Waterlogging can harm roots.",
            "low_rain": "Supplemental irrigation may be needed during dry periods.",
            "normal": "Continue regular tapping schedule. Monitor for leaf diseases."
        }
    },
    "tea": {
        "ideal_temp": (15, 30),
        "ideal_rainfall": (150, 250),
        "advice": {
            "high_temp": "Provide shade if possible. Ensure adequate soil moisture.",
            "low_temp": "Tea is generally cold-tolerant but frost can damage tender shoots.",
            "high_rain": "Ensure good drainage. Prune bushes to improve air circulation.",
            "low_rain": "Supplemental irrigation is essential for quality leaf production.",
            "normal": "Continue regular plucking. Monitor for pests and diseases."
        }
    },
    "pepper": {
        "ideal_temp": (20, 35),
        "ideal_rainfall": (150, 250),
        "advice": {
            "high_temp": "Provide adequate shade and moisture. Mulch around plants.",
            "low_temp": "Protect plants from cold winds. Frost can be damaging.",
            "high_rain": "Ensure good drainage. Waterlogging can cause root diseases.",
            "low_rain": "Regular irrigation is essential. Drip irrigation works well.",
            "normal": "Continue regular care. Support vines properly as they grow."
        }
    },
    "cardamom": {
        "ideal_temp": (10, 35),
        "ideal_rainfall": (150, 300),
        "advice": {
            "high_temp": "Provide shade and adequate moisture. Mulch heavily.",
            "low_temp": "Protect from frost. Cardamom is sensitive to cold.",
            "high_rain": "Ensure excellent drainage. Waterlogging is detrimental.",
            "low_rain": "Regular irrigation is crucial. Maintain high humidity.",
            "normal": "Continue regular care. Divide and replant overcrowded clumps."
        }
    },
    "tapioca": {
        "ideal_temp": (20, 35),
        "ideal_rainfall": (100, 200),
        "advice": {
            "high_temp": "Ensure adequate moisture. Tapioca is drought-tolerant but benefits from irrigation.",
            "low_temp": "Protect from cold temperatures which can damage the crop.",
            "high_rain": "Ensure good drainage to prevent root rot.",
            "low_rain": "Tapioca is drought-resistant but irrigation improves yield.",
            "normal": "Continue regular care. Harvest when roots are mature."
        }
    }
}

# Kerala seasonal patterns
KERALA_SEASONS = {
    "1-3": "Dry season - irrigation may be needed",
    "4-6": "Pre-monsoon hot period - watch for heat stress",
    "7-9": "Southwest monsoon - ensure drainage",
    "10-12": "Northeast monsoon - harvest planning"
}

def get_seasonal_advice():
    """Get advice based on current month"""
    import datetime
    month = datetime.datetime.now().month
    
    if 1 <= month <= 3:
        season_text = "Dry season - irrigation may be needed"
    elif 4 <= month <= 6:
        season_text = "Pre-monsoon hot period - watch for heat stress"
    elif 7 <= month <= 9:
        season_text = "Southwest monsoon - ensure drainage"
    else:
        season_text = "Northeast monsoon - harvest planning"
    
    return language_manager.translate_text(season_text)

def get_advice(crop, weather, land_type, district):
    """Generate contextual agricultural advice based on crop, weather, and soil conditions"""
    crop = crop.lower()
    temp = weather.get('temp', 30)
    condition = weather.get('condition', '').lower()
    rain_prob = weather.get('rain_prob', 0)
    humidity = weather.get('humidity', 70)
    
    advice_parts = []
    
    # Add seasonal advice (already translated in get_seasonal_advice)
    advice_parts.append(get_seasonal_advice())
    
    # Temperature-based advice
    if crop in CROP_ADVICE_KNOWLEDGE:
        ideal_min, ideal_max = CROP_ADVICE_KNOWLEDGE[crop]["ideal_temp"]
        
        if temp > ideal_max + 5:
            advice_text = CROP_ADVICE_KNOWLEDGE[crop]["advice"]["high_temp"]
        elif temp < ideal_min - 5:
            advice_text = CROP_ADVICE_KNOWLEDGE[crop]["advice"]["low_temp"]
        else:
            advice_text = CROP_ADVICE_KNOWLEDGE[crop]["advice"]["normal"]
        
        advice_parts.append(language_manager.translate_text(advice_text))
    else:
        # Generic temperature advice for unknown crops
        if temp > 35:
            advice_text = "High temperature detected. Ensure adequate irrigation and consider shading for sensitive plants."
        elif temp < 20:
            advice_text = "Low temperature. Protect sensitive plants from cold stress."
        else:
            advice_text = "Temperature conditions are favorable for most crops."
        
        advice_parts.append(language_manager.translate_text(advice_text))
    
    # Rainfall probability advice
    if rain_prob > 70:
        if crop in CROP_ADVICE_KNOWLEDGE:
            advice_text = CROP_ADVICE_KNOWLEDGE[crop]["advice"]["high_rain"]
        else:
            advice_text = "High probability of rain. Ensure proper drainage in your fields."
        advice_parts.append(language_manager.translate_text(advice_text))
    elif rain_prob < 20:
        if crop in CROP_ADVICE_KNOWLEDGE:
            advice_text = CROP_ADVICE_KNOWLEDGE[crop]["advice"]["low_rain"]
        else:
            advice_text = "Low probability of rain. Consider irrigation if soil is dry."
        advice_parts.append(language_manager.translate_text(advice_text))
    
    # Humidity-based advice
    if humidity > 85:
        advice_text = "High humidity conditions. Monitor for fungal diseases and improve air circulation where possible."
        advice_parts.append(language_manager.translate_text(advice_text))
    elif humidity < 50:
        advice_text = "Low humidity. Ensure adequate soil moisture and consider mulching to reduce evaporation."
        advice_parts.append(language_manager.translate_text(advice_text))
    
    # Weather condition-based advice
    if "rain" in condition:
        advice_text = "Rainy conditions expected. Plan fieldwork accordingly and ensure proper drainage."
        advice_parts.append(language_manager.translate_text(advice_text))
    elif "sunny" in condition or "clear" in condition:
        advice_text = "Sunny conditions are good for growth but monitor soil moisture levels regularly."
        advice_parts.append(language_manager.translate_text(advice_text))
    elif "cloud" in condition:
        advice_text = "Cloudy conditions may reduce evaporation but watch for fungal diseases in high humidity."
        advice_parts.append(language_manager.translate_text(advice_text))
    
    # Land type-based advice
    land_advice = {
        "sandy": "Sandy soil drains quickly. Consider more frequent irrigation and add organic matter to improve water retention.",
        "clay": "Clay soil retains moisture well. Be cautious of overwatering and ensure good drainage to prevent waterlogging.",
        "loamy": "Loamy soil has good properties for most crops. Maintain organic matter content through regular additions.",
        "alluvial": "Alluvial soil is generally fertile. Monitor nutrient levels and supplement as needed based on crop requirements.",
        "rocky": "Rocky soil may need amendments for better water retention and root growth. Consider terracing in sloped areas."
    }
    
    if land_type.lower() in land_advice:
        advice_text = land_advice[land_type.lower()]
        advice_parts.append(language_manager.translate_text(advice_text))
    
    # District-specific considerations
    district_advice = {
        "idukki": "This hilly region may have microclimates. Consider local conditions in your planning.",
        "wayanad": "Hilly terrain requires careful soil conservation. Terrace farming is recommended.",
        "alappuzha": "Being in a low-lying area, requires careful water management, especially during heavy rains.",
        "kuttanad": "Unique below-sea-level farming requires specialized water management practices.",
        "palakkad": "Relatively drier region. Water conservation techniques are important.",
        "thrissur": "Diverse agricultural zone. Consider local microclimates for crop planning."
    }
    
    if district.lower() in district_advice:
        advice_text = district_advice[district.lower()]
    else:
        advice_text = f"Consider local {district} conditions and consult with agricultural officers for specific advice."
    
    advice_parts.append(language_manager.translate_text(advice_text))
    
    # General best practices (already handled by translation)
    general_advice = [
        "Regularly monitor your crops for signs of pests, diseases, or nutrient deficiencies.",
        "Maintain soil health through organic matter addition and appropriate crop rotation.",
        "Keep records of weather patterns and crop performance to improve future planning."
    ]
    
    for advice in general_advice:
        advice_parts.append(language_manager.translate_text(advice))
    
    return " ".join(advice_parts)

# Simple function to simulate what the app expects
def get_advice_simple(crop, weather, land_type, district):
    """Simplified version that matches the expected function signature"""
    return get_advice(crop, weather, land_type, district)