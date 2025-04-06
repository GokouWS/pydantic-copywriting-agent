"""
Test script to verify the Google API key works.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_api_key():
    """Test the Google API key with a simple prompt."""
    
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
        print("\nAvailable models:")
        for model in models:
            if "generateContent" in model.supported_generation_methods:
                print(f"- {model.name}")
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-pro-2.5')
        response = model.generate_content("Hello, world!")
        
        print("\nTest response:")
        print(response.text)
        
        print("\nAPI key is working correctly!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_key()
