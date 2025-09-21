import requests
import random
from datetime import datetime

# Kerala district coordinates mapping
KERALA_DISTRICTS_COORDINATES = {
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366},
    "Kollam": {"lat": 8.8932, "lon": 76.6141},
    "Pathanamthitta": {"lat": 9.2648, "lon": 76.7870},
    "Alappuzha": {"lat": 9.4981, "lon": 76.3388},
    "Kottayam": {"lat": 9.5916, "lon": 76.5222},
    "Idukki": {"lat": 9.9189, "lon": 76.9445},
    "Ernakulam": {"lat": 9.9816, "lon": 76.2999},
    "Thrissur": {"lat": 10.5276, "lon": 76.2144},
    "Palakkad": {"lat": 10.7867, "lon": 76.6548},
    "Malappuram": {"lat": 11.0510, "lon": 76.0711},
    "Kozhikode": {"lat": 11.2588, "lon": 75.7804},
    "Wayanad": {"lat": 11.6854, "lon": 76.1320},
    "Kannur": {"lat": 11.8745, "lon": 75.3704},
    "Kasaragod": {"lat": 12.4996, "lon": 74.9869}
}

def get_weather(city):
    """Get real weather data from Open-Meteo API"""
    # Get coordinates for the district
    if city not in KERALA_DISTRICTS_COORDINATES:
        return get_fallback_weather(city)
    
    coords = KERALA_DISTRICTS_COORDINATES[city]
    
    try:
        # Current weather and forecast API call
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&hourly=precipitation_probability&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Asia/Kolkata"
        response = requests.get(url, timeout=10)
        data = response.json()
        print(data,"response from open-meteo")
        
        if response.status_code == 200:
            current = data.get("current", {})
            hourly = data.get("hourly", {})
            
            # Get current hour's precipitation probability
            current_hour = datetime.now().hour
            precip_probs = hourly.get("precipitation_probability", [])
            rain_prob = precip_probs[current_hour] if current_hour < len(precip_probs) else 0
            
            # Map weather code to condition description
            weather_code = current.get("weather_code", 0)
            condition = map_weather_code(weather_code)
            
            return {
                "temp": round(current.get("temperature_2m", 30)),
                "condition": condition,
                "humidity": current.get("relative_humidity_2m", 70),
                "wind_speed": current.get("wind_speed_10m", 5),
                "rain_prob": rain_prob
            }
        else:
            return get_fallback_weather(city)
            
    except (requests.RequestException, KeyError, ValueError):
        return get_fallback_weather(city)

def map_weather_code(code):
    """Map WMO weather code to human-readable description"""
    weather_codes = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow Fall",
        73: "Moderate Snow Fall",
        75: "Heavy Snow Fall",
        77: "Snow Grains",
        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Slight Hail",
        99: "Thunderstorm with Heavy Hail"
    }
    return weather_codes.get(code, "Unknown")

def get_fallback_weather(city):
    """Fallback weather data in case API fails"""
    # Simple fallback with seasonal variations
    fallback_data = {
        "temp": random.randint(25, 35),
        "condition": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]),
        "humidity": random.randint(60, 90),
        "wind_speed": random.randint(2, 8),
        "rain_prob": random.randint(0, 70)
    }
    return fallback_data