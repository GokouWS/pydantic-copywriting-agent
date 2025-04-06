"""
Simple test script to verify the copywriting agent works with Google Gemini.
"""

import os
from dotenv import load_dotenv
from models import ContentRequest, ContentType, ToneType, AudienceType
from agent import CopywritingAgent

# Load environment variables
load_dotenv()

def test_agent():
    """Test the copywriting agent with a simple request."""
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        print("Please set it in your .env file and try again.")
        return
    
    print("Initializing copywriting agent with Google Gemini...")
    
    try:
        # Initialize the agent
        agent = CopywritingAgent()
        
        # Create a simple content request
        request = ContentRequest(
            content_type=ContentType.BLOG_POST,
            topic="The Benefits of Artificial Intelligence in Content Creation",
            tone=ToneType.CONVERSATIONAL,
            audience=AudienceType.GENERAL,
            keywords=["AI", "content creation", "productivity", "creativity"],
            word_count=300,
            include_research=False  # Set to True to test research functionality
        )
        
        print(f"Generating content for topic: {request.topic}")
        print(f"Content type: {request.content_type}")
        print(f"Tone: {request.tone}")
        print(f"Target audience: {request.audience}")
        print("Generating content...")
        
        # Generate content
        response = agent.generate_content(request)
        
        print("\n" + "="*50)
        print("GENERATED CONTENT:")
        print("="*50)
        print(response.content)
        print("="*50)
        print(f"Model used: {response.metadata.get('model_used', 'Unknown')}")
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        print("Test failed.")

if __name__ == "__main__":
    test_agent()
