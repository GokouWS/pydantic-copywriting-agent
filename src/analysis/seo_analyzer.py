"""
SEO analysis functionality for content optimization.
"""

import re
from typing import Dict, List, Any, Optional


class SEOAnalyzer:
    """Analyzes content for SEO optimization."""
    
    def __init__(self):
        """Initialize the SEO analyzer."""
        pass
    
    def analyze(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Perform SEO analysis on content.
        
        Args:
            content: The content to analyze
            keywords: List of target keywords
            
        Returns:
            Dictionary with SEO analysis results
        """
        try:
            # Clean content
            clean_content = content.lower()
            
            # Basic metrics
            word_count = len(re.findall(r"\b\w+\b", clean_content))
            sentence_count = len(re.split(r'[.!?]+', content))
            paragraph_count = len(re.split(r"\n\s*\n", content))

            # Extract title and headings
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else ""

            h2_headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
            h3_headings = re.findall(r"^###\s+(.+)$", content, re.MULTILINE)

            # Keyword analysis
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
            seo_score = self._calculate_seo_score(
                title, h2_headings, h3_headings, keyword_metrics, 
                word_count, sentence_count, paragraph_count, keywords
            )

            return {
                "overall_score": seo_score,
                "word_count": word_count,
                "sentence_count": sentence_count,
                "paragraph_count": paragraph_count,
                "keyword_metrics": keyword_metrics,
                "has_title": bool(title),
                "h2_count": len(h2_headings),
                "h3_count": len(h3_headings),
                "recommendations": self._generate_recommendations(
                    title, h2_headings, h3_headings, keyword_metrics, 
                    word_count, sentence_count, paragraph_count
                )
            }
        except Exception as e:
            print(f"Error in SEO analysis: {e}")
            # Return a default analysis
            return {
                "overall_score": 50,  # Default score
                "word_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0,
                "keyword_metrics": {k: {"count": 0, "density": 0, "in_title": False, "in_headings": False} for k in keywords},
                "has_title": False,
                "h2_count": 0,
                "h3_count": 0,
                "recommendations": ["Unable to analyze content due to an error."]
            }
    
    def _calculate_seo_score(
        self, title: str, h2_headings: List[str], h3_headings: List[str], 
        keyword_metrics: Dict[str, Dict[str, Any]], word_count: int, 
        sentence_count: int, paragraph_count: int, keywords: List[str]
    ) -> float:
        """Calculate SEO score based on various factors."""
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
        normalized_keyword_score = (keyword_score / max_keyword_score) * 30 if max_keyword_score > 0 else 0
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

        return seo_score
    
    def _generate_recommendations(
        self, title: str, h2_headings: List[str], h3_headings: List[str], 
        keyword_metrics: Dict[str, Dict[str, Any]], word_count: int, 
        sentence_count: int, paragraph_count: int
    ) -> List[str]:
        """Generate SEO recommendations based on analysis."""
        recommendations = []
        
        # Title recommendations
        if not title:
            recommendations.append("Add a title (H1) to your content.")
        elif len(title) < 40:
            recommendations.append(f"Your title is {len(title)} characters. Consider making it longer (40-60 characters) for better SEO.")
        elif len(title) > 60:
            recommendations.append(f"Your title is {len(title)} characters. Consider making it shorter (40-60 characters) for better SEO.")
        
        # Heading recommendations
        if not h2_headings:
            recommendations.append("Add H2 headings to structure your content.")
        if not h3_headings and len(h2_headings) > 1:
            recommendations.append("Consider adding H3 subheadings under your main sections.")
        
        # Keyword recommendations
        low_density_keywords = []
        high_density_keywords = []
        missing_in_title_keywords = []
        missing_in_headings_keywords = []
        
        for keyword, metrics in keyword_metrics.items():
            if metrics["count"] == 0:
                recommendations.append(f"Add the keyword '{keyword}' to your content.")
            elif metrics["density"] < 0.5:
                low_density_keywords.append(keyword)
            elif metrics["density"] > 2.5:
                high_density_keywords.append(keyword)
            
            if not metrics["in_title"] and title:
                missing_in_title_keywords.append(keyword)
            
            if not metrics["in_headings"] and (h2_headings or h3_headings):
                missing_in_headings_keywords.append(keyword)
        
        if low_density_keywords:
            recommendations.append(f"Increase the usage of these keywords: {', '.join(low_density_keywords)}.")
        
        if high_density_keywords:
            recommendations.append(f"Reduce the usage of these keywords to avoid keyword stuffing: {', '.join(high_density_keywords)}.")
        
        if missing_in_title_keywords and len(missing_in_title_keywords) <= 2:
            recommendations.append(f"Include these keywords in your title: {', '.join(missing_in_title_keywords)}.")
        
        if missing_in_headings_keywords and len(missing_in_headings_keywords) <= 3:
            recommendations.append(f"Include these keywords in your headings: {', '.join(missing_in_headings_keywords)}.")
        
        # Content length recommendations
        if word_count < 300:
            recommendations.append(f"Your content is {word_count} words. Consider adding more content (aim for at least 300-500 words).")
        
        # Structure recommendations
        if paragraph_count < 3:
            recommendations.append("Add more paragraphs to improve readability.")
        
        if paragraph_count > 0 and sentence_count / paragraph_count > 5:
            recommendations.append("Your paragraphs are quite long. Consider breaking them into smaller paragraphs for better readability.")
        
        return recommendations
    
    def get_social_media_recommendations(self, platform: str, content: str, keywords: List[str]) -> List[str]:
        """
        Get platform-specific social media recommendations.
        
        Args:
            platform: Social media platform (linkedin, twitter, instagram)
            content: The content to analyze
            keywords: List of target keywords
            
        Returns:
            List of recommendations
        """
        recommendations = []
        word_count = len(re.findall(r"\b\w+\b", content.lower()))
        
        # Platform-specific recommendations
        if platform.lower() == "linkedin":
            if word_count < 100:
                recommendations.append("LinkedIn posts perform better with 100-200 words. Consider adding more content.")
            elif word_count > 500:
                recommendations.append("Your LinkedIn post is quite long. Consider keeping it under 500 words for better engagement.")
            
            if len(keywords) > 0 and not any(keyword.lower() in content.lower() for keyword in keywords):
                recommendations.append("Include industry-specific keywords in your LinkedIn post for better visibility.")
            
            if "?" not in content:
                recommendations.append("Consider adding a question to encourage engagement and comments.")
            
            recommendations.append("Add a clear call-to-action at the end of your LinkedIn post.")
            
        elif platform.lower() == "twitter":
            if word_count > 50:
                recommendations.append("Twitter posts perform better when concise. Consider keeping it under 50 words.")
            
            hashtag_count = len(re.findall(r"#\w+", content))
            if hashtag_count == 0:
                recommendations.append("Add 1-2 relevant hashtags to increase discoverability.")
            elif hashtag_count > 3:
                recommendations.append("Too many hashtags can reduce engagement. Limit to 1-2 hashtags on Twitter.")
            
            if "https://" not in content and "http://" not in content:
                recommendations.append("Consider adding a relevant link to drive traffic.")
            
        elif platform.lower() == "instagram":
            hashtag_count = len(re.findall(r"#\w+", content))
            if hashtag_count < 5:
                recommendations.append("Instagram posts perform better with 5-15 relevant hashtags.")
            elif hashtag_count > 30:
                recommendations.append("Instagram limits posts to 30 hashtags. Remove some hashtags.")
            
            if word_count < 50:
                recommendations.append("Add more context to your Instagram caption for better engagement.")
            elif word_count > 300:
                recommendations.append("Your Instagram caption is quite long. Consider keeping the main message in the first 125 characters.")
            
            if "@" not in content:
                recommendations.append("Consider tagging relevant accounts to increase visibility.")
        
        # General social media recommendations
        if not any(emoji in content for emoji in ["😀", "👍", "🔥", "❤️", "✅", "👏", "🙌", "💯", "⭐", "🚀"]):
            recommendations.append(f"Add emojis to make your {platform} post more engaging and eye-catching.")
        
        return recommendations
