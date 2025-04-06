import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

from models import ContentRequest, ContentResponse, ResearchResult
from prompt_engineering import generate_copywriting_prompt
from utils import get_search_results

load_dotenv()


class CopywritingAgent:
    """
    AI agent for generating high-quality copywriting content.
    """

    def __init__(self, model_name: str = "gemini-2.0-pro-exp"):
        """
        Initialize the copywriting agent.

        Args:
            model_name: The Google Gemini model to use
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )

    def _perform_research(
        self, request: ContentRequest
    ) -> Optional[List[ResearchResult]]:
        """
        Perform web research based on the content request.

        Args:
            request: The content request

        Returns:
            List of research results or None if research is disabled
        """
        if not request.include_research:
            return None

        # Create search queries based on the topic and keywords
        search_query = f"{request.topic}"
        if request.keywords:
            search_query += f" {' '.join(request.keywords)}"

        # Add content type for more specific results
        search_query += f" {request.content_type} writing tips"

        try:
            return get_search_results(search_query)
        except Exception as e:
            print(f"Error performing research: {e}")
            return None

    def generate_content(self, request: ContentRequest) -> ContentResponse:
        """
        Generate content based on the request parameters.

        Args:
            request: The content request parameters

        Returns:
            Generated content and metadata
        """
        # Perform research if enabled
        research_results = self._perform_research(request)

        # Generate the prompt
        prompt = generate_copywriting_prompt(request, research_results)

        # Call the language model
        messages = [
            SystemMessage(content=prompt.split("\n\n")[0]),  # System prompt
            HumanMessage(content="\n\n".join(prompt.split("\n\n")[1:])),  # User prompt
        ]

        response = self.llm.invoke(messages)

        # Create and return the content response
        return ContentResponse(
            content=response.content,
            metadata={
                "content_type": request.content_type,
                "topic": request.topic,
                "tone": request.tone,
                "audience": request.audience,
                "word_count": request.word_count,
                "model_used": self.llm.model,
            },
            research_results=research_results,
        )
