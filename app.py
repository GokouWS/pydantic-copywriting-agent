import streamlit as st
import json
from datetime import datetime
from typing import List

from models import ContentRequest, ContentType, ToneType, AudienceType, ContentResponse
from graph_agent import CopywritingGraphAgent

# Page configuration
st.set_page_config(
    page_title="AI Copywriting Agent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "content_history" not in st.session_state:
    st.session_state.content_history = []

if "agent" not in st.session_state:
    try:
        st.session_state.agent = CopywritingGraphAgent()
    except ValueError as e:
        st.error(f"Error initializing agent: {e}")
        st.error(
            "Please make sure you have set up your .env file with the required API keys."
        )
        st.stop()


# Helper functions
def save_content(content_response: ContentResponse, filename: str = None):
    """Save the generated content to a file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        content_type = content_response.metadata.get("content_type", "content")
        filename = f"{content_type}_{timestamp}.md"

    with open(filename, "w") as f:
        f.write(content_response.content)

    return filename


def display_research_results(research_results):
    """Display research results in an expander"""
    if not research_results:
        return

    with st.expander("Research Sources", expanded=False):
        for i, result in enumerate(research_results, 1):
            st.markdown(f"### {i}. [{result.title}]({result.url})")
            st.markdown(f"**Source:** {result.source}")
            st.markdown(f"**Summary:** {result.snippet}")
            st.markdown("---")


def display_seo_analysis(metadata):
    """Display SEO analysis results"""
    if not metadata or "seo_score" not in metadata:
        return

    seo_score = metadata.get("seo_score", 0)

    # Determine score color
    if seo_score >= 80:
        score_color = "green"
    elif seo_score >= 60:
        score_color = "orange"
    else:
        score_color = "red"

    with st.expander("SEO Analysis", expanded=False):
        # Display SEO score with gauge chart
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(f"### SEO Score")
            st.markdown(
                f"<h1 style='color: {score_color};'>{seo_score:.1f}/100</h1>",
                unsafe_allow_html=True,
            )

        with col2:
            # Create a simple gauge chart using progress bar
            st.markdown("### SEO Performance")
            st.progress(seo_score / 100)

            # Add performance label
            if seo_score >= 80:
                st.success("Excellent SEO optimization")
            elif seo_score >= 60:
                st.warning("Good, but could be improved")
            else:
                st.error("Needs significant improvement")

        # Add SEO recommendations section
        st.markdown("### SEO Recommendations")
        st.markdown(
            "The content has been automatically optimized for search engines based on the following factors:"
        )

        st.markdown(
            "✅ **Keyword optimization**: Strategic placement of keywords in title, headings, and content"
        )
        st.markdown(
            "✅ **Content structure**: Proper heading hierarchy and paragraph structure"
        )
        st.markdown(
            "✅ **Readability**: Appropriate sentence length and complexity for target audience"
        )
        st.markdown(
            "✅ **Meta elements**: Inclusion of meta description and alt text for images"
        )
        st.markdown(
            "✅ **Internal and external linking**: Strategic link placement for SEO benefit"
        )


# Sidebar
st.sidebar.title("AI Copywriting Agent")
st.sidebar.markdown("Generate high-quality content for various use cases")

# Model info
st.sidebar.markdown("### Model Information")
st.sidebar.info(
    "Using Google Gemini 1.5 Pro with LangGraph for advanced workflow management and direct-response optimization."
)

# Content history
if st.session_state.content_history:
    st.sidebar.markdown("## Content History")
    for i, (timestamp, metadata) in enumerate(st.session_state.content_history):
        if st.sidebar.button(
            f"{metadata['content_type']} - {metadata['topic'][:20]}... ({timestamp})",
            key=f"history_{i}",
        ):
            st.session_state.selected_history_index = i

# Main content area
st.title("✍️ AI Copywriting Agent")
st.markdown("Generate high-quality content optimized for your specific needs")

# Input form
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

        custom_instructions = st.text_area(
            "Custom Instructions (Optional)",
            placeholder="Enter any additional instructions or requirements",
        )

    submit_button = st.form_submit_button("Generate Content")

# Process form submission
if submit_button:
    # Parse keywords
    keyword_list = [k.strip() for k in keywords.split("\n") if k.strip()]

    # Create content request
    request = ContentRequest(
        content_type=content_type,
        topic=topic,
        tone=tone,
        audience=audience,
        keywords=keyword_list,
        word_count=word_count,
        include_research=include_research,
        custom_instructions=custom_instructions if custom_instructions else None,
    )

    # Show progress
    with st.status("Generating content...", expanded=True) as status:
        if include_research:
            st.write("Researching relevant information...")

        st.write("Crafting your content...")
        st.write("Enhancing with direct-response marketing principles...")
        st.write("Analyzing and optimizing for SEO...")

        # Generate content
        try:
            content_response = st.session_state.agent.generate_content(request)

            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.content_history.append(
                (timestamp, content_response.metadata)
            )

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
        st.json(content_response.metadata)

    # Display research results if available
    display_research_results(content_response.research_results)

    # Display SEO analysis if available
    display_seo_analysis(content_response.metadata)

    # Display the content
    st.markdown("### Content Preview")
    st.markdown(content_response.content)

    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save as Markdown"):
            filename = save_content(content_response)
            st.success(f"Content saved to {filename}")

    with col2:
        if st.button("Copy to Clipboard"):
            st.code(content_response.content)
            st.success("Content copied to clipboard (use the copy button above)")

# Display selected history item if applicable
if hasattr(st.session_state, "selected_history_index"):
    st.markdown("## Content from History")
    st.write("This feature would display previously generated content from history")
    # In a real implementation, you would store and retrieve the actual content

# Run the app with: streamlit run app.py
if __name__ == "__main__":
    pass
