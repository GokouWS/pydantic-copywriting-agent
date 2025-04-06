"""
Direct test of the Google Gemini API without Streamlit.
"""

import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_direct_api():
    """Test the Google Gemini API directly."""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        return
    
    print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        print("Sending request to Gemini...")
        start_time = time.time()
        
        response = model.generate_content("Write a short paragraph about AI.")
        
        end_time = time.time()
        print(f"Response received in {end_time - start_time:.2f} seconds!")
        
        print("\nResponse:")
        print(response.text)
        
        print("\nDirect API test completed successfully!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_api()
