"""
Streamlit app using the Google Gemini API directly.
"""

import streamlit as st
import os
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
import google.generativeai as genai
import nltk
import ssl
from models import ContentType, ToneType, AudienceType


# Free SEO Tools Integration
class FreeSEOTools:
    """Integration with free SEO tools and data sources."""

    def __init__(self):
        """Initialize the free SEO tools."""
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    def get_keyword_metrics(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Get estimated metrics for a list of keywords using free data sources.

        Args:
            keywords: List of keywords to analyze

        Returns:
            Dictionary with estimated keyword metrics
        """
        keyword_metrics = {}

        for keyword in keywords:
            # Get search result count as a proxy for competition
            result_count = self._get_search_result_count(keyword)

            # Calculate estimated metrics based on keyword characteristics
            metrics = self._calculate_keyword_metrics(keyword, result_count)

            keyword_metrics[keyword] = metrics

        return keyword_metrics

    def _get_search_result_count(self, keyword: str) -> int:
        """
        Get the number of search results for a keyword as a proxy for competition.

        In a production environment, this would make an actual search request,
        but for demonstration purposes, we'll use a formula based on keyword characteristics.
        """
        try:
            # For demonstration, we'll use a formula based on keyword characteristics
            # In a real implementation, you would make an actual search request
            word_count = len(keyword.split())
            char_count = len(keyword)

            # More specific (longer) queries typically have fewer results
            base_count = 10000000  # 10 million
            multiplier = 0.7**word_count  # Exponential decrease with more words

            # Add some variation based on character count
            variation = char_count / 10

            result_count = int(base_count * multiplier * (1 + variation))
            return result_count
        except Exception as e:
            print(f"Error estimating search results: {e}")
            return 1000000  # Default fallback

    def _calculate_keyword_metrics(
        self, keyword: str, result_count: int
    ) -> Dict[str, Any]:
        """
        Calculate estimated keyword metrics based on keyword characteristics.

        Args:
            keyword: The keyword to analyze
            result_count: Estimated number of search results

        Returns:
            Dictionary with estimated keyword metrics
        """
        # Word count affects specificity and competition
        word_count = len(keyword.split())

        # Check for commercial intent words
        commercial_words = [
            "buy",
            "price",
            "cost",
            "cheap",
            "best",
            "top",
            "review",
            "vs",
            "versus",
        ]
        has_commercial_intent = any(
            word in keyword.lower() for word in commercial_words
        )

        # Calculate volume (higher for shorter, more common keywords)
        # This is a very rough estimate for demonstration purposes
        base_volume = 10000
        volume_multiplier = 0.5 ** (
            word_count - 1
        )  # Exponential decrease with more words
        estimated_volume = int(base_volume * volume_multiplier)

        # Calculate difficulty (higher for shorter, more competitive keywords)
        # Scale: 0-100, where 100 is most difficult
        base_difficulty = 70 - (word_count * 10)  # Longer keywords are less difficult
        competition_factor = min(result_count / 10000000, 1)  # Normalize by 10M results
        estimated_difficulty = max(
            min(int(base_difficulty * competition_factor * 1.5), 100), 1
        )

        # Calculate CPC (higher for commercial keywords)
        base_cpc = 0.5
        commercial_multiplier = 3 if has_commercial_intent else 1
        estimated_cpc = round(
            base_cpc * commercial_multiplier * (1 + competition_factor), 2
        )

        return {
            "volume": estimated_volume,
            "difficulty": estimated_difficulty,
            "competition": round(competition_factor, 2),
            "cpc": estimated_cpc,
            "results": result_count,
        }

    def analyze_serp(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Generate simulated SERP data for a keyword.

        In a production environment, this would scrape actual search results,
        but for demonstration purposes, we'll generate simulated data.

        Args:
            keyword: Keyword to analyze

        Returns:
            List of simulated top-ranking URLs with metrics
        """
        try:
            # For demonstration, we'll generate simulated SERP data
            # In a real implementation, you would scrape actual search results

            # Common domains for demonstration
            common_domains = [
                "wikipedia.org",
                "amazon.com",
                "nytimes.com",
                "forbes.com",
                "healthline.com",
                "webmd.com",
                "hubspot.com",
                "shopify.com",
                "medium.com",
                "youtube.com",
            ]

            # Generate simulated SERP data
            serp_data = []
            for i in range(10):  # Top 10 results
                # Select a domain based on keyword and position
                domain_index = (hash(keyword) + i) % len(common_domains)
                domain = common_domains[domain_index]

                # Generate URL
                url = f"https://www.{domain}/" + keyword.replace(" ", "-")
                if i > 0:
                    url += f"-{i}"

                # Generate metrics
                position = i + 1
                traffic = max(
                    1000 - (position * 100), 100
                )  # Higher positions get more traffic
                keywords_count = max(
                    500 - (position * 30), 50
                )  # Higher positions rank for more keywords
                featured = (
                    i == 0 and hash(keyword) % 5 == 0
                )  # 20% chance for first result to be featured

                serp_data.append(
                    {
                        "domain": domain,
                        "url": url,
                        "position": position,
                        "traffic": traffic,
                        "keywords": keywords_count,
                        "featured_snippet": featured,
                    }
                )

            return serp_data
        except Exception as e:
            print(f"Error generating SERP data: {e}")
            return []


# Handle SSL certificate issues for NLTK downloads

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK data
try:
    # Force download regardless of whether it's already there
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    print("NLTK data downloaded successfully!")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Load environment variables
load_dotenv()

# Configure the API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


# Simple SEO analysis function
def analyze_seo(content, keywords):
    """Perform a simple SEO analysis on the content."""
    try:
        import re

        # Clean content
        clean_content = content.lower()

        # Basic metrics
        word_count = len(re.findall(r"\b\w+\b", clean_content))

        # Simple sentence splitting
        sentence_count = len(re.split(r"[.!?]+", content))

        paragraph_count = len(re.split(r"\n\s*\n", content))

        # Extract title and headings
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""

        h2_headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        h3_headings = re.findall(r"^###\s+(.+)$", content, re.MULTILINE)

        # Simple keyword analysis without NLTK
        keyword_metrics = {}
        for keyword in keywords:
            count = clean_content.lower().count(keyword.lower())
            density = (count / word_count) * 100 if word_count > 0 else 0
            keyword_metrics[keyword] = {
                "count": count,
                "density": density,
                "in_title": keyword.lower() in title.lower() if title else False,
                "in_headings": any(
                    keyword.lower() in heading.lower()
                    for heading in h2_headings + h3_headings
                ),
            }

        # Calculate SEO score
        seo_score = 0

        # Title score (20 points)
        if title:
            seo_score += 10
            if 40 <= len(title) <= 60:
                seo_score += 10

        # Headings score (20 points)
        if h2_headings:
            seo_score += 10
        if h3_headings:
            seo_score += 10

        # Keyword score (30 points)
        keyword_score = 0
        for keyword, metrics in keyword_metrics.items():
            if metrics["count"] > 0:
                keyword_score += 2
            if metrics["in_title"]:
                keyword_score += 3
            if metrics["in_headings"]:
                keyword_score += 2
            if 0.5 <= metrics["density"] <= 2.5:
                keyword_score += 3

        # Normalize keyword score to 30 points
        max_keyword_score = len(keywords) * 10 if keywords else 10
        normalized_keyword_score = (
            (keyword_score / max_keyword_score) * 30 if max_keyword_score > 0 else 0
        )
        seo_score += normalized_keyword_score

        # Content length score (20 points)
        if word_count >= 1000:
            seo_score += 20
        elif word_count >= 500:
            seo_score += 15
        elif word_count >= 300:
            seo_score += 10
        elif word_count >= 100:
            seo_score += 5

        # Structure score (10 points)
        if paragraph_count >= 5:
            seo_score += 5
        if sentence_count / paragraph_count <= 3 and paragraph_count > 0:
            seo_score += 5

        return {
            "overall_score": seo_score,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "keyword_metrics": keyword_metrics,
            "has_title": bool(title),
            "h2_count": len(h2_headings),
            "h3_count": len(h3_headings),
        }
    except Exception as e:
        print(f"Error in SEO analysis: {e}")
        # Return a default analysis
        return {
            "overall_score": 50,  # Default score
            "word_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "keyword_metrics": {
                k: {"count": 0, "density": 0, "in_title": False, "in_headings": False}
                for k in keywords
            },
            "has_title": False,
            "h2_count": 0,
            "h3_count": 0,
        }


