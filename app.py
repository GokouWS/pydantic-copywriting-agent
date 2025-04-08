"""
AI Copywriting Agent with Google Gemini 2.0 Pro.

This application provides:
1. Content generation with direct-response marketing principles
2. SEO analysis and optimization
3. Social media content optimization
4. Video analysis for Instagram Reels and YouTube Shorts
"""

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import tempfile

# Import from our modular structure
from src.models import (
    ContentType,
    ToneType,
    AudienceType,
    SocialPlatform,
    VideoContentType,
    ContentRequest,
    VideoAnalysisRequest,
)
from src.api import GeminiAPI, BraveSearchAPI
from src.analysis import SEOAnalyzer
from src.analysis.improved_video_analyzer import ImprovedVideoAnalyzer
from src.ui import (
    display_header,
    display_sidebar,
    display_content_form,
    display_video_form,
    display_seo_analysis,
    display_enhanced_seo_analysis,
    display_video_analysis_results,
)

# Load environment variables
load_dotenv()

# Initialize session state
if "content_history" not in st.session_state:
    st.session_state.content_history = []

# Page configuration
st.set_page_config(
    page_title="AI Copywriting & Social Media Agent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize APIs and analyzers
@st.cache_resource
def initialize_apis():
    """Initialize API clients."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error(
            "GOOGLE_API_KEY not found in environment variables. Please set it in your .env file."
        )
        st.stop()

    return {
        "gemini_api": GeminiAPI(api_key),
        "brave_api": BraveSearchAPI(),
        "seo_analyzer": SEOAnalyzer(),
        "video_analyzer": ImprovedVideoAnalyzer(),
    }


apis = initialize_apis()


def main():
    """Main application function."""
    # Display header and sidebar
    display_header()
    sidebar_options = display_sidebar()

    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Content Generation", "Video Analysis"])

    with tab1:
        # Content generation tab
        handle_content_generation(sidebar_options["use_advanced_seo"])

    with tab2:
        # Video analysis tab
        handle_video_analysis()


def handle_content_generation(use_advanced_seo):
    """Handle content generation functionality."""
    # Display content form
    form_data = display_content_form()

    if form_data["submit"]:
        # Show progress
        with st.status("Generating content...", expanded=True) as status:
            if form_data["include_research"]:
                st.write("Researching relevant information...")

            st.write("Crafting your content...")
            st.write("Enhancing with direct-response marketing principles...")
            st.write("Analyzing and optimizing for SEO...")

            try:
                # Create the prompt
                prompt = create_content_prompt(form_data)

                # Generate content
                content = apis["gemini_api"].generate_content(prompt)

                # Add to history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                metadata = {
                    "content_type": form_data["content_type"],
                    "topic": form_data["topic"],
                    "tone": form_data["tone"],
                    "audience": form_data["audience"],
                    "word_count": form_data["word_count"],
                    "model_used": "models/gemini-2.0-pro-exp-02-05",
                }
                st.session_state.content_history.append((timestamp, metadata))

                status.update(
                    label="Content generated successfully!",
                    state="complete",
                    expanded=False,
                )
            except Exception as e:
                st.error(f"Error generating content: {e}")
                status.update(
                    label="Error generating content", state="error", expanded=False
                )
                st.stop()

        # Display generated content
        st.markdown("## Generated Content")

        # Display metadata
        with st.expander("Content Metadata", expanded=False):
            st.json(metadata)

        # Perform SEO analysis
        if use_advanced_seo:
            # Use enhanced SEO analysis with free SEO tools
            seo_results = apis["seo_analyzer"].analyze(content, form_data["keywords"])

            # Add SEO score to metadata
            metadata["seo_score"] = seo_results["overall_score"]
            metadata["using_advanced_seo"] = True

            # Display enhanced SEO analysis
            display_enhanced_seo_analysis(seo_results)
        else:
            # Use basic SEO analysis
            seo_results = apis["seo_analyzer"].analyze(content, form_data["keywords"])

            # Add SEO score to metadata
            metadata["seo_score"] = seo_results["overall_score"]

            # Display basic SEO analysis
            display_seo_analysis(seo_results)

        # Display the content
        st.markdown("### Content Preview")
        st.markdown(content)

        # Export options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save as Markdown"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{form_data['content_type']}_{timestamp}.md"
                with open(filename, "w") as f:
                    f.write(content)
                st.success(f"Content saved to {filename}")

        with col2:
            if st.button("Copy to Clipboard"):
                st.code(content)
                st.success("Content copied to clipboard (use the copy button above)")


def handle_video_analysis():
    """Handle video analysis functionality."""
    # Display video form
    form_data = display_video_form()

    if form_data["submit"]:
        if not form_data["video_path"]:
            st.error("Please upload a video file.")
            return

        # Show progress
        with st.status("Analyzing video...", expanded=True) as status:
            st.write("Extracting video frames...")
            st.write("Analyzing visual content...")
            st.write("Generating captions and hashtags...")

            try:
                # Create video analyzer
                video_analyzer = ImprovedVideoAnalyzer(
                    gemini_api=apis["gemini_api"], brave_api=apis["brave_api"]
                )

                # Analyze video
                result = video_analyzer.analyze_video(
                    video_path=form_data["video_path"],
                    content_type=VideoContentType(form_data["content_type"]),
                    keywords=form_data["keywords"],
                    max_frames=5,
                )

                status.update(
                    label="Video analysis completed successfully!",
                    state="complete",
                    expanded=False,
                )
            except Exception as e:
                st.error(f"Error analyzing video: {e}")
                status.update(
                    label="Error analyzing video", state="error", expanded=False
                )
                st.stop()
            finally:
                # Clean up temporary file
                if os.path.exists(form_data["video_path"]):
                    os.unlink(form_data["video_path"])

        # Display video analysis results
        display_video_analysis_results(result)


def create_content_prompt(form_data):
    """Create a prompt for content generation using advanced prompting techniques."""

    # Define the persona based on content type
    persona = {
        "blog_post": "an expert content strategist with 10+ years of experience in SEO optimization",
        "social_media": "a social media marketing expert who specializes in viral content creation",
        "email": "an email marketing specialist with expertise in high-conversion campaigns",
        "landing_page": "a conversion rate optimization expert who specializes in landing page design",
        "product_description": "a professional copywriter who specializes in compelling product descriptions",
        "ad_copy": "an advertising expert who creates high-converting ad campaigns",
        "press_release": "a PR professional with experience writing for major publications",
        "custom": "a professional copywriter with expertise in various content formats",
    }.get(form_data["content_type"], "a professional copywriter")

    # Create a more specific and detailed prompt using best practices
    prompt = f"""
    # Content Creation Request

    ## Your Role:
    You are {persona}. Your task is to create {form_data["content_type"]} content that achieves the following objectives:
    1. Engages the target audience effectively
    2. Incorporates direct response marketing principles
    3. Optimizes for search engines using the provided keywords
    4. Drives specific actions from the reader

    ## Content Specifications:
    - **Type:** {form_data["content_type"]}
    - **Topic:** {form_data["topic"]}
    - **Target Audience:** {form_data["audience"]}
    - **Tone and Style:** {form_data["tone"]}
    - **Primary Keywords:** {", ".join(form_data["keywords"]) if form_data["keywords"] else "No specific keywords provided"}
    - **Length:** Approximately {form_data["word_count"]} words
    {f"- **Platform:** {form_data['social_platform']}" if form_data.get("social_platform") else ""}

    {f"## Additional Context:\\n{form_data['custom_instructions']}" if form_data.get("custom_instructions") else ""}

    ## Direct Response Marketing Framework:
    Follow this structured approach to maximize engagement and conversions:

    1. **Problem Identification (25% of content)**
       - Clearly articulate the specific problem or pain point the audience faces
       - Use data, statistics, or relatable scenarios to validate the problem
       - Create emotional resonance by showing understanding of their frustration

    2. **Solution Presentation (40% of content)**
       - Present your solution logically, addressing each aspect of the problem
       - Highlight unique benefits using the AIDA framework (Attention, Interest, Desire, Action)
       - Include specific examples, case studies, or testimonials as evidence

    3. **Objection Handling (15% of content)**
       - Anticipate and address potential objections or concerns
       - Use risk reversal techniques (guarantees, social proof, etc.)
       - Create urgency through limited-time offers or scarcity elements

    4. **Clear Call-to-Action (20% of content)**
       - Provide explicit, compelling next steps
       - Use action-oriented language that creates momentum
       - Reinforce the primary benefit of taking action

    ## SEO Optimization Requirements:
    - Include primary keywords in the title, first paragraph, and at least one H2 heading
    - Maintain keyword density between 0.5% and 2.5% (not too sparse, not stuffed)
    - Structure content with proper heading hierarchy (H1 → H2 → H3)
    - Keep paragraphs short (3-4 sentences maximum) for improved readability
    - Include at least one relevant statistic or data point that supports your main argument
    - For blog posts: suggest 2-3 internal linking opportunities

    ## Content Structure:
    1. **Compelling headline** that includes primary keyword and creates curiosity
    2. **Strong opening paragraph** that hooks the reader and establishes relevance
    3. **Well-organized body** with clear headings and logical flow
    4. **Persuasive conclusion** with a specific, action-oriented CTA

    ## Do NOT include:
    - Generic or vague statements without supporting evidence
    - Excessive jargon that might confuse the target audience
    - Overpromising or making claims that cannot be substantiated
    - Walls of text without proper formatting and structure

    ## Output Format:
    Provide the complete content as requested, formatted appropriately for the content type, with proper Markdown formatting for headings, lists, and emphasis.

    ## Process Explanation:
    Before writing the content, briefly outline your approach and how you'll incorporate the direct response marketing principles and SEO requirements. Then proceed with creating the full content.
    """

    return prompt


def create_video_analysis_prompt(form_data, content_type):
    """Create an improved prompt for video analysis using advanced prompting techniques."""

    # Define the persona based on content type
    persona = {
        "instagram_reel": "a social media strategist specializing in Instagram growth with 8+ years of experience",
        "youtube_short": "a YouTube optimization expert who has helped creators reach millions of views",
        "tiktok": "a TikTok content strategist who understands viral trends and audience engagement",
    }.get(content_type.value, "a social media content expert")

    # Create platform-specific instructions
    platform_instructions = {
        "instagram_reel": """
        - Create a caption that's engaging but concise (max 2200 characters)
        - Focus on storytelling elements that create emotional connection
        - Include a question or call-to-action to boost comments
        - Suggest 20-30 hashtags organized by popularity (mix of broad, niche, and trending)
        - Recommend optimal posting times based on content theme
        """,
        "youtube_short": """
        - Create an attention-grabbing title (max 60 characters)
        - Write a description that front-loads keywords (max 300 characters)
        - Include 3-5 highly relevant hashtags
        - Suggest end screens and cards to drive further engagement
        - Recommend related video ideas to create a content series
        """,
        "tiktok": """
        - Create a short, punchy caption with strong hook
        - Include 3-5 trending hashtags plus 2-3 niche hashtags
        - Suggest trending sounds that could complement the video
        - Recommend follow-up content ideas to boost profile growth
        - Include ideas for text overlay to improve retention
        """,
    }.get(content_type.value, "")

    # Create a more specific and detailed prompt using best practices
    prompt = f"""
    # Video Content Analysis Request

    ## Your Role:
    You are {persona}. Your task is to analyze the provided video frames and create optimized content that will maximize engagement, reach, and conversion for {content_type.value}.

    ## Video Content Specifications:
    - **Platform:** {content_type.value}
    - **Keywords/Topics:** {", ".join(form_data["keywords"]) if form_data["keywords"] else "No specific keywords provided"}
    - **Target Caption Length:** {form_data["caption_length"]} characters
    {f"- **Additional Context:** {form_data['custom_instructions']}" if form_data.get("custom_instructions") else ""}

    ## Platform-Specific Requirements:
    {platform_instructions}

    ## Analysis Process:
    1. First, carefully analyze the video frames to understand:
       - The main subject/focus of the video
       - The apparent action or activity taking place
       - The mood, tone, and aesthetic of the content
       - Any text or recognizable elements visible
       - The likely target audience based on visual cues

    2. Based on your analysis, create:
       - A strategic caption that will drive engagement
       - Relevant hashtags organized by reach potential
       - Specific recommendations to improve performance

    ## Engagement Optimization:
    - Include pattern interrupts or curiosity hooks to stop the scroll
    - Create a sense of authenticity and relatability
    - Use emotional triggers appropriate to the content
    - Incorporate trending elements without forcing irrelevant content
    - Suggest ways to encourage shares, saves, and comments

    ## Output Format:
    Structure your response in the following format:

    **VIDEO ANALYSIS:**
    [Provide a brief analysis of what you observe in the video frames]

    **CAPTION:**
    [The complete caption, optimized for the platform]

    **HASHTAGS:**
    [List of recommended hashtags, organized by category]

    **PERFORMANCE RECOMMENDATIONS:**
    [5 specific, actionable recommendations to improve engagement]

    ## Important Guidelines:
    - Be specific and actionable in your recommendations
    - Avoid generic advice that could apply to any video
    - Consider current platform algorithm preferences
    - Focus on authentic engagement rather than gimmicks
    - Ensure all suggestions align with the actual video content
    """

    return prompt


if __name__ == "__main__":
    main()
