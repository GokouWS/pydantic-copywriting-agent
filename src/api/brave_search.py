"""
Integration with Brave Search API for SEO and social media optimization.
"""

import os
import requests
from typing import List, Dict, Any, Optional
import json


class BraveSearchAPI:
    """Integration with Brave Search API for SEO and social media optimization."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Brave Search API client.
        
        Args:
            api_key: Brave Search API key (optional, will use environment variable if not provided)
        """
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        self.base_url = "https://api.search.brave.com/res/v1"
        
        # For demo purposes, if no API key is available, use simulated data
        self.use_simulated_data = not self.api_key
        
        if self.use_simulated_data:
            print("No Brave API key found. Using simulated data.")
    
    def search(self, query: str, count: int = 10) -> Dict[str, Any]:
        """
        Perform a search query using Brave Search API.
        
        Args:
            query: Search query
            count: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        if self.use_simulated_data:
            return self._get_simulated_search_results(query, count)
        
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "count": count
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error from Brave Search API: {response.status_code}")
                print(response.text)
                return self._get_simulated_search_results(query, count)
        except Exception as e:
            print(f"Error calling Brave Search API: {e}")
            return self._get_simulated_search_results(query, count)
    
    def get_trending_hashtags(self, topic: str, platform: str = "all") -> List[str]:
        """
        Get trending hashtags for a topic on a specific platform.
        
        Args:
            topic: The topic to find hashtags for
            platform: Social media platform (linkedin, twitter, instagram, or all)
            
        Returns:
            List of trending hashtags
        """
        if self.use_simulated_data:
            return self._get_simulated_hashtags(topic, platform)
        
        # Construct a query that's likely to return hashtag information
        query = f"trending hashtags {topic} {platform}"
        
        # Get search results
        results = self.search(query, count=5)
        
        # Extract hashtags from results (this would need to be customized based on actual API response)
        hashtags = self._extract_hashtags_from_results(results, topic)
        
        return hashtags
    
    def analyze_social_content(self, topic: str, platform: str) -> Dict[str, Any]:
        """
        Analyze top-performing social media content for a topic.
        
        Args:
            topic: The topic to analyze
            platform: Social media platform (linkedin, twitter, instagram)
            
        Returns:
            Dictionary with analysis results
        """
        if self.use_simulated_data:
            return self._get_simulated_social_analysis(topic, platform)
        
        # Construct a query that's likely to return relevant social media content
        query = f"best {platform} posts about {topic}"
        
        # Get search results
        results = self.search(query, count=10)
        
        # Analyze the results
        analysis = self._analyze_social_results(results, platform)
        
        return analysis
    
    def _extract_hashtags_from_results(self, results: Dict[str, Any], topic: str) -> List[str]:
        """Extract hashtags from search results."""
        # This would need to be customized based on actual API response
        # For now, we'll return simulated data
        return self._get_simulated_hashtags(topic)
    
    def _analyze_social_results(self, results: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Analyze social media search results."""
        # This would need to be customized based on actual API response
        # For now, we'll return simulated data
        return self._get_simulated_social_analysis("", platform)
    
    def _get_simulated_search_results(self, query: str, count: int) -> Dict[str, Any]:
        """Generate simulated search results for demonstration purposes."""
        words = query.split()
        results = []
        
        for i in range(min(count, 10)):
            results.append({
                "title": f"Result {i+1} for {' '.join(words[:3])}",
                "url": f"https://example.com/result-{i+1}",
                "description": f"This is a simulated search result for the query '{query}'. It contains relevant information about {' '.join(words[:3])}.",
                "age": f"{i+1} days ago"
            })
        
        return {
            "query": query,
            "results": results,
            "mixed": {
                "news": [
                    {
                        "title": f"Latest news about {' '.join(words[:2])}",
                        "url": "https://example.com/news",
                        "description": f"Breaking news related to {' '.join(words[:2])}.",
                        "age": "1 hour ago"
                    }
                ],
                "videos": [
                    {
                        "title": f"Video about {' '.join(words[:2])}",
                        "url": "https://example.com/video",
                        "description": f"Popular video discussing {' '.join(words[:2])}.",
                        "age": "2 days ago"
                    }
                ]
            }
        }
    
    def _get_simulated_hashtags(self, topic: str, platform: str = "all") -> List[str]:
        """Generate simulated trending hashtags for demonstration purposes."""
        # Base hashtags that are generally popular
        base_hashtags = ["#trending", "#viral", "#follow", "#like", "#share"]
        
        # Convert topic to hashtags
        topic_words = topic.lower().replace("-", " ").split()
        topic_hashtags = [f"#{word}" for word in topic_words if len(word) > 3]
        
        # Platform-specific hashtags
        platform_hashtags = {
            "linkedin": ["#networking", "#career", "#business", "#leadership", "#innovation", "#professional"],
            "twitter": ["#trending", "#followfriday", "#tbt", "#nowplaying", "#news"],
            "instagram": ["#instagood", "#photooftheday", "#beautiful", "#fashion", "#happy"],
            "youtube": ["#youtubeshorts", "#subscribe", "#trending", "#viral", "#newvideo"],
            "all": ["#trending", "#content", "#digital", "#social", "#follow"]
        }
        
        # Combine hashtags based on platform
        selected_platform = platform.lower() if platform.lower() in platform_hashtags else "all"
        combined_hashtags = topic_hashtags + platform_hashtags[selected_platform]
        
        # Add some variation based on the topic
        if "marketing" in topic.lower():
            combined_hashtags.extend(["#digitalmarketing", "#contentmarketing", "#socialmedia", "#strategy"])
        elif "tech" in topic.lower() or "technology" in topic.lower():
            combined_hashtags.extend(["#tech", "#innovation", "#digital", "#future", "#ai"])
        elif "health" in topic.lower() or "fitness" in topic.lower():
            combined_hashtags.extend(["#health", "#fitness", "#wellness", "#lifestyle", "#motivation"])
        
        # Return a unique set of hashtags (up to 15)
        unique_hashtags = list(set(combined_hashtags))
        return unique_hashtags[:15]
    
    def _get_simulated_social_analysis(self, topic: str, platform: str) -> Dict[str, Any]:
        """Generate simulated social media content analysis for demonstration purposes."""
        platform = platform.lower()
        
        # Platform-specific engagement patterns
        engagement_patterns = {
            "linkedin": {
                "optimal_post_length": "1200-1600 characters",
                "best_posting_times": ["Tuesday 10-11am", "Wednesday 8-10am", "Thursday 1-2pm"],
                "top_content_types": ["How-to articles", "Industry insights", "Professional achievements"],
                "engagement_drivers": ["Questions", "Personal stories", "Data-driven insights"],
                "optimal_hashtag_count": "3-5 hashtags"
            },
            "twitter": {
                "optimal_post_length": "70-100 characters",
                "best_posting_times": ["Monday 9am", "Wednesday 12pm", "Friday 3pm"],
                "top_content_types": ["News", "Humor", "Polls", "Thread starters"],
                "engagement_drivers": ["Questions", "Controversial opinions", "Trending topics"],
                "optimal_hashtag_count": "1-2 hashtags"
            },
            "instagram": {
                "optimal_post_length": "138-150 characters",
                "best_posting_times": ["Monday 11am", "Wednesday 3pm", "Thursday 7pm"],
                "top_content_types": ["High-quality images", "Carousels", "Behind-the-scenes"],
                "engagement_drivers": ["Stories", "Questions", "User-generated content"],
                "optimal_hashtag_count": "9-11 hashtags"
            },
            "youtube": {
                "optimal_post_length": "Short: 30-60 seconds, Long: 10-15 minutes",
                "best_posting_times": ["Saturday 9-11am", "Sunday 3-6pm", "Thursday 2-4pm"],
                "top_content_types": ["Tutorials", "Reviews", "Entertainment", "Vlogs"],
                "engagement_drivers": ["Clear CTAs", "Questions in comments", "Consistent posting"],
                "optimal_hashtag_count": "3-5 hashtags"
            }
        }
        
        # Default to LinkedIn if platform not found
        selected_platform = platform if platform in engagement_patterns else "linkedin"
        
        # Sample content ideas based on platform
        content_ideas = {
            "linkedin": [
                "Share industry insights with data visualization",
                "Post about recent professional achievement",
                "Create a how-to guide for solving a common problem",
                "Share thoughts on industry trends with a question",
                "Post a carousel of tips related to your expertise"
            ],
            "twitter": [
                "Share a quick tip with a relevant hashtag",
                "Ask an engaging question about a trending topic",
                "Create a poll about industry preferences",
                "Share a link to valuable content with commentary",
                "Start a thread breaking down a complex topic"
            ],
            "instagram": [
                "Create a carousel of tips with eye-catching graphics",
                "Share behind-the-scenes content of your work",
                "Post a quote graphic with inspirational message",
                "Create a before/after transformation post",
                "Share user-generated content with permission"
            ],
            "youtube": [
                "Create a short tutorial solving a specific problem",
                "Share a day-in-the-life style vlog",
                "Create a reaction video to industry news",
                "Post a product review or comparison",
                "Create a compilation of tips in your niche"
            ]
        }
        
        return {
            "platform": platform,
            "engagement_patterns": engagement_patterns[selected_platform],
            "content_ideas": content_ideas[selected_platform],
            "recommended_posting_frequency": "3-4 times per week",
            "top_performing_content_formats": engagement_patterns[selected_platform]["top_content_types"][:3]
        }
