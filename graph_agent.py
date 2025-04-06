"""
Graph-based implementation of the copywriting agent using LangGraph.
"""

import os
from typing import Dict, List, TypedDict, Annotated, Optional, Any, Tuple, Union
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from models import (
    ContentRequest,
    ContentResponse,
    ResearchResult,
    ContentType,
    ToneType,
    AudienceType,
)
from prompt_engineering import generate_copywriting_prompt
from utils import get_search_results
from direct_response import DirectResponseMarketing
from seo_analysis import SEOAnalyzer

# Load environment variables
load_dotenv()


# Define state schema
class AgentState(TypedDict):
    """State for the copywriting agent workflow."""

    content_request: ContentRequest
    research_results: Optional[List[ResearchResult]]
    prompt: Optional[str]
    content: Optional[str]
    enhanced_content: Optional[str]
    seo_analysis: Optional[Dict[str, Any]]
    seo_optimized_content: Optional[str]
    metadata: Dict[str, Any]
    status: str
    error: Optional[str]


# Define node functions
def initialize_state(content_request: ContentRequest) -> AgentState:
    """
    Initialize the agent state with the content request.

    Args:
        content_request: The content request parameters

    Returns:
        Initial agent state
    """
    return AgentState(
        content_request=content_request,
        research_results=None,
        prompt=None,
        content=None,
        enhanced_content=None,
        seo_analysis=None,
        seo_optimized_content=None,
        metadata={
            "content_type": content_request.content_type,
            "topic": content_request.topic,
            "tone": content_request.tone,
            "audience": content_request.audience,
            "word_count": content_request.word_count,
            "model_used": "gemini-1.5-pro-latest",
        },
        status="initialized",
        error=None,
    )


def perform_research(state: AgentState) -> Dict[str, Any]:
    """
    Perform web research based on the content request.

    Args:
        state: Current agent state

    Returns:
        Updated state with research results
    """
    print("\nStarting research phase...")
    try:
        content_request = state["content_request"]

        # Skip research if not requested
        if not content_request.include_research:
            return {"research_results": None, "status": "research_skipped"}

        # Create search queries based on the topic and keywords
        search_query = f"{content_request.topic}"
        if content_request.keywords:
            search_query += f" {' '.join(content_request.keywords)}"

        # Add content type for more specific results
        search_query += f" {content_request.content_type} writing tips"

        # Perform the search
        research_results = get_search_results(search_query)

        return {"research_results": research_results, "status": "research_completed"}
    except Exception as e:
        return {"research_results": None, "status": "research_failed", "error": str(e)}


def generate_prompt(state: AgentState) -> Dict[str, Any]:
    """
    Generate the prompt for the AI model.

    Args:
        state: Current agent state

    Returns:
        Updated state with generated prompt
    """
    print("\nGenerating prompt...")
    try:
        content_request = state["content_request"]
        research_results = state["research_results"]

        # Generate the prompt
        prompt = generate_copywriting_prompt(content_request, research_results)

        return {"prompt": prompt, "status": "prompt_generated"}
    except Exception as e:
        return {"prompt": None, "status": "prompt_generation_failed", "error": str(e)}


def generate_content(state: AgentState) -> Dict[str, Any]:
    """
    Generate content using the AI model.

    Args:
        state: Current agent state

    Returns:
        Updated state with generated content
    """
    print("\nGenerating content...")
    try:
        prompt = state["prompt"]

        # Initialize the AI model
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )

        # Combine the prompt into a single message
        # Note: SystemMessage is not directly supported by the Google Gemini integration

        # Call the language model
        messages = [HumanMessage(content=prompt)]

        response = llm.invoke(messages)

        return {
            "content": response.content,
            "status": "content_generated",
            "metadata": {**state["metadata"], "model_used": llm.model},
        }
    except Exception as e:
        return {"content": None, "status": "content_generation_failed", "error": str(e)}


def apply_direct_response_principles(state: AgentState) -> Dict[str, Any]:
    """
    Apply direct response marketing principles to enhance the content.

    Args:
        state: Current agent state

    Returns:
        Updated state with enhanced content
    """
    try:
        content = state["content"]
        content_request = state["content_request"]

        # Get direct response marketing principles
        dr_principles = DirectResponseMarketing.get_principles()
        dr_ctr_techniques = DirectResponseMarketing.get_ctr_boosting_techniques()

        # Initialize the AI model for enhancement
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )

        # Create enhancement prompt
        enhancement_prompt = f"""
        # Direct Response Enhancement

        ## Original Content:
        {content}

        ## Content Type:
        {content_request.content_type}

        ## Enhancement Task:
        Enhance the above content using direct response marketing principles to maximize click-through rates.
        Focus on:

        1. Creating compelling headlines that drive clicks
        2. Adding urgency and scarcity elements
        3. Strengthening calls-to-action
        4. Incorporating social proof
        5. Using power words and emotional triggers
        6. Implementing the AIDA framework (Attention, Interest, Desire, Action)
        7. Creating information gaps that require clicking to resolve
        8. Using specific numbers and data points to increase credibility

        ## Important:
        - Maintain the original topic and purpose
        - Keep the same general structure
        - Preserve key information and facts
        - Ensure the tone matches {content_request.tone}
        - Target the content for {content_request.audience} audience

        ## Output:
        Provide only the enhanced content without explanations.
        """

        # Call the language model
        messages = [HumanMessage(content=enhancement_prompt)]

        response = llm.invoke(messages)

        return {"enhanced_content": response.content, "status": "content_enhanced"}
    except Exception as e:
        return {
            "enhanced_content": state["content"],  # Fall back to original content
            "status": "enhancement_failed",
            "error": str(e),
        }


