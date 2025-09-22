import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # load GEMINI_API_KEY from .env

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Gemini API Key not found in environment variables!")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Initialize chatbot model
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Send a message to Gemini chatbot and return its reply in bullet points"""
    try:
        # Enhanced prompt to force bullet point format
        enhanced_prompt = f"""Please provide the response in bullet points format only. Use • for each bullet point and keep it concise.

Question: {prompt}

Format your response exactly like this:
• [First point]
• [Second point] 
• [Third point]
• [Fourth point]

Keep each bullet point short and practical. Use relevant emojis where appropriate."""

        response = model.generate_content(
            enhanced_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        
        # Ensure the response is in bullet point format
        response_text = response.text.strip()
        
        # If response doesn't start with bullet points, convert it
        if not response_text.startswith(('•', '-', '*')):
            # Split by sentences and convert to bullet points
            sentences = [s.strip() for s in response_text.split('.') if s.strip()]
            bullet_points = []
            for sentence in sentences[:5]:  # Limit to 5 bullet points
                if sentence and not sentence.endswith('.'):
                    sentence += '.'
                bullet_points.append(f"• {sentence}")
            
            response_text = '\n'.join(bullet_points)
        
        return response_text
        
    except Exception as e:
        return f"• ⚠️ Gemini error: {str(e)}"