# Enhanced SEO analysis with free SEO tools
def enhanced_seo_analysis(content, keywords, use_advanced_seo=False):
    """Perform enhanced SEO analysis with free SEO tools."""
    # Get basic SEO metrics
    basic_seo = analyze_seo(content, keywords)

    # If advanced SEO is enabled and we have keywords, enhance with free SEO tools
    if use_advanced_seo and keywords:
        try:
            # Initialize Free SEO Tools
            seo_tools = FreeSEOTools()

            # Get keyword metrics
            keyword_metrics = seo_tools.get_keyword_metrics(keywords)

            # Get SERP data for primary keyword
            primary_keyword = keywords[0] if keywords else ""
            serp_data = (
                seo_tools.analyze_serp(primary_keyword) if primary_keyword else []
            )

            # Generate competitive insights
            competitive_insights = _generate_competitive_insights(serp_data)

            # Enhance basic SEO analysis with advanced data
            enhanced_seo = {
                **basic_seo,
                "keyword_metrics": {
                    **basic_seo["keyword_metrics"],
                    "advanced_data": keyword_metrics,
                },
                "serp_analysis": serp_data,
                "competitive_insights": competitive_insights,
            }

            return enhanced_seo
        except Exception as e:
            print(f"Error enhancing SEO with advanced tools: {e}")
            return basic_seo
    else:
        return basic_seo