def analyze_seo(state: AgentState) -> Dict[str, Any]:
    """
    Analyze content for SEO optimization.

    Args:
        state: Current agent state

    Returns:
        Updated state with SEO analysis
    """
    try:
        content = state["enhanced_content"] or state["content"]
        if not content:
            return {
                "seo_analysis": None,
                "status": "seo_analysis_skipped",
                "error": "No content available for SEO analysis",
            }

        content_request = state["content_request"]
        keywords = content_request.keywords or []
        content_type = content_request.content_type

        # Initialize SEO analyzer
        seo_analyzer = SEOAnalyzer()

        # Perform SEO analysis
        analysis_results = seo_analyzer.analyze(
            content=content, target_keywords=keywords, content_type=content_type
        )

        return {"seo_analysis": analysis_results, "status": "seo_analysis_completed"}
    except Exception as e:
        return {"seo_analysis": None, "status": "seo_analysis_failed", "error": str(e)}


def optimize_seo(state: AgentState) -> Dict[str, Any]:
    """
    Optimize content for SEO based on analysis.

    Args:
        state: Current agent state

    Returns:
        Updated state with SEO-optimized content
    """
    try:
        content = state["enhanced_content"] or state["content"]
        seo_analysis = state["seo_analysis"]

        if not content or not seo_analysis:
            return {
                "seo_optimized_content": content,  # Return original content
                "status": "seo_optimization_skipped",
            }

        # Skip optimization if SEO score is already high
        if seo_analysis["overall_score"] >= 85:
            return {
                "seo_optimized_content": content,
                "status": "seo_optimization_skipped",
                "metadata": {
                    **state["metadata"],
                    "seo_score": seo_analysis["overall_score"],
                },
            }

        # Initialize SEO analyzer
        seo_analyzer = SEOAnalyzer()

        # Generate prompt for SEO improvement
        seo_prompt = seo_analyzer.get_seo_improvement_prompt(seo_analysis, content)

        # Initialize the AI model
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.7,
            google_api_key=api_key,
            convert_system_message_to_human=True,
        )

        # Call the language model
        messages = [HumanMessage(content=seo_prompt)]
        response = llm.invoke(messages)

        return {
            "seo_optimized_content": response.content,
            "status": "seo_optimization_completed",
            "metadata": {
                **state["metadata"],
                "seo_score": seo_analysis["overall_score"],
            },
        }
    except Exception as e:
        return {
            "seo_optimized_content": state["enhanced_content"]
            or state["content"],  # Fall back to original content
            "status": "seo_optimization_failed",
            "error": str(e),
        }


def should_refine_content(state: AgentState) -> str:
    """
    Determine if content needs further refinement.

    Args:
        state: Current agent state

    Returns:
        Next step in the workflow
    """
    # For now, we'll just do a single pass
    # In a more advanced implementation, this could analyze the content
    # and decide if it needs further refinement
    return "complete"


class CopywritingGraphAgent:
    """
    Graph-based AI agent for generating high-quality copywriting content.
    """

    def __init__(self):
        """Initialize the graph-based copywriting agent."""
        # Build the workflow graph
        self.workflow = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build the workflow graph.

        Returns:
            Compiled workflow graph
        """
        # Create the graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("research", perform_research)
        workflow.add_node("generate_prompt", generate_prompt)
        workflow.add_node("generate_content", generate_content)
        workflow.add_node("enhance_content", apply_direct_response_principles)
        workflow.add_node("analyze_seo", analyze_seo)
        workflow.add_node("optimize_seo", optimize_seo)

        # Add edges
        workflow.add_edge("research", "generate_prompt")
        workflow.add_edge("generate_prompt", "generate_content")
        workflow.add_edge("generate_content", "enhance_content")
        workflow.add_edge("enhance_content", "analyze_seo")
        workflow.add_edge("analyze_seo", "optimize_seo")

        # Add conditional edge for potential refinement loop
        workflow.add_conditional_edges(
            "optimize_seo",
            should_refine_content,
            {"refine": "generate_content", "complete": END},
        )

        # Set the entry point
        workflow.set_entry_point("research")

        # Compile the graph
        return workflow.compile()

    def generate_content(self, request: ContentRequest) -> ContentResponse:
        """
        Generate content based on the request parameters.

        Args:
            request: The content request parameters

        Returns:
            Generated content and metadata
        """
        print(f"\nStarting content generation for topic: {request.topic}")
        print(f"Content type: {request.content_type}")
        print(f"Using model: gemini-1.5-pro-latest")
        # Initialize the state
        initial_state = initialize_state(request)

        # Execute the workflow
        try:
            final_state = self.workflow.invoke(initial_state)

            # Print debug information
            print("\nWorkflow execution completed.")
            print(f"Content available: {bool(final_state.get('content'))}")
            print(
                f"Enhanced content available: {bool(final_state.get('enhanced_content'))}"
            )
            print(
                f"SEO optimized content available: {bool(final_state.get('seo_optimized_content'))}"
            )

            # Add SEO score to metadata if available
            metadata = final_state["metadata"]
            if final_state.get("seo_analysis"):
                metadata["seo_score"] = final_state["seo_analysis"]["overall_score"]
                print(f"SEO score: {metadata['seo_score']}")

            # Get the final content
            final_content = (
                final_state.get("seo_optimized_content")
                or final_state.get("enhanced_content")
                or final_state.get("content")
                or ""
            )

            print(f"Final content length: {len(final_content)}")
            if not final_content:
                print("WARNING: No content was generated!")

            # Create and return the content response
            return ContentResponse(
                content=final_content,
                metadata=metadata,
                research_results=final_state.get("research_results"),
            )
        except Exception as e:
            import traceback

            print(f"Error in workflow execution: {e}")
            traceback.print_exc()
            raise
