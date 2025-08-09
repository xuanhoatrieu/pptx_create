
import google.generativeai as genai

def get_gemini_client(api_key):
    """Initializes and returns the Gemini API client."""
    genai.configure(api_key=api_key)
    return genai
