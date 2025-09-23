from flask import Flask, render_template, request, jsonify
from weather import get_weather
from logic import get_advice
import google.generativeai as genai
import os
from dotenv import load_dotenv
from language_support import language_manager

load_dotenv()

app = Flask(__name__)

# Configure Gemini AI with better error handling
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ Gemini AI configured successfully")
        # Test the configuration
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini AI model loaded successfully")
    except Exception as e:
        print(f"❌ Gemini AI configuration failed: {e}")
        GEMINI_API_KEY = None
else:
    print("❌ GEMINI_API_KEY not found in environment variables")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/set_language", methods=["POST"])
def set_language():
    data = request.json
    language = data.get("language", "en")
    language_manager.set_language(language)
    return jsonify({"status": "success", "language": language})

@app.route("/save_profile", methods=["POST"])
def save_profile():
    try:
        data = request.json
        farmer_name = data.get("farmerName")
        phone = data.get("phone")
        district = data.get("district")
        village = data.get("village")
        land_type = data.get("landType")
        crop = data.get("crop")

        print(f"📝 Received data: {data}")

        weather = get_weather(district)
        advice = get_advice(crop, weather, land_type, district)

        print(f"🌤️ Weather data: {weather}")
        print(f"💡 Advice: {advice}")

        # Translate weather information based on current language
        current_language = language_manager.get_current_language()
        
        if current_language == "ml":
            condition_translations = {
                "Sunny": "വെയിലുള്ള", "Clear": "തെളിഞ്ഞ", "Cloudy": "മേഘാവൃതം", 
                "Rainy": "മഴയുള്ള", "Partly cloudy": "ഭാഗികമേഘാവൃതം", "Overcast": "കുളിരുള്ള",
                "Mist": "മൂടൽമഞ്ഞ്", "Fog": "പുകപ്പടലം", "Drizzle": "തുള്ളിമഴ",
                "Light rain": "ലഘുമഴ", "Moderate rain": "മധ്യമമഴ", "Heavy rain": "കനമഴ"
            }
            weather["condition"] = condition_translations.get(weather.get("condition"), weather.get("condition"))
            
        elif current_language == "ta":
            condition_translations = {
                "Sunny": "வெயிலான", "Clear": "தெளிவான", "Cloudy": "மேகமூட்டம்", 
                "Rainy": "மழையுள்ள", "Partly cloudy": "பகுதி மேகமூட்டம்", "Overcast": "முழுமேகமூட்டம்",
                "Mist": "மூடுபனி", "Fog": "பனிப்புகல்", "Drizzle": "தூறல்",
                "Light rain": "இலேசான மழை", "Moderate rain": "மிதமான மழை", "Heavy rain": "கனமழை"
            }
            weather["condition"] = condition_translations.get(weather.get("condition"), weather.get("condition"))

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
            "advice": advice,
            "language": current_language
        })
    
    except Exception as e:
        print(f"❌ Error in save_profile: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/ask_gemini", methods=["POST"])
