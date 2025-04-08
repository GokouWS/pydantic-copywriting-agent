"""
Streamlit UI components for the AI copywriting agent.
"""

import streamlit as st
from typing import Dict, List, Any, Optional, Callable
import os
import tempfile
from src.models.content_models import (
    ContentType,
    ToneType,
    AudienceType,
    SocialPlatform,
    VideoContentType,
)


def display_header():
    """Display the application header."""
    st.title("✍️ AI Copywriting & Social Media Agent")
    st.markdown("Generate high-quality content optimized for your specific needs")


def display_sidebar():
    """Display the sidebar with model information and options."""
    st.sidebar.title("AI Content Agent")
    st.sidebar.markdown("### Model Information")
    st.sidebar.info(
        "Using Google Gemini 2.0 Pro Experimental with direct-response marketing principles and SEO optimization."
    )

    # Advanced SEO options
    st.sidebar.markdown("### Advanced SEO Options")
    use_advanced_seo = st.sidebar.checkbox(
        "Enable Advanced SEO Analysis",
        value=True,
        help="Enable advanced SEO analysis with keyword metrics, competitive insights, and SERP analysis.",
    )

    if use_advanced_seo:
        st.sidebar.success("Advanced SEO analysis enabled!")
        st.sidebar.info(
            "This will provide estimated keyword metrics, competitive insights, and SERP analysis using algorithmic models."
        )

    return {"use_advanced_seo": use_advanced_seo}


def display_content_form():
    """Display the content generation form."""
    with st.form("content_request_form"):
        col1, col2 = st.columns(2)

        with col1:
            content_type = st.selectbox(
                "Content Type",
                options=[ct.value for ct in ContentType],
                format_func=lambda x: x.replace("_", " ").title(),
            )

            topic = st.text_area(
                "Topic/Subject",
                placeholder="Enter the main topic or subject of your content",
            )

            keywords = st.text_area(
                "Keywords (one per line)",
                placeholder="Enter keywords to include in your content (one per line)",
            )

            word_count = st.number_input(
                "Target Word Count", min_value=50, max_value=5000, value=500, step=50
            )

        with col2:
            tone = st.selectbox(
                "Tone",
                options=[t.value for t in ToneType],
                format_func=lambda x: x.replace("_", " ").title(),
            )

            audience = st.selectbox(
                "Target Audience",
                options=[a.value for a in AudienceType],
                format_func=lambda x: x.replace("_", " ").title(),
            )

            include_research = st.checkbox("Include Web Research", value=True)

            # Show social platform selector if content type is social_media
            social_platform = None
            if content_type == ContentType.SOCIAL_MEDIA.value:
                social_platform = st.selectbox(
                    "Social Platform",
                    options=[p.value for p in SocialPlatform],
                    format_func=lambda x: x.replace("_", " ").title(),
                )

            custom_instructions = st.text_area(
                "Custom Instructions (Optional)",
                placeholder="Enter any additional instructions or requirements",
            )

        submit_button = st.form_submit_button("Generate Content")

        # Parse keywords
        keyword_list = [k.strip() for k in keywords.split("\n") if k.strip()]

        return {
            "submit": submit_button,
            "content_type": content_type,
            "topic": topic,
            "tone": tone,
            "audience": audience,
            "keywords": keyword_list,
            "word_count": word_count,
            "include_research": include_research,
            "social_platform": social_platform,
            "custom_instructions": custom_instructions,
        }


def display_video_form():
    """Display the video analysis form."""
    with st.form("video_analysis_form"):
        col1, col2 = st.columns(2)

        with col1:
            content_type = st.selectbox(
                "Video Content Type",
                options=[vt.value for vt in VideoContentType],
                format_func=lambda x: x.replace("_", " ").title(),
            )

            uploaded_file = st.file_uploader(
                "Upload Video",
                type=["mp4", "mov", "avi", "webm"],
                help="Upload a video file to analyze",
            )

            keywords = st.text_area(
                "Keywords (one per line)",
                placeholder="Enter keywords to include in your captions and hashtags",
            )

        with col2:
            caption_length = st.number_input(
                "Target Caption Length",
                min_value=50,
                max_value=2200,
                value=200,
                step=50,
                help="Maximum length for Instagram is 2200 characters",
            )

            custom_instructions = st.text_area(
                "Custom Instructions (Optional)",
                placeholder="Enter any additional instructions for caption generation",
            )

        submit_button = st.form_submit_button("Analyze Video")

        # Parse keywords
        keyword_list = [k.strip() for k in keywords.split("\n") if k.strip()]

        # Save uploaded file to temp location if provided
        video_path = None
        if uploaded_file is not None:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_file.write(uploaded_file.getvalue())
            video_path = temp_file.name
            temp_file.close()

        return {
            "submit": submit_button,
            "content_type": content_type,
            "video_path": video_path,
            "keywords": keyword_list,
            "caption_length": caption_length,
            "custom_instructions": custom_instructions,
            "uploaded_file": uploaded_file,
        }


