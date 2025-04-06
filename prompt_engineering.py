from typing import List, Optional
from models import ContentRequest, ResearchResult, ContentType
from utils import (
    get_content_type_instructions,
    get_tone_instructions,
    get_audience_instructions,
)
from prompt_templates import (
    MASTER_COPYWRITING_SYSTEM_PROMPT,
    get_enhanced_prompt_template,
)
from direct_response import DirectResponseMarketing


def generate_copywriting_prompt(
    request: ContentRequest, research_results: Optional[List[ResearchResult]] = None
) -> str:
    """
    Generate a comprehensive prompt for the AI copywriting agent.

    Args:
        request: The content request parameters
        research_results: Optional research results to include

    Returns:
        A well-structured prompt for the AI model
    """
    # Use the master copywriting system prompt
    system_prompt = MASTER_COPYWRITING_SYSTEM_PROMPT

    # Content type specific instructions
    content_type_instructions = get_content_type_instructions(request.content_type)

    # Get enhanced prompt template for the content type
    enhanced_template = get_enhanced_prompt_template(request.content_type)

    # Tone instructions
    tone_instructions = get_tone_instructions(request.tone)

    # Audience instructions
    audience_instructions = get_audience_instructions(request.audience)

    # Construct the user prompt
    user_prompt = f"""
    # Content Creation Request

    ## Content Type:
    {request.content_type}

    ## Topic:
    {request.topic}

    ## Target Audience:
    {audience_instructions}

    ## Tone and Style:
    {tone_instructions}

    ## Content Structure and Approach:
    {content_type_instructions}

    ## Advanced Optimization Guidelines:
    {enhanced_template}

    ## Keywords to Include:
    {", ".join(request.keywords) if request.keywords else "No specific keywords provided"}

    ## Target Length:
    {f"Approximately {request.word_count} words" if request.word_count else "No specific length requirement"}
    """

    # Add custom instructions if provided
    if request.custom_instructions:
        user_prompt += f"""
        ## Additional Instructions:
        {request.custom_instructions}
        """

    # Add research results if available
    if research_results:
        research_section = """
        ## Research Findings:
        Use the following information to enhance your content with accurate and relevant details:
        """

        for i, result in enumerate(research_results, 1):
            research_section += f"""
            ### Source {i}: {result.title}
            - Source: {result.source}
            - URL: {result.url}
            - Summary: {result.snippet}
            """

        user_prompt += research_section

    # Get direct response marketing principles
    dr_principles = DirectResponseMarketing.get_principles()
    dr_ctr_techniques = DirectResponseMarketing.get_ctr_boosting_techniques()
    dr_aida_framework = DirectResponseMarketing.get_aida_framework()

    # Add direct response marketing section
    user_prompt += """
    ## Direct Response Marketing Principles:
    Incorporate these principles to maximize engagement and click-through rates:

    ### Core Principles:
    - Urgency: Create a sense of time limitation or scarcity
    - Specificity: Use specific numbers, timeframes, and results
    - Social Proof: Show that others have achieved results
    - Risk Reversal: Remove perceived risk with guarantees
    - Problem-Agitation-Solution: Clearly identify the problem, emphasize the pain, then present the solution
    - Clear CTA: Make the next step obvious and compelling

    ### AIDA Framework Implementation:
    - Attention: Use pattern interrupts, shocking statistics, or provocative questions
    - Interest: Present specific benefits and create information gaps
    - Desire: Paint a vivid picture of the after-state and overcome objections
    - Action: Use clear, direct command language with urgency elements

    ### CTR Boosting Techniques:
    - Use numbers and power words in headlines
    - Front-load benefits in the first sentence
    - Create information gaps that require clicking to resolve
    - Use bullet points for easy scanning
    - Keep paragraphs short (1-3 sentences maximum)
    - Include testimonials with specific results when appropriate
    - Leverage loss aversion (fear of missing out)
    - Test multiple headline variations
    """

    # Add final output instructions
    user_prompt += """
    ## Output Format:
    Please provide the complete content as requested, formatted appropriately for the content type.

    ## Important Guidelines:
    - Focus on providing value to the reader
    - Be original and avoid generic content
    - Use evidence and examples where appropriate
    - Ensure factual accuracy
    - Maintain a consistent tone throughout
    - Structure the content for easy readability
    - Include a compelling call-to-action that drives clicks
    - Optimize for high click-through rates using direct response principles
    """

    # Combine system and user prompts
    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    return full_prompt
