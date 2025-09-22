from flask import Flask, render_template, request, jsonify
from weather import get_weather
from logic import get_advice
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ Gemini AI configured successfully")
else:
    print("❌ GEMINI_API_KEY not found")

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

    weather = get_weather(district)
    advice = get_advice(crop, weather, land_type, district)

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

# UPDATED GEMINI ROUTE WITH BULLET POINT FORMATTING
@app.route("/ask_gemini", methods=["POST"])
def ask_gemini():
    try:
        if not GEMINI_API_KEY:
            return jsonify({"error": "Gemini API key not configured"}), 500
            
        data = request.json
        print(data,"dkfjklgfdjjgl")
        user_question = data.get("question", "").strip()
        farmer_context = data.get("context", {})
        
        if not user_question:
            return jsonify({"error": "No question provided"}), 400
        
        # UPDATED PROMPT FOR STRICT BULLET POINT FORMATTING
        prompt = f"""
        You are Krishi Sakhi, an agricultural assistant for Kerala farmers.
        
        Farmer's Context:
        - Crop: {farmer_context.get('crop', 'Not specified')}
        - District: {farmer_context.get('district', 'Not specified')}
        - Soil Type: {farmer_context.get('landType', 'Not specified')}
        - Weather: {farmer_context.get('weather', 'Not specified')}
        
        Question: {user_question}
        
        CRITICAL FORMATTING REQUIREMENTS:
        - Respond ONLY in bullet points using • symbol
        - Each bullet point must start with • followed by a space
        - Use relevant emojis at the beginning of each bullet point
        - Maximum 5-6 bullet points total
        - Each bullet should be 1-2 lines maximum
        - No paragraphs, no long explanations
        - No introduction sentences, just direct bullet points
        - End with one encouraging bullet point with 😊 or 🌱 emoji
        
        Example format:
        • 🌱 [First point here]
        • 💧 [Second point here]
        • 🌾 [Third point here]
        • 😊 [Encouraging note]
        
        Now provide the response:
        """
        print(prompt)
        
        # Generate response
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=300  # Limit length for brevity
            )
        )
        
        # ENSURE BULLET POINT FORMAT - FALLBACK IF GEMINI DOESN'T FOLLOW
        answer_text = response.text.strip()
        
        # If response doesn't contain bullet points, convert it
        if not any(char in answer_text for char in ['•', '-', '*']):
            # Convert to bullet points
            sentences = [s.strip() for s in answer_text.split('.') if s.strip()]
            bullet_points = []
            emojis = ['🌱', '💧', '🌾', '🌞', '🐛', '💪', '📝', '😊']
            
            for i, sentence in enumerate(sentences[:6]):  # Max 6 points
                if sentence:
                    emoji = emojis[i % len(emojis)]
                    # Remove any existing numbering or bullets
                    clean_sentence = sentence.lstrip('123456789.-* ').strip()
                    if clean_sentence and not clean_sentence.endswith('.'):
                        clean_sentence += '.'
                    bullet_points.append(f"• {emoji} {clean_sentence}")
            
            # Add encouraging note if not present
            if bullet_points and '😊' not in answer_text and '🌱' not in answer_text[-10:]:
                bullet_points.append("• 😊 Stay positive and keep observing your crops!")
            
            answer_text = '\n'.join(bullet_points)
        
        return jsonify({"answer": answer_text})
        
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        error_response = "• ⚠️ AI service is temporarily unavailable. Please try again later.\n• 🌱 In the meantime, consult your local Krishi Bhavan for assistance!"
        return jsonify({"answer": error_response})

if __name__ == "__main__":
    app.run(debug=True)