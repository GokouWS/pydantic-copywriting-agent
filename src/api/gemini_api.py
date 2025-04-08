"""
Integration with Google's Gemini API for content generation and video analysis.
"""

import os
import base64
from typing import List, Dict, Any, Optional, Union
import google.generativeai as genai
from PIL import Image
import io


class GeminiAPI:
    """Integration with Google's Gemini API for content generation and video analysis."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "models/gemini-2.0-pro-exp-02-05",
    ):
        """
        Initialize the Gemini API client.

        Args:
            api_key: Google API key (optional, will use environment variable if not provided)
            model_name: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key is required. Set GOOGLE_API_KEY environment variable or provide it directly."
            )

        self.model_name = model_name

        # Configure the API
        genai.configure(api_key=self.api_key)

    def generate_content(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate text content using Gemini.

        Args:
            prompt: The prompt to send to Gemini
            temperature: Creativity level (0.0 to 1.0)

        Returns:
            Generated content as string
        """
        try:
            # Initialize the model
            model = genai.GenerativeModel(self.model_name)

            # Generate content
            response = model.generate_content(
                prompt, generation_config={"temperature": temperature}
            )

            return response.text
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            raise

    def analyze_images(self, images: List[Union[str, bytes]], prompt: str) -> str:
        """
        Analyze images using Gemini's multimodal capabilities.

        Args:
            images: List of image paths or bytes
            prompt: The prompt to send to Gemini along with the images

        Returns:
            Analysis results as string
        """
        try:
            # Initialize the model
            model = genai.GenerativeModel(self.model_name)

            # Process images
            processed_images = []
            for img in images:
                if isinstance(img, str):
                    # It's a file path
                    with open(img, "rb") as f:
                        image_bytes = f.read()
                    processed_images.append(genai.Image.from_bytes(image_bytes))
                else:
                    # It's already bytes
                    processed_images.append(genai.Image.from_bytes(img))

            # Generate content with images
            response = model.generate_content([prompt, *processed_images])

            return response.text
        except Exception as e:
            print(f"Error analyzing images with Gemini: {e}")
            raise

    def analyze_video_frames(self, frames: List[bytes], prompt: str) -> str:
        """
        Analyze video frames using Gemini's multimodal capabilities.

        Args:
            frames: List of video frame bytes
            prompt: The prompt to send to Gemini along with the frames

        Returns:
            Analysis results as string
        """
        try:
            # Initialize the model
            model = genai.GenerativeModel(self.model_name)

            # Process frames
            processed_frames = [genai.Image.from_bytes(frame) for frame in frames]

            # Generate content with frames
            response = model.generate_content([prompt, *processed_frames])

            return response.text
        except Exception as e:
            print(f"Error analyzing video frames with Gemini: {e}")
            raise

    def get_instagram_reel_content(
        self, frames: List[bytes], keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Generate Instagram Reel content based on video frames.

        Args:
            frames: List of video frame bytes
            keywords: List of target keywords

        Returns:
            Dictionary with caption, hashtags, and recommendations
        """
        prompt = f"""
        Analyze these video frames from an Instagram Reel and create:

        1. An engaging caption (max 2200 characters) that will drive engagement
        2. A set of 15-30 relevant hashtags that will maximize discoverability
        3. 5 specific recommendations to improve the video's performance

        Target keywords: {", ".join(keywords)}

        Format your response as follows:
        CAPTION:
        [Your caption here]

        HASHTAGS:
        [hashtag1] [hashtag2] [hashtag3] ...

        RECOMMENDATIONS:
        1. [First recommendation]
        2. [Second recommendation]
        3. [Third recommendation]
        4. [Fourth recommendation]
        5. [Fifth recommendation]
        """

        response = self.analyze_video_frames(frames, prompt)

        # Parse the response
        caption = ""
        hashtags = []
        recommendations = []

        current_section = None
        for line in response.split("\n"):
            line = line.strip()
            if line == "CAPTION:":
                current_section = "caption"
            elif line == "HASHTAGS:":
                current_section = "hashtags"
            elif line == "RECOMMENDATIONS:":
                current_section = "recommendations"
            elif (
                current_section == "caption"
                and line
                and not line.startswith("HASHTAGS:")
            ):
                caption += line + "\n"
            elif (
                current_section == "hashtags"
                and line
                and not line.startswith("RECOMMENDATIONS:")
            ):
                # Extract hashtags from the line
                for word in line.split():
                    if word.startswith("#"):
                        hashtags.append(word)
            elif current_section == "recommendations" and line:
                # Check if line starts with a number followed by a period
                if line[0].isdigit() and line[1:].startswith(". "):
                    recommendations.append(line[3:])  # Remove the number and period

        return {
            "caption": caption.strip(),
            "hashtags": hashtags,
            "recommendations": recommendations,
        }

    def get_youtube_shorts_content(
        self, frames: List[bytes], keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Generate YouTube Shorts content based on video frames.

        Args:
            frames: List of video frame bytes
            keywords: List of target keywords

        Returns:
            Dictionary with title, description, hashtags, and recommendations
        """
        prompt = f"""
        Analyze these video frames from a YouTube Short and create:

        1. An attention-grabbing title (max 100 characters)
        2. An SEO-optimized description (max 500 characters)
        3. A set of 3-5 relevant hashtags that will maximize discoverability
        4. 5 specific recommendations to improve the video's performance

        Target keywords: {", ".join(keywords)}

        Format your response as follows:
        TITLE:
        [Your title here]

        DESCRIPTION:
        [Your description here]

        HASHTAGS:
        [hashtag1] [hashtag2] [hashtag3] ...

        RECOMMENDATIONS:
        1. [First recommendation]
        2. [Second recommendation]
        3. [Third recommendation]
        4. [Fourth recommendation]
        5. [Fifth recommendation]
        """

        response = self.analyze_video_frames(frames, prompt)

        # Parse the response
        title = ""
        description = ""
        hashtags = []
        recommendations = []

        current_section = None
        for line in response.split("\n"):
            line = line.strip()
            if line == "TITLE:":
                current_section = "title"
            elif line == "DESCRIPTION:":
                current_section = "description"
            elif line == "HASHTAGS:":
                current_section = "hashtags"
            elif line == "RECOMMENDATIONS:":
                current_section = "recommendations"
            elif (
                current_section == "title"
                and line
                and not line.startswith("DESCRIPTION:")
            ):
                title = line
            elif (
                current_section == "description"
                and line
                and not line.startswith("HASHTAGS:")
            ):
                description += line + "\n"
            elif (
                current_section == "hashtags"
                and line
                and not line.startswith("RECOMMENDATIONS:")
            ):
                # Extract hashtags from the line
                for word in line.split():
                    if word.startswith("#"):
                        hashtags.append(word)
            elif current_section == "recommendations" and line:
                # Check if line starts with a number followed by a period
                if line[0].isdigit() and line[1:].startswith(". "):
                    recommendations.append(line[3:])  # Remove the number and period

        return {
            "title": title,
            "description": description.strip(),
            "hashtags": hashtags,
            "recommendations": recommendations,
        }
