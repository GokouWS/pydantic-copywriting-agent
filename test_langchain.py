"""
Test script to verify the LangChain integration with Google Gemini.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()


def test_langchain_integration():
    """Test the LangChain integration with Google Gemini."""

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        return

    print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")

    try:
        # Initialize the LangChain model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )

        # Create messages
        # Note: SystemMessage is not directly supported, so we'll use only HumanMessage
        messages = [
            HumanMessage(
                content="You are a helpful assistant. Write a short poem about AI."
            )
        ]

        # Generate content
        print("Generating content...")
        response = llm.invoke(messages)

        print("\nResponse:")
        print(response.content)

        print("\nLangChain integration is working correctly!")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_langchain_integration()
