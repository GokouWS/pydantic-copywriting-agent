"""
Test script for the graph-based copywriting agent.
"""

import os
from dotenv import load_dotenv
from models import ContentRequest, ContentType, ToneType, AudienceType
from graph_agent import CopywritingGraphAgent

# Load environment variables
load_dotenv()

def test_graph_agent():
    """Test the graph-based copywriting agent with a simple request."""
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        print("Please set it in your .env file and try again.")
        return
    
    print("Initializing graph-based copywriting agent with Google Gemini 2.5 Pro...")
    
    try:
        # Initialize the agent
        agent = CopywritingGraphAgent()
        
        # Create a simple content request
        request = ContentRequest(
            content_type=ContentType.BLOG_POST,
            topic="How to Double Your Click-Through Rates with Direct Response Marketing",
            tone=ToneType.PERSUASIVE,
            audience=AudienceType.BUSINESS,
            keywords=["CTR optimization", "direct response", "copywriting", "A/B testing", "conversion"],
            word_count=500,
            include_research=True,  # Set to True to test research functionality
            custom_instructions="Focus on practical techniques that can be implemented immediately. Include specific examples of before/after CTR improvements."
        )
        
        print(f"Generating content for topic: {request.topic}")
        print(f"Content type: {request.content_type}")
        print(f"Tone: {request.tone}")
        print(f"Target audience: {request.audience}")
        print("Generating content using LangGraph workflow...")
        
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
        import traceback
        traceback.print_exc()
        print("Test failed.")

if __name__ == "__main__":
    test_graph_agent()
