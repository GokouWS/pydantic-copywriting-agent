"""
Test script to check available Gemini models.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_available_models():
    """List all available Gemini models."""
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        return
    
    print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models
        models = genai.list_models()
        print("\nAvailable Gemini models:")
        for model in models:
            if "gemini" in model.name.lower() and "generateContent" in model.supported_generation_methods:
                print(f"- {model.name}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_available_models()