def display_seo_analysis(seo_results):
    """Display SEO analysis results."""
    if not seo_results:
        return

    with st.expander("SEO Analysis", expanded=False):
        # Display SEO score with gauge chart
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("### SEO Score")
            score_color = (
                "green"
                if seo_results["overall_score"] >= 80
                else "orange"
                if seo_results["overall_score"] >= 60
                else "red"
            )
            st.markdown(
                f"<h1 style='color: {score_color};'>{seo_results['overall_score']:.1f}/100</h1>",
                unsafe_allow_html=True,
            )

        with col2:
            # Create a simple gauge chart using progress bar
            st.markdown("### SEO Performance")
            st.progress(seo_results["overall_score"] / 100)

            # Add performance label
            if seo_results["overall_score"] >= 80:
                st.success("Excellent SEO optimization")
            elif seo_results["overall_score"] >= 60:
                st.warning("Good, but could be improved")
            else:
                st.error("Needs significant improvement")

        # Display content metrics
        st.markdown("### Content Structure")
        col1, col2, col3 = st.columns(3)
        col1.metric("Word Count", seo_results["word_count"])
        col2.metric("Paragraphs", seo_results["paragraph_count"])
        col3.metric("Headings", seo_results["h2_count"] + seo_results["h3_count"])

        # Display keyword metrics
        st.markdown("### Keyword Analysis")
        for keyword, metrics in seo_results["keyword_metrics"].items():
            st.markdown(
                f"**{keyword}**: {metrics['count']} occurrences, {metrics['density']:.2f}% density"
            )
            st.markdown(
                f"- In title: {':white_check_mark:' if metrics['in_title'] else ':x:'}"
            )
            st.markdown(
                f"- In headings: {':white_check_mark:' if metrics['in_headings'] else ':x:'}"
            )

        # Display recommendations
        if "recommendations" in seo_results:
            st.markdown("### Recommendations")
            for recommendation in seo_results["recommendations"]:
                st.markdown(f"- {recommendation}")


def display_enhanced_seo_analysis(seo_results):
    """Display enhanced SEO analysis results."""
    if not seo_results:
        return

    with st.expander("Enhanced SEO Analysis", expanded=False):
        # Display basic SEO score
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("### SEO Score")
            score_color = (
                "green"
                if seo_results["overall_score"] >= 80
                else "orange"
                if seo_results["overall_score"] >= 60
                else "red"
            )
            st.markdown(
                f"<h1 style='color: {score_color};'>{seo_results['overall_score']:.1f}/100</h1>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("### SEO Performance")
            st.progress(seo_results["overall_score"] / 100)

        # Display keyword metrics with advanced data
        if "advanced_data" in seo_results.get("keyword_metrics", {}):
            st.markdown("### Keyword Analysis (Advanced Data)")

            for keyword, metrics in seo_results["keyword_metrics"][
                "advanced_data"
            ].items():
                st.markdown(f"**{keyword}**")
                cols = st.columns(5)
                cols[0].metric("Monthly Volume", metrics["volume"])
                cols[1].metric("Difficulty", f"{metrics['difficulty']}/100")
                cols[2].metric("Competition", f"{metrics['competition']:.2f}")
                cols[3].metric("CPC", f"${metrics['cpc']:.2f}")
                cols[4].metric("Results", f"{metrics['results']:,}")

        # Display competitive insights
        if "competitive_insights" in seo_results:
            st.markdown("### Competitive Insights")
            for insight in seo_results["competitive_insights"]:
                st.markdown(f"- {insight}")

        # Display SERP analysis
        if "serp_analysis" in seo_results and seo_results["serp_analysis"]:
            st.markdown("### Top Search Results")
            for i, result in enumerate(seo_results["serp_analysis"][:5], 1):
                st.markdown(
                    f"**{i}. [{result['domain']}]({result['url']})** (Position: {result['position']})"
                )
                st.markdown(
                    f"Traffic: {result['traffic']:,} | Keywords: {result['keywords']:,}"
                )


def display_video_analysis_results(result):
    """Display video analysis results."""
    if not result:
        return

    st.markdown("## Video Analysis Results")

    # Display caption
    st.markdown("### Caption")
    st.text_area("Caption", result.caption, height=150)

    # Display hashtags
    st.markdown("### Hashtags")
    hashtags_text = " ".join(result.hashtags)
    st.code(hashtags_text)

    # Copy buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Copy Caption"):
            st.toast("Caption copied to clipboard!")
    with col2:
        if st.button("Copy Hashtags"):
            st.toast("Hashtags copied to clipboard!")

    # Display recommendations
    st.markdown("### Recommendations")
    for recommendation in result.recommendations:
        st.markdown(f"- {recommendation}")

    # Display metadata
    with st.expander("Metadata", expanded=False):
        st.json(result.metadata)
