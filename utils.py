import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
from models import ResearchResult, ContentType, ToneType, AudienceType

load_dotenv()


def get_search_results(query: str, num_results: int = 5) -> List[ResearchResult]:
    """
    Search the web for relevant information using Brave Search API.

    Args:
        query: The search query
        num_results: Number of results to return

    Returns:
        List of search results
    """
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_SEARCH_API_KEY not found in environment variables")

    headers = {"Accept": "application/json", "X-Subscription-Token": api_key}

    params = {"q": query, "count": num_results}

    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search", headers=headers, params=params
    )

    if response.status_code != 200:
        raise Exception(f"Search API returned status code {response.status_code}")

    data = response.json()
    results = []

    for item in data.get("web", {}).get("results", []):
        results.append(
            ResearchResult(
                source=item.get("site", ""),
                title=item.get("title", ""),
                snippet=item.get("description", ""),
                url=item.get("url", ""),
            )
        )

    return results


def get_content_type_instructions(content_type: ContentType) -> str:
    """
    Get specific instructions based on content type.
    """
    instructions = {
        ContentType.BLOG_POST: """
            Create a high-converting blog post with:
            - A headline that uses numbers, power words, and creates curiosity
            - An engaging introduction that hooks the reader with a problem or surprising fact
            - Well-organized body with benefit-focused subheadings
            - Short paragraphs (1-3 sentences) for easy scanning
            - Bullet points to highlight key benefits or takeaways
            - Strategic use of bold text for important points
            - Information gaps that create curiosity and encourage continued reading
            - Multiple compelling CTAs throughout the content
            - Urgency elements that encourage immediate action
            - Social proof elements like statistics, testimonials, or case studies
            - A strong conclusion with a final, persuasive call-to-action
        """,
        ContentType.SOCIAL_MEDIA: """
            Create high-CTR social media content with:
            - A pattern-interrupting first line that stops scrolling
            - Concise, benefit-focused messaging that creates curiosity
            - Strategic use of emojis to draw attention to key points
            - Power words that trigger emotional responses
            - A clear, compelling call-to-action with urgency elements
            - Question-based engagement hooks that prompt responses
            - Social proof elements when appropriate
            - Appropriate hashtags that extend reach
            - Appropriate length for the platform with line breaks for scannability
            - A/B test suggestions for different headline approaches
        """,
        ContentType.EMAIL: """
            Create a high-converting email with:
            - A subject line that creates curiosity or promises specific value
            - A compelling preheader that extends the subject line promise
            - Personalized greeting and content when possible
            - An opening line that immediately engages with a question or bold statement
            - Short paragraphs (1-2 sentences) for easy mobile reading
            - Bullet points to highlight key benefits
            - Strategic use of bold and italics for emphasis
            - A clear, compelling primary CTA repeated 2-3 times
            - Urgency elements like limited time offers or deadlines
            - P.S. section that reinforces the main benefit or adds urgency
            - A/B test suggestions for different subject lines and CTAs
        """,
        ContentType.LANDING_PAGE: """
            Create a high-converting landing page with:
            - A headline that clearly communicates the unique value proposition
            - A subheadline that expands on the main benefit or addresses objections
            - Hero section with a clear, compelling primary CTA
            - Benefit-focused sections with specific outcomes (not features)
            - Bullet points that highlight key benefits with power words
            - Multiple strategically placed CTAs with action-oriented language
            - Trust indicators including testimonials with specific results
            - Social proof elements with numbers and statistics
            - Risk-reversal elements like guarantees or free trials
            - Urgency and scarcity elements that drive immediate action
            - FAQ section that preemptively addresses objections
            - Mobile-optimized layout suggestions for maximum conversion
            - A/B test suggestions for different value propositions and CTAs
        """,
        ContentType.PRODUCT_DESCRIPTION: """
            Create a compelling product description with:
            - Attention-grabbing headline
            - Clear explanation of what the product is
            - Emphasis on key features and benefits
            - Technical specifications where relevant
            - Sensory and emotional language
            - Clear call-to-action
        """,
        ContentType.AD_COPY: """
            Create persuasive ad copy with:
            - Attention-grabbing headline
            - Clear value proposition
            - Emotional triggers
            - Sense of urgency
            - Strong call-to-action
            - Appropriate length for the ad platform
        """,
        ContentType.PRESS_RELEASE: """
            Create a professional press release with:
            - Compelling headline
            - Dateline and location
            - Strong lead paragraph with the 5 Ws (who, what, when, where, why)
            - Relevant quotes from key stakeholders
            - Boilerplate company information
            - Contact information
        """,
        ContentType.CUSTOM: """
            Create custom content following best practices for:
            - Clear and engaging communication
            - Proper structure and flow
            - Appropriate tone and style
            - Compelling calls-to-action where needed
            - Relevant and accurate information
        """,
    }

    return instructions.get(content_type, instructions[ContentType.CUSTOM])


def get_tone_instructions(tone: ToneType) -> str:
    """
    Get specific instructions based on tone.
    """
    instructions = {
        ToneType.PROFESSIONAL: "Use formal language, industry terminology, and maintain a serious, authoritative voice.",
        ToneType.CONVERSATIONAL: "Write as if having a friendly conversation, using contractions, questions, and a warm, approachable style.",
        ToneType.ENTHUSIASTIC: "Use energetic language, exclamations, and convey excitement and passion about the topic.",
        ToneType.INFORMATIVE: "Focus on facts, clear explanations, and educational content without unnecessary embellishment.",
        ToneType.PERSUASIVE: "Use compelling arguments, rhetorical questions, and persuasive techniques to convince the reader.",
        ToneType.HUMOROUS: "Incorporate appropriate humor, wit, and a light-hearted approach to engage the reader.",
        ToneType.FORMAL: "Use proper grammar, avoid contractions, and maintain a sophisticated, academic tone.",
        ToneType.CASUAL: "Use relaxed language, slang (when appropriate), and a laid-back, friendly approach.",
    }

    return instructions.get(tone, instructions[ToneType.CONVERSATIONAL])


def get_audience_instructions(audience: AudienceType) -> str:
    """
    Get specific instructions based on audience type.
    """
    instructions = {
        AudienceType.GENERAL: "Write for a broad audience with varied knowledge levels, avoiding jargon and complex concepts without explanation.",
        AudienceType.TECHNICAL: "Use technical terminology, detailed explanations, and assume specialized knowledge in the subject area.",
        AudienceType.BUSINESS: "Focus on business value, ROI, and strategic implications using professional business language.",
        AudienceType.CONSUMER: "Emphasize benefits over features, use accessible language, and focus on how the product/service improves daily life.",
        AudienceType.EXPERT: "Use advanced terminology, in-depth analysis, and assume high-level understanding of the subject matter.",
        AudienceType.BEGINNER: "Provide clear explanations, avoid jargon, use analogies, and assume no prior knowledge of the subject.",
        AudienceType.YOUTH: "Use simple language, engaging examples, and a more energetic tone appropriate for younger audiences.",
        AudienceType.SENIOR: "Use clear, straightforward language, avoid trendy terms, and consider accessibility in your communication.",
    }

    return instructions.get(audience, instructions[AudienceType.GENERAL])
