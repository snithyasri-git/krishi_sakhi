from flask import Flask, render_template, request, jsonify
from weather import get_weather
from logic import get_advice
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/save_profile", methods=["POST"])
def save_profile():
    data = request.json
    farmer_name = data.get("farmerName")
    phone = data.get("phone")
    district = data.get("district")
    village = data.get("village")
    land_type = data.get("landType")
    crop = data.get("crop")

    # Get real weather data
    weather = get_weather(district)
    print(weather,"weather")
    
    # Get AI-powered advice
    advice = get_advice(crop, weather, land_type, district)
    print(advice,"advice")

    return jsonify({
        "farmerName": farmer_name,
        "phone": phone,
        "district": district,
        "village": village,
        "landType": land_type,
        "crop": crop,
        "temp": weather.get("temp"),
        "condition": weather.get("condition"),
        "rain_prob": weather.get("rain_prob", 0),
        "humidity": weather.get("humidity", 0),
        "wind_speed": weather.get("wind_speed", 0),
        "advice": advice
    })

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)