def _generate_competitive_insights(serp_data):
    """Generate insights from competitive SERP data."""
    insights = []

    if not serp_data:
        return ["No competitive data available"]

    # Count domains in top results
    domains = {}
    for item in serp_data:
        domain = item.get("domain", "")
        if domain:
            domains[domain] = domains.get(domain, 0) + 1

    # Find most common domains
    common_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:3]
    if common_domains:
        domains_str = ", ".join([domain for domain, _ in common_domains])
        insights.append(f"Top domains in search results: {domains_str}")

    # Analyze featured snippets
    featured_count = sum(1 for item in serp_data if item.get("featured_snippet"))
    if featured_count > 0:
        insights.append(
            f"There are {featured_count} featured snippets in the top results"
        )

    # Analyze traffic potential
    total_traffic = sum(item.get("traffic", 0) for item in serp_data)
    avg_traffic = total_traffic / len(serp_data) if serp_data else 0
    insights.append(f"Average traffic to top results: {avg_traffic:.2f} visits/month")

    # Analyze keyword count
    total_keywords = sum(item.get("keywords", 0) for item in serp_data)
    avg_keywords = total_keywords / len(serp_data) if serp_data else 0
    insights.append(f"Top pages rank for an average of {avg_keywords:.0f} keywords")

    return insights


# Function to display enhanced SEO analysis
def display_enhanced_seo_analysis(seo_results):
    """Display enhanced SEO analysis results in Streamlit."""
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


