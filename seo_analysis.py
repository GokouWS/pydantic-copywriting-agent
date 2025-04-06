"""
SEO analysis module for evaluating and improving content.
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Handle SSL certificate issues for NLTK downloads
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download necessary NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


class SEOAnalyzer:
    """
    Analyzes content for SEO optimization and provides recommendations.
    """

    def __init__(self):
        """Initialize the SEO analyzer."""
        self.stop_words = set(stopwords.words("english"))

    def analyze(
        self, content: str, target_keywords: List[str], content_type: str
    ) -> Dict[str, Any]:
        """
        Perform comprehensive SEO analysis on content.

        Args:
            content: The content to analyze
            target_keywords: List of target keywords
            content_type: Type of content (blog_post, landing_page, etc.)

        Returns:
            Dictionary with analysis results and recommendations
        """
        # Clean and prepare content
        clean_content = content.lower()

        # Basic metrics
        word_count = len(re.findall(r"\b\w+\b", clean_content))
        sentence_count = len(sent_tokenize(content))
        paragraph_count = len(re.split(r"\n\s*\n", content))

        # Extract title and headings
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""

        h2_headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        h3_headings = re.findall(r"^###\s+(.+)$", content, re.MULTILINE)

        # Keyword analysis
        keyword_metrics = self._analyze_keywords(clean_content, target_keywords)

        # Readability analysis
        readability_metrics = self._analyze_readability(content)

        # Content structure analysis
        structure_metrics = {
            "has_title": bool(title),
            "title_length": len(title),
            "h2_count": len(h2_headings),
            "h3_count": len(h3_headings),
            "paragraph_count": paragraph_count,
            "avg_paragraph_length": word_count / paragraph_count
            if paragraph_count > 0
            else 0,
            "has_meta_description": self._check_meta_description(content),
            "has_image_alt": self._check_image_alt(content),
            "has_internal_links": self._check_internal_links(content),
            "has_external_links": self._check_external_links(content),
        }

        # Calculate overall SEO score
        seo_score = self._calculate_seo_score(
            keyword_metrics, readability_metrics, structure_metrics, content_type
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            keyword_metrics,
            readability_metrics,
            structure_metrics,
            content_type,
            target_keywords,
        )

        return {
            "overall_score": seo_score,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "keyword_metrics": keyword_metrics,
            "readability_metrics": readability_metrics,
            "structure_metrics": structure_metrics,
            "recommendations": recommendations,
        }

    def _analyze_keywords(
        self, content: str, target_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze keyword usage in content.

        Args:
            content: The content to analyze
            target_keywords: List of target keywords

        Returns:
            Dictionary with keyword metrics
        """
        # Tokenize content
        words = word_tokenize(content)
        words = [word.lower() for word in words if word.isalnum()]

        # Remove stop words
        filtered_words = [word for word in words if word not in self.stop_words]

        # Count words
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)

        # Analyze keyword density
        keyword_metrics = {}
        for keyword in target_keywords:
            # Handle multi-word keywords
            if " " in keyword:
                count = content.lower().count(keyword.lower())
            else:
                count = word_freq.get(keyword.lower(), 0)

            density = (count / total_words) * 100 if total_words > 0 else 0
            keyword_metrics[keyword] = {
                "count": count,
                "density": density,
                "in_title": keyword.lower() in content.split("\n")[0].lower()
                if content
                else False,
                "in_headings": any(
                    keyword.lower() in heading.lower()
                    for heading in re.findall(r"^#{1,3}\s+(.+)$", content, re.MULTILINE)
                ),
                "in_first_paragraph": keyword.lower()
                in content.split("\n\n")[0].lower()
                if content
                else False,
                "in_last_paragraph": keyword.lower()
                in content.split("\n\n")[-1].lower()
                if content
                else False,
                "optimal_density": 0.5 <= density <= 2.5,
            }

        # Calculate overall keyword score
        keyword_score = 0
        for metrics in keyword_metrics.values():
            if metrics["count"] > 0:
                keyword_score += 1
            if metrics["in_title"]:
                keyword_score += 2
            if metrics["in_headings"]:
                keyword_score += 1
            if metrics["in_first_paragraph"]:
                keyword_score += 1
            if metrics["optimal_density"]:
                keyword_score += 1

        # Normalize score to 0-100
        max_possible_score = len(keyword_metrics) * 6
        normalized_score = (
            (keyword_score / max_possible_score) * 100 if max_possible_score > 0 else 0
        )

        return {
            "keyword_score": normalized_score,
            "keywords": keyword_metrics,
            "top_terms": dict(word_freq.most_common(10)),
        }

    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """
        Analyze content readability.

        Args:
            content: The content to analyze

        Returns:
            Dictionary with readability metrics
        """
        # Tokenize content
        sentences = sent_tokenize(content)
        words = word_tokenize(content)
        words = [word for word in words if word.isalnum()]

        # Calculate basic metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Calculate syllable count and complex word count
        syllable_count = 0
        complex_word_count = 0

        for word in words:
            syllables = self._count_syllables(word)
            syllable_count += syllables
            if syllables >= 3:
                complex_word_count += 1

        # Calculate readability scores
        if word_count > 0 and sentence_count > 0:
            # Flesch Reading Ease
            flesch_reading_ease = (
                206.835
                - (1.015 * avg_sentence_length)
                - (84.6 * (syllable_count / word_count))
            )

            # Flesch-Kincaid Grade Level
            flesch_kincaid_grade = (
                0.39 * avg_sentence_length
                + 11.8 * (syllable_count / word_count)
                - 15.59
            )

            # Gunning Fog Index
            gunning_fog = 0.4 * (
                avg_sentence_length + 100 * (complex_word_count / word_count)
            )

            # SMOG Index
            smog = (
                1.043 * math.sqrt(complex_word_count * (30 / sentence_count)) + 3.1291
            )
        else:
            flesch_reading_ease = 0
            flesch_kincaid_grade = 0
            gunning_fog = 0
            smog = 0

        return {
            "flesch_reading_ease": flesch_reading_ease,
            "flesch_kincaid_grade": flesch_kincaid_grade,
            "gunning_fog": gunning_fog,
            "smog_index": smog,
            "avg_sentence_length": avg_sentence_length,
            "complex_word_percentage": (complex_word_count / word_count) * 100
            if word_count > 0
            else 0,
            "readability_score": self._calculate_readability_score(
                flesch_reading_ease, flesch_kincaid_grade, gunning_fog
            ),
        }

    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word.

        Args:
            word: The word to count syllables for

        Returns:
            Number of syllables
        """
        # Basic syllable counting algorithm
        word = word.lower()
        if len(word) <= 3:
            return 1

        # Remove 'es', 'ed' at the end
        word = re.sub(r"e$", "", word)
        word = re.sub(r"es$", "", word)
        word = re.sub(r"ed$", "", word)

        # Count vowel groups
        count = len(re.findall(r"[aeiouy]+", word))

        # Adjust for special cases
        if count == 0:
            count = 1

        return count

    def _check_meta_description(self, content: str) -> bool:
        """
        Check if content has a meta description.

        Args:
            content: The content to check

        Returns:
            True if meta description is found
        """
        # For markdown content, we'll look for a description section
        return bool(re.search(r"description:|meta description:", content.lower()))

    def _check_image_alt(self, content: str) -> bool:
        """
        Check if content has images with alt text.

        Args:
            content: The content to check

        Returns:
            True if images with alt text are found
        """
        # Look for markdown image syntax with alt text
        images = re.findall(r"!\[(.*?)\]", content)
        return any(img.strip() for img in images)

    def _check_internal_links(self, content: str) -> bool:
        """
        Check if content has internal links.

        Args:
            content: The content to check

        Returns:
            True if internal links are found
        """
        # Look for markdown link syntax
        return bool(re.search(r"\[.*?\]\((?!http).*?\)", content))

    def _check_external_links(self, content: str) -> bool:
        """
        Check if content has external links.

        Args:
            content: The content to check

        Returns:
            True if external links are found
        """
        # Look for markdown link syntax with http/https
        return bool(re.search(r"\[.*?\]\(https?://.*?\)", content))

    def _calculate_readability_score(
        self,
        flesch_reading_ease: float,
        flesch_kincaid_grade: float,
        gunning_fog: float,
    ) -> float:
        """
        Calculate overall readability score.

        Args:
            flesch_reading_ease: Flesch Reading Ease score
            flesch_kincaid_grade: Flesch-Kincaid Grade Level
            gunning_fog: Gunning Fog Index

        Returns:
            Normalized readability score (0-100)
        """
        # Normalize Flesch Reading Ease (0-100, higher is better)
        normalized_fre = min(max(flesch_reading_ease, 0), 100)

        # Normalize Flesch-Kincaid Grade (0-18, lower is better)
        normalized_fkg = max(0, min(18 - flesch_kincaid_grade, 18)) / 18 * 100

        # Normalize Gunning Fog (0-18, lower is better)
        normalized_fog = max(0, min(18 - gunning_fog, 18)) / 18 * 100

        # Average the normalized scores
        return (normalized_fre + normalized_fkg + normalized_fog) / 3

    def _calculate_seo_score(
        self,
        keyword_metrics: Dict[str, Any],
        readability_metrics: Dict[str, Any],
        structure_metrics: Dict[str, Any],
        content_type: str,
    ) -> float:
        """
        Calculate overall SEO score.

        Args:
            keyword_metrics: Keyword analysis metrics
            readability_metrics: Readability analysis metrics
            structure_metrics: Content structure metrics
            content_type: Type of content

        Returns:
            Overall SEO score (0-100)
        """
        # Get component scores
        keyword_score = keyword_metrics["keyword_score"]
        readability_score = readability_metrics["readability_score"]

        # Calculate structure score
        structure_score = 0
        if structure_metrics["has_title"]:
            structure_score += 15

        if 40 <= structure_metrics["title_length"] <= 60:
            structure_score += 10
        elif structure_metrics["title_length"] > 0:
            structure_score += 5

        if structure_metrics["h2_count"] >= 2:
            structure_score += 10
        elif structure_metrics["h2_count"] > 0:
            structure_score += 5

        if structure_metrics["h3_count"] >= 2:
            structure_score += 5

        if structure_metrics["has_meta_description"]:
            structure_score += 15

        if structure_metrics["has_image_alt"]:
            structure_score += 10

        if structure_metrics["has_internal_links"]:
            structure_score += 10

        if structure_metrics["has_external_links"]:
            structure_score += 10

        # Normalize structure score to 0-100
        structure_score = min(structure_score, 100)

        # Weight the scores based on content type
        if content_type == "blog_post":
            weights = {"keyword": 0.3, "readability": 0.3, "structure": 0.4}
        elif content_type == "landing_page":
            weights = {"keyword": 0.4, "readability": 0.2, "structure": 0.4}
        elif content_type == "product_description":
            weights = {"keyword": 0.5, "readability": 0.2, "structure": 0.3}
        else:
            weights = {"keyword": 0.33, "readability": 0.33, "structure": 0.34}

        # Calculate weighted score
        overall_score = (
            keyword_score * weights["keyword"]
            + readability_score * weights["readability"]
            + structure_score * weights["structure"]
        )

        return overall_score

    def _generate_recommendations(
        self,
        keyword_metrics: Dict[str, Any],
        readability_metrics: Dict[str, Any],
        structure_metrics: Dict[str, Any],
        content_type: str,
        target_keywords: List[str],
    ) -> List[str]:
        """
        Generate SEO recommendations based on analysis.

        Args:
            keyword_metrics: Keyword analysis metrics
            readability_metrics: Readability analysis metrics
            structure_metrics: Content structure metrics
            content_type: Type of content
            target_keywords: List of target keywords

        Returns:
            List of recommendations
        """
        recommendations = []

        # Keyword recommendations
        primary_keyword = target_keywords[0] if target_keywords else ""

        if primary_keyword and primary_keyword in keyword_metrics["keywords"]:
            keyword_data = keyword_metrics["keywords"][primary_keyword]

            if not keyword_data["in_title"]:
                recommendations.append(
                    f"Include the primary keyword '{primary_keyword}' in the title"
                )

            if not keyword_data["in_headings"]:
                recommendations.append(
                    f"Include the primary keyword '{primary_keyword}' in at least one heading"
                )

            if not keyword_data["in_first_paragraph"]:
                recommendations.append(
                    f"Include the primary keyword '{primary_keyword}' in the first paragraph"
                )

            if not keyword_data["optimal_density"]:
                if keyword_data["density"] < 0.5:
                    recommendations.append(
                        f"Increase the density of the primary keyword '{primary_keyword}' (currently {keyword_data['density']:.2f}%)"
                    )
                elif keyword_data["density"] > 2.5:
                    recommendations.append(
                        f"Decrease the density of the primary keyword '{primary_keyword}' to avoid keyword stuffing (currently {keyword_data['density']:.2f}%)"
                    )

        # Readability recommendations
        if readability_metrics["flesch_reading_ease"] < 60:
            recommendations.append(
                "Improve readability by using shorter sentences and simpler words"
            )

        if readability_metrics["avg_sentence_length"] > 20:
            recommendations.append(
                f"Reduce average sentence length (currently {readability_metrics['avg_sentence_length']:.1f} words)"
            )

        if readability_metrics["complex_word_percentage"] > 20:
            recommendations.append("Use simpler words to improve readability")

        # Structure recommendations
        if not structure_metrics["has_title"]:
            recommendations.append("Add a clear title to the content")
        elif structure_metrics["title_length"] < 40:
            recommendations.append(
                "Make the title longer (40-60 characters is optimal)"
            )
        elif structure_metrics["title_length"] > 60:
            recommendations.append("Shorten the title (40-60 characters is optimal)")

        if structure_metrics["h2_count"] < 2:
            recommendations.append("Add more H2 headings to structure your content")

        if not structure_metrics["has_meta_description"]:
            recommendations.append(
                "Add a meta description to improve search engine visibility"
            )

        if not structure_metrics["has_image_alt"]:
            recommendations.append("Add images with descriptive alt text")

        if not structure_metrics["has_internal_links"]:
            recommendations.append("Add internal links to other relevant content")

        if not structure_metrics["has_external_links"]:
            recommendations.append("Add external links to authoritative sources")

        # Content length recommendations
        word_count = structure_metrics.get("word_count", 0)
        if content_type == "blog_post" and word_count < 1000:
            recommendations.append(
                f"Increase content length (currently {word_count} words, aim for 1000+ words)"
            )
        elif content_type == "landing_page" and word_count < 500:
            recommendations.append(
                f"Increase content length (currently {word_count} words, aim for 500+ words)"
            )

        return recommendations

    def get_seo_improvement_prompt(
        self, analysis_results: Dict[str, Any], content: str
    ) -> str:
        """
        Generate a prompt for improving content SEO.

        Args:
            analysis_results: Results from SEO analysis
            content: Original content

        Returns:
            Prompt for improving SEO
        """
        recommendations = analysis_results["recommendations"]
        keyword_metrics = analysis_results["keyword_metrics"]

        prompt = f"""
        # SEO Improvement Task

        ## Original Content:
        {content}

        ## SEO Analysis Results:
        - Overall SEO Score: {analysis_results["overall_score"]:.1f}/100
        - Word Count: {analysis_results["word_count"]}
        - Readability Score: {analysis_results["readability_metrics"]["readability_score"]:.1f}/100

        ## Key Recommendations:
        {chr(10).join(f"- {rec}" for rec in recommendations)}

        ## Keyword Analysis:
        """

        for keyword, metrics in keyword_metrics["keywords"].items():
            prompt += f"""
            - Keyword: {keyword}
              - Count: {metrics["count"]}
              - Density: {metrics["density"]:.2f}%
              - In Title: {"Yes" if metrics["in_title"] else "No"}
              - In Headings: {"Yes" if metrics["in_headings"] else "No"}
              - In First Paragraph: {"Yes" if metrics["in_first_paragraph"] else "No"}
            """

        prompt += """
        ## Task:
        Rewrite the content to improve its SEO performance based on the analysis and recommendations above.
        Maintain the original message and purpose while optimizing for search engines.

        ## Important:
        - Implement all the recommendations listed above
        - Maintain the original tone and style
        - Ensure the content remains natural and reader-friendly
        - Do not sacrifice quality for keyword density

        ## Output:
        Provide only the improved content without explanations.
        """

        return prompt
