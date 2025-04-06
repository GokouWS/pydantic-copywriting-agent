"""
Test script for the SEO analysis functionality.
"""

import os
from dotenv import load_dotenv
from models import ContentRequest, ContentType, ToneType, AudienceType
from graph_agent import CopywritingGraphAgent
from seo_analysis import SEOAnalyzer

# Load environment variables
load_dotenv()

def test_seo_analysis():
    """Test the SEO analysis functionality with a sample content."""
    
    # Sample content for testing
    sample_content = """
# The Ultimate Guide to SEO Optimization in 2023

Search Engine Optimization (SEO) is crucial for any website looking to attract organic traffic. In this comprehensive guide, we'll explore the most effective strategies for improving your search rankings.

## Understanding Search Engine Algorithms

Google and other search engines use complex algorithms to determine which pages should rank for specific queries. These algorithms consider hundreds of factors, including:

- Content relevance and quality
- Backlink profile
- User experience metrics
- Mobile-friendliness
- Page loading speed

### On-Page SEO Factors

On-page SEO refers to optimizations you can make directly on your website:

1. **Keyword Research**: Identify relevant keywords with good search volume
2. **Content Optimization**: Create high-quality, comprehensive content
3. **Meta Tags**: Optimize title tags and meta descriptions
4. **Header Tags**: Use H1, H2, H3 tags appropriately
5. **Internal Linking**: Connect related pages on your site

### Off-Page SEO Strategies

Off-page SEO involves actions taken outside your website:

- Building high-quality backlinks
- Social media engagement
- Brand mentions across the web
- Guest posting on relevant sites

## Technical SEO Considerations

Technical SEO ensures your site is accessible and understandable to search engines:

- Site speed optimization
- Mobile responsiveness
- XML sitemaps
- Robots.txt configuration
- Structured data markup

## Measuring SEO Success

Track your progress using these key metrics:

- Organic traffic growth
- Keyword rankings
- Conversion rates
- Bounce rate
- Time on page

By implementing these strategies consistently, you'll improve your website's visibility in search results and drive more targeted traffic to your pages.

[Contact us](https://example.com/contact) to learn more about our SEO services.

![SEO Process Diagram](seo-process.jpg)
    """
    
    # Initialize SEO analyzer
    seo_analyzer = SEOAnalyzer()
    
    # Define target keywords
    target_keywords = ["SEO", "search engine optimization", "keyword research", "backlinks", "content optimization"]
    
    # Perform SEO analysis
    analysis_results = seo_analyzer.analyze(
        content=sample_content,
        target_keywords=target_keywords,
        content_type="blog_post"
    )
    
    # Print analysis results
    print("\n" + "="*50)
    print("SEO ANALYSIS RESULTS:")
    print("="*50)
    print(f"Overall SEO Score: {analysis_results['overall_score']:.1f}/100")
    print(f"Word Count: {analysis_results['word_count']}")
    print(f"Readability Score: {analysis_results['readability_metrics']['readability_score']:.1f}/100")
    
    print("\nKeyword Analysis:")
    for keyword, metrics in analysis_results['keyword_metrics']['keywords'].items():
        print(f"  - {keyword}: {metrics['count']} occurrences, {metrics['density']:.2f}% density")
        print(f"    In Title: {'Yes' if metrics['in_title'] else 'No'}")
        print(f"    In Headings: {'Yes' if metrics['in_headings'] else 'No'}")
    
    print("\nRecommendations:")
    for recommendation in analysis_results['recommendations']:
        print(f"  - {recommendation}")
    
    # Generate SEO improvement prompt
    seo_prompt = seo_analyzer.get_seo_improvement_prompt(analysis_results, sample_content)
    
    print("\n" + "="*50)
    print("SEO IMPROVEMENT PROMPT:")
    print("="*50)
    print(seo_prompt[:500] + "...")  # Print first 500 chars of the prompt
    
    print("\nTest completed successfully!")

def test_full_workflow():
    """Test the full workflow including SEO analysis."""
    
    # Check if API key is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: GOOGLE_API_KEY not found in environment variables.")
        print("Please set it in your .env file and try again.")
        return
    
    print("Initializing graph-based copywriting agent with SEO analysis...")
    
    try:
        # Initialize the agent
        agent = CopywritingGraphAgent()
        
        # Create a content request
        request = ContentRequest(
            content_type=ContentType.BLOG_POST,
            topic="SEO Best Practices for E-commerce Websites",
            tone=ToneType.INFORMATIVE,
            audience=AudienceType.BUSINESS,
            keywords=["e-commerce SEO", "product page optimization", "category pages", "site structure", "technical SEO"],
            word_count=500,
            include_research=True,
            custom_instructions="Focus on practical SEO tips specifically for e-commerce websites. Include sections on product page optimization, category pages, and technical SEO considerations."
        )
        
        print(f"Generating content for topic: {request.topic}")
        print(f"Content type: {request.content_type}")
        print(f"Tone: {request.tone}")
        print(f"Target audience: {request.audience}")
        print("Generating content with SEO optimization...")
        
        # Generate content
        response = agent.generate_content(request)
        
        print("\n" + "="*50)
        print("GENERATED CONTENT:")
        print("="*50)
        print(response.content[:500] + "...")  # Print first 500 chars
        
        print("\n" + "="*50)
        print("SEO SCORE:")
        print("="*50)
        print(f"SEO Score: {response.metadata.get('seo_score', 'Not available')}")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("Test failed.")

if __name__ == "__main__":
    print("Testing SEO Analysis Module...")
    test_seo_analysis()
    
    print("\n\nTesting Full Workflow with SEO Analysis...")
    test_full_workflow()
