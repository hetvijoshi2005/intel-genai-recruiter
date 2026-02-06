import requests
import os
from dotenv import load_dotenv

load_dotenv()

# CHECK YOUR HACKATHON DOCS: 
# The URL might be "https://api.scaledown.ai/v1/compress" or similar.
# Verify this exact URL from your challenge instructions.
SCALEDOWN_URL = "https://api.scaledown.ai/v1/compress" 

def compress_resume(raw_text):
    """
    Sends raw resume text to ScaleDown to reduce token count using Gemini 2.5 Flash.
    """
    api_key = os.getenv("SCALEDOWN_API_KEY")
    if not api_key:
        return raw_text  # Fail safe: return original text if no key
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Updated payload with the specific model you selected
    payload = {
        "text": raw_text,
        "model": "gemini-2.5-flash",  # <--- SELECTED MODEL
        "compression_rate": 0.8       # Target 80% reduction
    }
    
    try:
        response = requests.post(SCALEDOWN_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Check if the API returns 'compressed_text' or just 'text'
            # Adjust this key based on the actual API response format
            return response.json().get("compressed_text", raw_text)
        else:
            print(f"ScaleDown Error {response.status_code}: {response.text}")
            return raw_text
            
    except Exception as e:
        print(f"ScaleDown Connection Error: {e}")
        return raw_text