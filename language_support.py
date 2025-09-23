# language_support.py
import requests
import json

# Translation dictionaries for static content
TRANSLATIONS = {
    "ml": {  # Malayalam
        # Weather conditions
        "Clear Sky": "സ്വച്ഛമായ ആകാശം",
        "Mainly Clear": "പ്രധാനമായും സ്വച്ഛം",
        "Partly Cloudy": "ഭാഗികമായി മേഘാവൃതം",
        "Overcast": "പൂർണ്ണമായി മേഘാവൃതം",
        "Fog": "മൂടൽമഞ്ഞ്",
        "Depositing Rime Fog": "തുഷാര മൂടൽമഞ്ഞ്",
        "Light Drizzle": "ലഘു തുള്ളിപ്പനി",
        "Moderate Drizzle": "മിതമായ തുള്ളിപ്പനി",
        "Dense Drizzle": "കനത്ത തുള്ളിപ്പനി",
        "Light Freezing Drizzle": "ലഘു ഹിമതുള്ളിപ്പനി",
        "Dense Freezing Drizzle": "കനത്ത ഹിമതുള്ളിപ്പനി",
        "Slight Rain": "ലഘു മഴ",
        "Moderate Rain": "മിതമായ മഴ",
        "Heavy Rain": "കനത്ത മഴ",
        "Light Freezing Rain": "ലഘു ഹിമമഴ",
        "Heavy Freezing Rain": "കനത്ത ഹിമമഴ",
        "Slight Snow Fall": "ലഘു ഹിമപതനം",
        "Moderate Snow Fall": "മിതമായ ഹിമപതനം",
        "Heavy Snow Fall": "കനത്ത ഹിമപതനം",
        "Snow Grains": "ഹിമകണങ്ങൾ",
        "Slight Rain Showers": "ലഘു മഴത്തുള്ളികൾ",
        "Moderate Rain Showers": "മിതമായ മഴത്തുള്ളികൾ",
        "Violent Rain Showers": "ശക്തമായ മഴത്തുള്ളികൾ",
        "Slight Snow Showers": "ലഘു ഹിമത്തുള്ളികൾ",
        "Heavy Snow Showers": "കനത്ത ഹിമത്തുള്ളികൾ",
        "Thunderstorm": "இடிமழை",
        "Thunderstorm with Slight Hail": "ലഘു ആലിപ്പഴത്തോടുകൂടിയ இடிமழை",
        "Thunderstorm with Heavy Hail": "കനത്ത ആലിപ്പഴത്തോടുകൂടിയ இடிமழை",
        "Unknown": "അജ്ഞാതം",
        
        # Seasons
        "Dry season - irrigation may be needed": "വരണ്ട കാലാവസ്ഥ - നീരാവണി ആവശ്യമായി വന്നേക്കാം",
        "Pre-monsoon hot period - watch for heat stress": "മൺസൂണിന് മുമ്പത്തെ ചൂടുകാലം - ചൂട് സമ്മർദ്ദം ശ്രദ്ധിക്കുക",
        "Southwest monsoon - ensure drainage": "നൈഋത്യ മൺസൂൺ - ജലനിരപ്പ് ഉറപ്പാക്കുക",
        "Northeast monsoon - harvest planning": "വടകിഴക്കൻ മൺസൂൺ - വിളവെടുപ്പ് ആസൂത്രണം",
        
        # Generic advice components
        "High probability of rain. Ensure proper drainage in your fields.": "മഴയുടെ ഉയർന്ന സാധ്യത. നിങ്ങളുടെ വയലുകളിൽ ഉചിതമായ ജലനിരപ്പ് ഉറപ്പാക്കുക.",
        "Low probability of rain. Consider irrigation if soil is dry.": "മഴയുടെ കുറഞ്ഞ സാധ്യത. മണ്ണ് വരണ്ടാണെങ്കിൽ നീരാവണി പരിഗണിക്കുക.",
        "High humidity conditions. Monitor for fungal diseases and improve air circulation where possible.": "ഉയർന്ന ആർദ്രതാ സാഹചര്യങ്ങൾ. ഫംഗസ് രോഗങ്ങൾ നിരീക്ഷിക്കുകയും സാധ്യമെങ്കിൽ വായു സഞ്ചാരം മെച്ചപ്പെടുത്തുകയും ചെയ്യുക.",
        "Low humidity. Ensure adequate soil moisture and consider mulching to reduce evaporation.": "കുറഞ്ഞ ആർദ്രത. മണ്ണിന്റെ ഈർപ്പം ഉറപ്പാക്കുകയും ബാഷ്പീകരണം കുറയ്ക്കാൻ മൾച്ചിംഗ് പരിഗണിക്കുകയും ചെയ്യുക.",
        "Rainy conditions expected. Plan fieldwork accordingly and ensure proper drainage.": "മഴയുള്ള കാലാവസ്ഥ പ്രതീക്ഷിക്കാം. അതിനനുസരിച്ച് വയൽ ജോലി ആസൂത്രണം ചെയ്യുകയും ഉചിതമായ ജലനിരപ്പ് ഉറപ്പാക്കുകയും ചെയ്യുക.",
        "Sunny conditions are good for growth but monitor soil moisture levels regularly.": "വളർച്ചയ്ക്ക് സൂര്യപ്രകാശം നല്ലതാണ്, എന്നാൽ മണ്ണിന്റെ ഈർപ്പം ക്രമമായി നിരീക്ഷിക്കുക.",
        "Cloudy conditions may reduce evaporation but watch for fungal diseases in high humidity.": "മേഘാവൃതമായ കാലാവസ്ഥ ബാഷ്പീകരണം കുറയ്ക്കും, എന്നാൽ ഉയർന്ന ആർദ്രതയിൽ ഫംഗസ് രോഗങ്ങൾ ശ്രദ്ധിക്കുക.",
        
        # Land types
        "Sandy soil drains quickly. Consider more frequent irrigation and add organic matter to improve water retention.": "മണൽ മണ്ണ് വേഗത്തിൽ വറ്റുന്നു. കൂടുതൽ തവണ നീരാവണി പരിഗണിക്കുകയും ജല സംരക്ഷണം മെച്ചപ്പെടുത്താൻ ജൈവ പദാർത്ഥങ്ങൾ ചേർക്കുകയും ചെയ്യുക.",
        "Clay soil retains moisture well. Be cautious of overwatering and ensure good drainage to prevent waterlogging.": "ചെളി മണ്ണ് ഈർപ്പം നന്നായി പിടിച്ച് നിർത്തുന്നു. അമിതമായി വെള്ളം ഒഴിക്കുന്നതിൽ ശ്രദ്ധിക്കുകയും വെള്ളം കെട്ടുന്നത് തടയാൻ നല്ല ജലനിരപ്പ് ഉറപ്പാക്കുകയും ചെയ്യുക.",
        "Loamy soil has good properties for most crops. Maintain organic matter content through regular additions.": "എക്കൽ മണ്ണിന് മിക്ക വിളകൾക്കും നല്ല ഗുണങ്ങളുണ്ട്. ക്രമമായി ജൈവ പദാർത്ഥങ്ങൾ ചേർത്ത് അവയുടെ അംശം നിലനിർത്തുക.",
        "Alluvial soil is generally fertile. Monitor nutrient levels and supplement as needed based on crop requirements.": "അവശിഷ്ട മണ്ണ് സാധാരണയായി ഫലവത്താണ്. പോഷകാഹാര നില നിരീക്ഷിക്കുകയും വിളയുടെ ആവശ്യങ്ങളെ അടിസ്ഥാനമാക്കി ആവശ്യമായി സപ്ലിമെന്റ് ചെയ്യുകയും ചെയ്യുക.",
        "Rocky soil may need amendments for better water retention and root growth. Consider terracing in sloped areas.": "പാറക്കല്ല് മണ്ണിന് നല്ല ജല സംരക്ഷണത്തിനും വേരുകളുടെ വളർച്ചയ്ക്കും തിരുത്തലുകൾ ആവശ്യമായി വന്നേക്കാം. ചരിഞ്ഞ പ്രദേശങ്ങളിൽ ചരിവ് പരിഗണിക്കുക.",
        
        # District-specific advice
        "This hilly region may have microclimates. Consider local conditions in your planning.": "ഈ പർവതപ്രദേശത്ത് മൈക്രോക്ലൈമെറ്റുകൾ ഉണ്ടാകാം. നിങ്ങളുടെ ആസൂത്രണത്തിൽ പ്രാദേശിക സാഹചര്യങ്ങൾ പരിഗണിക്കുക.",
        "Hilly terrain requires careful soil conservation. Terrace farming is recommended.": "പർവതപ്രദേശത്തിന് ശ്രദ്ധയോടെയുള്ള മണ്ണ് സംരക്ഷണം ആവശ്യമാണ്. ചരിവ് കൃഷി ശുപാർശ ചെയ്യുന്നു.",
        "Being in a low-lying area, requires careful water management, especially during heavy rains.": "താഴ്ന്ന പ്രദേശമായതിനാൽ, പ്രത്യേകിച്ച് കനത്ത മഴയ്ക്ക് സമയത്ത് ശ്രദ്ധയോടെയുള്ള ജല management ആവശ്യമാണ്.",
        "Unique below-sea-level farming requires specialized water management practices.": "സമുദ്രനിരപ്പിന് താഴെയുള്ള അദ്വിതീയ കൃഷിക്ക് സ്പെഷ്യലൈസ്ഡ് ജല management പ്രാക്ടീസുകൾ ആവശ്യമാണ്.",
        "Relatively drier region. Water conservation techniques are important.": "ആപേക്ഷികമായി വരണ്ട പ്രദേശം. ജല സംരക്ഷണ techniqueകൾ പ്രധാനമാണ്.",
        "Diverse agricultural zone. Consider local microclimates for crop planning.": "വൈവിധ്യമാർന്ന കാർഷിക മേഖല. വിള ആസൂത്രണത്തിന് പ്രാദേശിക മൈക്രോക്ലൈമെറ്റുകൾ പരിഗണിക്കുക.",
        "Consider local conditions and consult with agricultural officers for specific advice.": "പ്രാദേശിക സാഹചര്യങ്ങൾ പരിഗണിക്കുകയും നിർദ്ദിഷ്ട ഉപദേശത്തിന് കാർഷിക ഉദ്യോഗസ്ഥരുമായി കൂടിയാലോചിക്കുകയും ചെയ്യുക.",
        
        # General advice
        "Regularly monitor your crops for signs of pests, diseases, or nutrient deficiencies.": "കീടങ്ങൾ, രോഗങ്ങൾ അല്ലെങ്കിൽ പോഷകാഹാര കുറവുകളുടെ ലക്ഷണങ്ങൾക്കായി നിങ്ങളുടെ വിളകൾ ക്രമമായി നിരീക്ഷിക്കുക.",
        "Maintain soil health through organic matter addition and appropriate crop rotation.": "ജൈവ പദാർത്ഥങ്ങൾ ചേർക്കലിലൂടെയും ഉചിതമായ വിള ഭ്രമണത്തിലൂടെയും മണ്ണിന്റെ ആരോഗ്യം നിലനിർത്തുക.",
        "Keep records of weather patterns and crop performance to improve future planning.": "ഭാവി ആസൂത്രണം മെച്ചപ്പെടുത്താൻ കാലാവസ്ഥാ പാറ്റേണുകളുടെയും വിള പ്രകടനത്തിന്റെയും റെക്കോർഡുകൾ സൂക്ഷിക്കുക."
    }
}

