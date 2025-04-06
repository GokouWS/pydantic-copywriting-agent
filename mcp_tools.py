"""
This module provides integration with various MCP (Model Control Protocol) tools
for enhancing the AI copywriting agent with external capabilities.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class BraveSearchTool:
    """
    Tool for performing web searches using the Brave Search API.
    """
    
    def __init__(self):
        self.api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_SEARCH_API_KEY not found in environment variables")
        
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
    
    def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search using Brave Search API.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        params = {
            "q": query,
            "count": num_results
        }
        
        response = requests.get(
            self.base_url,
            headers=self.headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Search API returned status code {response.status_code}")
        
        data = response.json()
        results = []
        
        for item in data.get("web", {}).get("results", []):
            results.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("url", ""),
                "site": item.get("site", "")
            })
        
        return results


class ContentAnalysisTool:
    """
    Tool for analyzing content for readability, SEO, and other metrics.
    This is a placeholder for a real implementation that would integrate with
    services like Clearscope, MarketMuse, or custom NLP models.
    """
    
    def analyze_readability(self, text: str) -> Dict[str, Any]:
        """
        Analyze the readability of text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Readability metrics
        """
        # This would be implemented with actual readability algorithms
        # For now, return placeholder data
        return {
            "flesch_kincaid_grade": 8.5,
            "flesch_reading_ease": 65.2,
            "gunning_fog": 10.1,
            "smog_index": 9.8,
            "coleman_liau_index": 10.2,
            "automated_readability_index": 9.5,
            "dale_chall_readability_score": 7.8,
            "difficult_words": 42,
            "word_count": len(text.split()),
            "sentence_count": text.count(".") + text.count("!") + text.count("?"),
            "avg_sentence_length": len(text.split()) / (text.count(".") + text.count("!") + text.count("?") + 1),
            "avg_word_length": sum(len(word) for word in text.split()) / len(text.split())
        }
    
    def analyze_seo(self, text: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Analyze the SEO characteristics of text.
        
        Args:
            text: The text to analyze
            keywords: Target keywords
            
        Returns:
            SEO metrics
        """
        # This would be implemented with actual SEO analysis algorithms
        # For now, return placeholder data
        text_lower = text.lower()
        keyword_counts = {keyword: text_lower.count(keyword.lower()) for keyword in keywords}
        total_keywords = sum(keyword_counts.values())
        
        return {
            "keyword_density": total_keywords / len(text.split()) if text else 0,
            "keyword_counts": keyword_counts,
            "has_meta_description": "meta description" in text_lower,
            "title_length": len(text.split("\n")[0]) if text else 0,
            "content_length": len(text),
            "word_count": len(text.split()),
            "readability_score": 65.2  # Placeholder
        }


class CopywritingBestPractices:
    """
    Tool for providing copywriting best practices and templates.
    """
    
    def get_headline_formulas(self, category: Optional[str] = None) -> List[str]:
        """
        Get proven headline formulas.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of headline formulas
        """
        all_formulas = {
            "how_to": [
                "How to {Achieve Desired Outcome} Without {Pain Point}",
                "How to {Achieve Desired Outcome} in {Timeframe}",
                "How I {Achieved Result} in {Timeframe}",
                "How {Target Audience} Can {Achieve Desired Outcome}",
                "How to {Achieve Desired Outcome} Like {Expert/Celebrity}"
            ],
            "list": [
                "{Number} Ways to {Achieve Desired Outcome}",
                "{Number} {Adjective} Tips for {Achieving Desired Outcome}",
                "{Number} Secrets of {Successful Outcome}",
                "The Top {Number} {Resources/Tools} for {Target Audience}",
                "{Number} Mistakes That {Prevent Desired Outcome}"
            ],
            "question": [
                "Do You Make These {Number} {Topic} Mistakes?",
                "Are You {Experiencing Pain Point}?",
                "Want to {Achieve Desired Outcome}?",
                "What Would Happen If You {Action}?",
                "Is {Common Belief} Actually {Hurting/Helping} You?"
            ],
            "problem_solution": [
                "{Pain Point}? Try This {Solution}",
                "End {Pain Point} With This {Adjective} {Solution}",
                "Struggling With {Pain Point}? Here's Your {Solution}",
                "The {Adjective} Way to Solve {Pain Point}",
                "Finally! A Solution for {Pain Point}"
            ],
            "curiosity": [
                "The Secret to {Desired Outcome}",
                "{Number} Little-Known Ways to {Achieve Desired Outcome}",
                "Here's What {Experts/Competitors} Don't Want You to Know About {Topic}",
                "The Surprising Truth About {Topic}",
                "What {Experts/Celebrities} Can Teach You About {Topic}"
            ]
        }
        
        if category and category in all_formulas:
            return all_formulas[category]
        
        # Return all formulas if no category specified
        return [formula for formulas in all_formulas.values() for formula in formulas]
    
    def get_copywriting_frameworks(self) -> Dict[str, str]:
        """
        Get descriptions of proven copywriting frameworks.
        
        Returns:
            Dictionary of framework names and descriptions
        """
        return {
            "AIDA": "Attention, Interest, Desire, Action - A framework that guides the reader through a funnel from getting their attention to taking action.",
            "PAS": "Problem, Agitation, Solution - Identify a problem, agitate it by emphasizing pain points, then present your solution.",
            "BAB": "Before, After, Bridge - Show the current state, the desired state, and how your product/service bridges the gap.",
            "4Cs": "Clear, Concise, Compelling, Credible - Focus on these four qualities to create effective copy.",
            "FAB": "Features, Advantages, Benefits - Describe what your product has, what it does, and how it improves the customer's life.",
            "STAR": "Situation, Task, Action, Result - Tell a story about a problem, what needed to be done, what was done, and the outcome.",
            "4Ps": "Promise, Picture, Proof, Push - Make a promise, paint a picture of the result, provide proof, and push for action.",
            "PPPP": "Picture, Promise, Prove, Push - Similar to 4Ps but starts with the picture of what's possible.",
            "QUEST": "Qualify, Understand, Educate, Stimulate, Transition - Guide prospects through a journey to becoming customers."
        }
    
    def get_emotional_triggers(self) -> Dict[str, List[str]]:
        """
        Get emotional triggers for different types of content.
        
        Returns:
            Dictionary of emotional trigger categories and examples
        """
        return {
            "fear": [
                "Missing out (FOMO)",
                "Failure",
                "Rejection",
                "Uncertainty",
                "Loss"
            ],
            "desire": [
                "Success",
                "Recognition",
                "Belonging",
                "Comfort",
                "Pleasure"
            ],
            "trust": [
                "Safety",
                "Reliability",
                "Expertise",
                "Transparency",
                "Social proof"
            ],
            "value": [
                "Saving money",
                "Saving time",
                "Exclusivity",
                "Simplicity",
                "Convenience"
            ],
            "identity": [
                "Self-image",
                "Status",
                "Group affiliation",
                "Personal values",
                "Aspirations"
            ]
        }