# Function to display basic SEO analysis
def display_seo_analysis(seo_results):
    """Display SEO analysis results in Streamlit."""
    if not seo_results:
        return

    seo_score = seo_results.get("overall_score", 0)

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
            st.markdown("### SEO Score")
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

        # Display keyword metrics
        st.markdown("### Keyword Analysis")
        for keyword, metrics in seo_results["keyword_metrics"].items():
            st.markdown(
                f"**{keyword}**: {metrics['count']} occurrences, {metrics['density']:.2f}% density"
            )
            st.markdown(f"- In title: {'✅' if metrics['in_title'] else '❌'}")
            st.markdown(f"- In headings: {'✅' if metrics['in_headings'] else '❌'}")

        # Display content metrics
        st.markdown("### Content Structure")
        st.markdown(f"- Word count: {seo_results['word_count']}")
        st.markdown(f"- Sentence count: {seo_results['sentence_count']}")
        st.markdown(f"- Paragraph count: {seo_results['paragraph_count']}")
        st.markdown(f"- Has title: {'✅' if seo_results['has_title'] else '❌'}")
        st.markdown(f"- H2 headings: {seo_results['h2_count']}")
        st.markdown(f"- H3 headings: {seo_results['h3_count']}")


# Page configuration
st.set_page_config(
    page_title="AI Copywriting Agent (Direct)",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "content_history" not in st.session_state:
    st.session_state.content_history = []

# Sidebar
st.sidebar.title("AI Copywriting Agent")
st.sidebar.markdown("Generate high-quality content for various use cases")

# Model info
st.sidebar.markdown("### Model Information")
st.sidebar.info(
    "Using Google Gemini 2.5 Pro with direct-response marketing principles and SEO optimization."
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
st.title("✍️ AI Copywriting Agent (Direct API)")
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

    # Show progress
    with st.status("Generating content...", expanded=True) as status:
        if include_research:
            st.write("Researching relevant information...")

        st.write("Crafting your content...")

        # Generate content
        try:
            # Create the prompt
            prompt = f"""
            # Content Creation Request

            ## Content Type:
            {content_type}

            ## Topic:
            {topic}

            ## Target Audience:
            {audience}

            ## Tone and Style:
            {tone}

            ## Keywords to Include:
            {", ".join(keyword_list) if keyword_list else "No specific keywords provided"}

            ## Target Length:
            Approximately {word_count} words

            {f"## Additional Instructions:\\n{custom_instructions}" if custom_instructions else ""}

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

            ## SEO Optimization Guidelines:
            - Include primary keywords in the title, headings, and first paragraph
            - Maintain keyword density between 0.5% and 2.5%
            - Use proper heading hierarchy (H1, H2, H3)
            - Create descriptive, keyword-rich headings
            - Keep paragraphs short for readability
            - Include internal and external links where appropriate
            - Use descriptive alt text for any images
            - Create a meta description that includes primary keywords

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
            - Optimize for both human engagement and search engines
            """

            # Initialize the model
            model = genai.GenerativeModel("gemini-2.0-pro-exp")

            # Generate content
            response = model.generate_content(prompt)

            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            metadata = {
                "content_type": content_type,
                "topic": topic,
                "tone": tone,
                "audience": audience,
                "word_count": word_count,
                "model_used": "gemini-2.0-pro-exp",
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
        seo_results = enhanced_seo_analysis(
            response.text, keyword_list, use_advanced_seo
        )

        # Add SEO score to metadata
        metadata["seo_score"] = seo_results["overall_score"]
        metadata["using_advanced_seo"] = True

        # Display enhanced SEO analysis
        display_enhanced_seo_analysis(seo_results)
    else:
        # Use basic SEO analysis
        seo_results = analyze_seo(response.text, keyword_list)

        # Add SEO score to metadata
        metadata["seo_score"] = seo_results["overall_score"]

        # Display basic SEO analysis
        display_seo_analysis(seo_results)

    # Display the content
    st.markdown("### Content Preview")
    st.markdown(response.text)

    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save as Markdown"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{content_type}_{timestamp}.md"
            with open(filename, "w") as f:
                f.write(response.text)
            st.success(f"Content saved to {filename}")

    with col2:
        if st.button("Copy to Clipboard"):
            st.code(response.text)
            st.success("Content copied to clipboard (use the copy button above)")