class LanguageManager:
    def __init__(self):
        self.current_language = "en"  # Default to English
    
    def set_language(self, language):
        if language in ["en", "ml"]:
            self.current_language = language
        return self.current_language
    
    def get_current_language(self):
        return self.current_language
    
    def translate_text(self, text):
        """Translate text to current language"""
        if self.current_language == "en" or text is None:
            return text
        
        # Check if translation exists
        if self.current_language in TRANSLATIONS:
            lang_dict = TRANSLATIONS[self.current_language]
            if text in lang_dict:
                return lang_dict[text]
        
        # Return original text if no translation found
        return text
    
    def translate_weather_data(self, weather_data):
        """Translate weather condition in weather data"""
        if weather_data and "condition" in weather_data:
            weather_data["condition"] = self.translate_text(weather_data["condition"])
        return weather_data
    
    def translate_advice(self, advice_text):
        """Translate agricultural advice text"""
        if self.current_language == "en":
            return advice_text
        
        # For Malayalam, we'll use a simpler approach by translating key phrases
        # For production, you might want to use a translation API
        if self.current_language == "ml":
            # Split and translate common phrases
            translated_parts = []
            sentences = advice_text.split('. ')
            
            for sentence in sentences:
                if sentence.strip():
                    translated = self.translate_text(sentence.strip())
                    if translated:
                        translated_parts.append(translated)
            
            return '. '.join(translated_parts)
        
        return advice_text

# Global language manager instance
language_manager = LanguageManager()