def ask_gemini():
    try:
        print("🤖 Gemini AI endpoint called")
        
        if not GEMINI_API_KEY:
            error_msg = "❌ Gemini API key not configured"
            print(error_msg)
            return jsonify({"error": error_msg}), 500
            
        data = request.json
        print(f"📨 Received data: {data}")
        
        user_question = data.get("question", "").strip()
        farmer_context = data.get("context", {})
        current_language = language_manager.get_current_language()
        
        if not user_question:
            error_msg = "❌ No question provided"
            print(error_msg)
            return jsonify({"error": error_msg}), 400
        
        print(f"🌐 Current language: {current_language}")
        print(f"❓ Question: {user_question}")
        
        # Update prompt based on language
        language_instruction = ""
        if current_language == "ml":
            language_instruction = "IMPORTANT: Respond in Malayalam language using Malayalam script. Use simple agricultural terms."
        elif current_language == "ta":
            language_instruction = "IMPORTANT: Respond in Tamil language using Tamil script. Use simple agricultural terms."
        
        prompt = f"""
        You are Krishi Sakhi, an agricultural assistant for Indian farmers.

        Farmer's Context:
        - Crop: {farmer_context.get('crop', 'Not specified')}
        - District: {farmer_context.get('district', 'Not specified')}
        - Soil Type: {farmer_context.get('landType', 'Not specified')}
        - Weather: {farmer_context.get('weather', 'Not specified')}

        Question: {user_question}

        {language_instruction}

        FORMATTING:
        - Use bullet points with • symbol
        - Each point should be concise (1-2 lines)
        - Use relevant emojis
        - Maximum 5-6 points
        - End with encouragement

        Response:
        """
        
        print(f"📝 Prompt sent to Gemini: {prompt[:200]}...")
        
        # Generate response with timeout
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                    top_p=0.8
                )
            )
            
            print("✅ Gemini response received")
            answer_text = response.text.strip()
            print(f"📄 Response text: {answer_text[:100]}...")
            
        except Exception as api_error:
            print(f"❌ Gemini API error: {api_error}")
            # Fallback response
            if current_language == "ml":
                answer_text = "• 🌱 ക്ഷമിക്കണം, താൽക്കാലിക സമസ്യയുണ്ട്\n• 🔄 കുറച്ച് നിമിഷങ്ങൾക്ക് ശേഷം വീണ്ടും ശ്രമിക്കുക\n• 📞 അത്യാവശ്യത്തിന് കൃഷി ഭവനത്തിൽ ബന്ധപ്പെടുക\n• 😊 ദയവായി വീണ്ടും ശ്രമിക്കുക!"
            elif current_language == "ta":
                answer_text = "• 🌱 மன்னிக்கவும், தற்காலிக பிரச்சனை\n• 🔄 சில நிமிடங்களில் மீண்டும் முயற்சிக்கவும்\n• 📞 அவசரத்திற்கு விவசாய அலுவலகத்தை தொடர்பு கொள்ளவும்\n• 😊 தயவு செய்து மீண்டும் முயற்சிக்கவும்!"
            else:
                answer_text = "• 🌱 Sorry, temporary issue\n• 🔄 Please try again in a few minutes\n• 📞 Contact Krishi Bhavan for urgent help\n• 😊 Please try again!"
        
        # Format response if needed
        if not any(char in answer_text for char in ['•', '-', '*']):
            print("🔧 Formatting response to bullet points...")
            sentences = [s.strip() for s in answer_text.split('.') if s.strip()]
            bullet_points = []
            emojis = ['🌱', '💧', '🌾', '🌞', '🐛', '💪', '📝', '😊']
            
            for i, sentence in enumerate(sentences[:6]):
                if sentence and len(sentence) > 5:  # Avoid very short sentences
                    emoji = emojis[i % len(emojis)]
                    clean_sentence = sentence.lstrip('123456789.-* ').strip()
                    if clean_sentence:
                        bullet_points.append(f"• {emoji} {clean_sentence}")
            
            if bullet_points:
                if current_language == "ml" and not any('😊' in point or '🌱' in point for point in bullet_points[-2:]):
                    bullet_points.append("• 😊 നന്ദി, വീണ്ടും ചോദിക്കുക!")
                elif current_language == "ta" and not any('😊' in point or '🌱' in point for point in bullet_points[-2:]):
                    bullet_points.append("• 😊 நன்றி, மீண்டும் கேளுங்கள்!")
                elif not any('😊' in point or '🌱' in point for point in bullet_points[-2:]):
                    bullet_points.append("• 😊 Thank you, ask again!")
                
                answer_text = '\n'.join(bullet_points)
        
        print(f"✅ Final response: {answer_text[:100]}...")
        return jsonify({"answer": answer_text})
        
    except Exception as e:
        print(f"❌ Critical error in ask_gemini: {e}")
        current_language = language_manager.get_current_language()
        if current_language == "ml":
            error_response = "• ⚠️ സിസ്റ്റം താൽക്കാലികമായി പ്രവർത്തിക്കുന്നില്ല\n• 🔄 പേജ് refresh ചെയ്ത് വീണ്ടും ശ്രമിക്കുക\n• 🌱 ക്ഷമിക്കണം, അസൗകര്യത്തിന്"
        elif current_language == "ta":
            error_response = "• ⚠️ கணினி தற்காலிகமாக செயல்படவில்லை\n• 🔄 பக்கத்தைப் புதுப்பித்து மீண்டும் முயற்சிக்கவும்\n• 🌱 மன்னிக்கவும், சிரமத்திற்கு"
        else:
            error_response = "• ⚠️ System temporarily down\n• 🔄 Refresh page and try again\n• 🌱 Sorry for the inconvenience"
        
        return jsonify({"answer": error_response})

@app.route("/test_gemini")
def test_gemini():
    """Test route to check if Gemini AI is working"""
    try:
        if not GEMINI_API_KEY:
            return jsonify({"status": "error", "message": "API key missing"})
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Hello' in one word.")
        
        return jsonify({
            "status": "success", 
            "message": "Gemini AI is working",
            "response": response.text
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    print("🚀 Starting Flask application...")
    print(f"🔑 API Key present: {bool(GEMINI_API_KEY)}")
    app.run(debug=True, host='0.0.0.0', port=5000)