# AI Copywriting & Social Media Agent with Google Gemini 2.0 Pro

An AI-powered content creation assistant built with Pydantic and Streamlit that uses Google's Gemini 2.0 Pro model to generate high-quality, SEO-optimized content with direct-response marketing principles for various use cases. Now with video analysis for Instagram Reels and YouTube Shorts!

## Features

- **Advanced AI**: Uses Google's Gemini 2.0 Pro model for state-of-the-art content generation
- **Advanced SEO Analysis**: Automatically analyzes and optimizes content for search engines
- **Direct Response Marketing**: Incorporates proven principles to maximize click-through rates
- **Social Media Optimization**: Tailored content for LinkedIn, Twitter, Instagram, and YouTube
- **Video Analysis**: Generate captions and hashtags for Instagram Reels and YouTube Shorts
- **User-friendly Interface**: Intuitive Streamlit UI with detailed analytics and visualizations
- **Customizable Parameters**: Tailor content to specific needs and audiences
- **Real-time Updates**: Uses Watchdog for automatic refreshing during development

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your Google API key
6. Download NLTK data (optional): `python -m src.utils.nltk_utils`
7. Run the application: `streamlit run app.py`

## Usage

### Content Generation

1. Select the "Content Generation" tab
2. Choose the content type you want to generate
3. Fill in the required parameters including keywords for SEO optimization
4. Click "Generate Content"
5. Review the generated content along with SEO analysis
6. Export or copy the optimized content

### Video Analysis (In Progress)

1. Select the "Video Analysis" tab
2. Upload a video file (MP4, MOV, AVI, or WEBM)
3. Choose the content type (Instagram Reel or YouTube Short)
4. Add relevant keywords for hashtag generation
5. Click "Analyze Video"
6. Review the generated caption, hashtags, and recommendations
7. Copy and use the content on your preferred platform

## SEO Analysis Features

- **Comprehensive Content Analysis**: Evaluates content structure, keyword usage, and readability
- **SEO Score**: Provides an overall score from 0-100 based on SEO best practices
- **Keyword Optimization**: Analyzes keyword density, placement, and distribution
- **Competitive Insights**: Provides data on top-ranking content for your keywords
- **Automated Improvements**: Automatically enhances content based on SEO analysis
- **Detailed Recommendations**: Provides specific suggestions for further optimization

## Direct Response Marketing

The agent incorporates proven direct-response marketing principles to maximize click-through rates:

- **AIDA Framework**: Attention, Interest, Desire, Action structure
- **Compelling Headlines**: Uses proven formulas for high-converting headlines
- **Urgency Elements**: Creates a sense of time limitation or scarcity
- **Social Proof**: Demonstrates that others have already taken action
- **Clear CTAs**: Makes the next step obvious and compelling
- **Benefit Focus**: Emphasizes what the reader gets rather than features

## Video Analysis Features

- **Frame Extraction**: Automatically extracts key frames from uploaded videos
- **Visual Content Analysis**: Uses Gemini 2.0 Pro's multimodal capabilities to understand video content
- **Platform-Specific Optimization**: Tailored captions and hashtags for Instagram Reels and YouTube Shorts
- **Trending Hashtag Integration**: Incorporates trending hashtags relevant to your content
- **Performance Recommendations**: Provides specific suggestions to improve video engagement
- **One-Click Copy**: Easily copy generated captions and hashtags for immediate use

## Project Structure

```
.
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── .env.example           # Example environment variables
└── src/                    # Source code directory
    ├── api/                # API integrations
    │   ├── brave_search.py # Brave Search API integration
    │   └── gemini_api.py   # Google Gemini API integration
    ├── models/             # Data models
    │   └── content_models.py # Pydantic models for the application
    ├── analysis/           # Content analysis modules
    │   ├── seo_analyzer.py # SEO analysis functionality
    │   └── improved_video_analyzer.py # Video analysis functionality
    ├── ui/                 # User interface components
    │   └── streamlit_components.py # Streamlit UI components
    └── utils/              # Utility functions
        ├── nltk_utils.py   # NLTK utilities
        └── video_utils.py  # Video processing utilities
```
