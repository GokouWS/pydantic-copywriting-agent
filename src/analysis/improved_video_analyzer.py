"""
Improved video analysis functionality for social media content optimization.
"""

import os
import cv2
import tempfile
from typing import List, Dict, Any, Optional, Union
import numpy as np
from src.api.gemini_api import GeminiAPI
from src.api.brave_search import BraveSearchAPI
from src.models.content_models import VideoContentType, VideoAnalysisResult


class ImprovedVideoAnalyzer:
    """Analyzes video content for social media optimization with improved prompting."""
    
    def __init__(self, gemini_api: Optional[GeminiAPI] = None, brave_api: Optional[BraveSearchAPI] = None):
        """
        Initialize the video analyzer.
        
        Args:
            gemini_api: GeminiAPI instance (optional)
            brave_api: BraveSearchAPI instance (optional)
        """
        self.gemini_api = gemini_api or GeminiAPI()
        self.brave_api = brave_api or BraveSearchAPI()
    
    def analyze_video(
        self, video_path: str, content_type: VideoContentType, 
        keywords: List[str] = None, max_frames: int = 5,
        custom_instructions: str = None
    ) -> VideoAnalysisResult:
        """
        Analyze video content and generate platform-specific captions and hashtags.
        
        Args:
            video_path: Path to the video file
            content_type: Type of video content (instagram_reel, youtube_short, etc.)
            keywords: List of target keywords
            max_frames: Maximum number of frames to extract
            custom_instructions: Additional instructions for content generation
            
        Returns:
            VideoAnalysisResult with generated content
        """
        # Extract frames from the video
        frames = self._extract_frames(video_path, max_frames)
        
        # Convert frames to bytes for Gemini API
        frame_bytes = [self._frame_to_bytes(frame) for frame in frames]
        
        # Get trending hashtags for the keywords
        platform = self._get_platform_from_content_type(content_type)
        trending_hashtags = self._get_trending_hashtags(keywords, platform)
        
        # Create a form data dictionary for the prompt
        form_data = {
            "keywords": keywords or [],
            "caption_length": 2200 if content_type == VideoContentType.INSTAGRAM_REEL else 500,
            "custom_instructions": custom_instructions
        }
        
        # Create an improved prompt for video analysis
        prompt = self._create_video_analysis_prompt(form_data, content_type)
        
        # Send the frames and prompt to Gemini API
        response = self.gemini_api.analyze_video_frames(frame_bytes, prompt)
        
        # Parse the response
        result = self._parse_video_analysis_response(response, content_type)
        
        # Combine generated hashtags with trending hashtags
        all_hashtags = list(set(result["hashtags"] + trending_hashtags))
        
        # Limit hashtags based on platform
        if content_type == VideoContentType.INSTAGRAM_REEL and len(all_hashtags) > 30:
            all_hashtags = all_hashtags[:30]  # Instagram limit
        elif content_type == VideoContentType.YOUTUBE_SHORT and len(all_hashtags) > 15:
            all_hashtags = all_hashtags[:15]  # YouTube reasonable limit
        
        # Create metadata based on content type
        metadata = {
            "platform": platform,
            "content_type": content_type.value,
            "frame_count": len(frames),
            "keywords": keywords or []
        }
        
        # Add additional metadata for YouTube Shorts
        if content_type == VideoContentType.YOUTUBE_SHORT and "title" in result:
            metadata["title"] = result["title"]
            metadata["description"] = result["description"]
        
        return VideoAnalysisResult(
            caption=result["caption"],
            hashtags=all_hashtags,
            recommendations=result["recommendations"],
            metadata=metadata
        )
    
    def _extract_frames(self, video_path: str, max_frames: int = 5) -> List[np.ndarray]:
        """
        Extract frames from a video file.
        
        Args:
            video_path: Path to the video file
            max_frames: Maximum number of frames to extract
            
        Returns:
            List of frames as numpy arrays
        """
        frames = []
        
        try:
            # Open the video file
            video = cv2.VideoCapture(video_path)
            
            # Check if video opened successfully
            if not video.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = video.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps if fps > 0 else 0
            
            # Calculate frame indices to extract
            if total_frames <= max_frames:
                # If video has fewer frames than max_frames, use all frames
                frame_indices = list(range(total_frames))
            else:
                # Otherwise, extract frames at regular intervals
                frame_indices = [int(i * total_frames / max_frames) for i in range(max_frames)]
            
            # Extract frames
            for idx in frame_indices:
                video.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = video.read()
                if ret:
                    # Convert from BGR to RGB (OpenCV uses BGR by default)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame)
            
            # Release the video
            video.release()
            
            return frames
        
        except Exception as e:
            print(f"Error extracting frames from video: {e}")
            return []
    
    def _frame_to_bytes(self, frame: np.ndarray) -> bytes:
        """
        Convert a frame (numpy array) to bytes.
        
        Args:
            frame: Frame as numpy array
            
        Returns:
            Frame as bytes
        """
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
                temp_filename = temp.name
            
            # Save the frame as JPEG
            cv2.imwrite(temp_filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            
            # Read the file as bytes
            with open(temp_filename, "rb") as f:
                frame_bytes = f.read()
            
            # Delete the temporary file
            os.unlink(temp_filename)
            
            return frame_bytes
        
        except Exception as e:
            print(f"Error converting frame to bytes: {e}")
            return b""
    
    def _get_platform_from_content_type(self, content_type: VideoContentType) -> str:
        """
        Get the platform name from content type.
        
        Args:
            content_type: Type of video content
            
        Returns:
            Platform name
        """
        if content_type == VideoContentType.INSTAGRAM_REEL:
            return "instagram"
        elif content_type == VideoContentType.YOUTUBE_SHORT:
            return "youtube"
        elif content_type == VideoContentType.TIKTOK:
            return "tiktok"
        else:
            return "all"
    
    def _parse_video_analysis_response(self, response: str, content_type: VideoContentType) -> Dict[str, Any]:
        """
        Parse the response from Gemini API for video analysis.
        
        Args:
            response: Response text from Gemini API
            content_type: Type of video content
            
        Returns:
            Dictionary with parsed results
        """
        # Initialize default result structure
        result = {
            "caption": "",
            "hashtags": [],
            "recommendations": []
        }
        
        # Add title and description for YouTube Shorts
        if content_type == VideoContentType.YOUTUBE_SHORT:
            result["title"] = ""
            result["description"] = ""
        
        # Parse the response based on sections
        current_section = None
        caption_lines = []
        hashtags = []
        recommendations = []
        title = ""
        description_lines = []
        
        for line in response.split('\n'):
            line = line.strip()
            
            # Identify sections
            if "VIDEO ANALYSIS:" in line.upper():
                current_section = "analysis"
                continue
            elif "CAPTION:" in line.upper():
                current_section = "caption"
                continue
            elif "TITLE:" in line.upper() and content_type == VideoContentType.YOUTUBE_SHORT:
                current_section = "title"
                continue
            elif "DESCRIPTION:" in line.upper() and content_type == VideoContentType.YOUTUBE_SHORT:
                current_section = "description"
                continue
            elif "HASHTAGS:" in line.upper():
                current_section = "hashtags"
                continue
            elif "PERFORMANCE RECOMMENDATIONS:" in line.upper() or "RECOMMENDATIONS:" in line.upper():
                current_section = "recommendations"
                continue
            
            # Skip empty lines or section headers
            if not line or line.startswith('#'):
                continue
            
            # Process content based on current section
            if current_section == "caption":
                caption_lines.append(line)
            elif current_section == "title":
                title = line
            elif current_section == "description":
                description_lines.append(line)
            elif current_section == "hashtags":
                # Extract hashtags from the line
                for word in line.split():
                    if word.startswith('#'):
                        hashtags.append(word)
            elif current_section == "recommendations":
                # Check if line starts with a number or dash
                if (line[0].isdigit() and line[1:].startswith('. ')) or line.startswith('- '):
                    # Remove the number/dash and period
                    if line[0].isdigit():
                        clean_line = line[line.index('.')+1:].strip()
                    else:
                        clean_line = line[1:].strip()
                    recommendations.append(clean_line)
                elif recommendations:  # Continue previous recommendation if not a new one
                    recommendations[-1] += " " + line
        
        # Combine parsed content
        result["caption"] = "\n".join(caption_lines).strip()
        result["hashtags"] = hashtags
        result["recommendations"] = recommendations
        
        # For YouTube Shorts, add title and description
        if content_type == VideoContentType.YOUTUBE_SHORT:
            result["title"] = title
            result["description"] = "\n".join(description_lines).strip()
            
            # If no separate title/description was found, split the caption
            if not result["title"] and "\n" in result["caption"]:
                parts = result["caption"].split("\n", 1)
                result["title"] = parts[0]
                result["description"] = parts[1] if len(parts) > 1 else ""
        
        return result
    
    def _get_trending_hashtags(self, keywords: Optional[List[str]], platform: str) -> List[str]:
        """
        Get trending hashtags for keywords on a specific platform.
        
        Args:
            keywords: List of target keywords
            platform: Social media platform
            
        Returns:
            List of trending hashtags
        """
        if not keywords:
            return []
        
        # Combine keywords into a topic
        topic = " ".join(keywords[:3])  # Use first 3 keywords
        
        # Get trending hashtags
        hashtags = self.brave_api.get_trending_hashtags(topic, platform)
        
        return hashtags
    
    def _create_video_analysis_prompt(self, form_data, content_type):
        """Create an improved prompt for video analysis using advanced prompting techniques."""
        
        # Define the persona based on content type
        persona = {
            "instagram_reel": "a social media strategist specializing in Instagram growth with 8+ years of experience",
            "youtube_short": "a YouTube optimization expert who has helped creators reach millions of views",
            "tiktok": "a TikTok content strategist who understands viral trends and audience engagement"
        }.get(content_type.value, "a social media content expert")
        
        # Create platform-specific instructions
        platform_instructions = {
            "instagram_reel": """
            - Create a caption that's engaging but concise (max 2200 characters)
            - Focus on storytelling elements that create emotional connection
            - Include a question or call-to-action to boost comments
            - Suggest 20-30 hashtags organized by popularity (mix of broad, niche, and trending)
            - Recommend optimal posting times based on content theme
            """,
            
            "youtube_short": """
            - Create an attention-grabbing title (max 60 characters)
            - Write a description that front-loads keywords (max 300 characters)
            - Include 3-5 highly relevant hashtags
            - Suggest end screens and cards to drive further engagement
            - Recommend related video ideas to create a content series
            """,
            
            "tiktok": """
            - Create a short, punchy caption with strong hook
            - Include 3-5 trending hashtags plus 2-3 niche hashtags
            - Suggest trending sounds that could complement the video
            - Recommend follow-up content ideas to boost profile growth
            - Include ideas for text overlay to improve retention
            """
        }.get(content_type.value, "")
        
        # Create a more specific and detailed prompt using best practices
        prompt = f"""
        # Video Content Analysis Request

        ## Your Role:
        You are {persona}. Your task is to analyze the provided video frames and create optimized content that will maximize engagement, reach, and conversion for {content_type.value}.

        ## Video Content Specifications:
        - **Platform:** {content_type.value}
        - **Keywords/Topics:** {', '.join(form_data["keywords"]) if form_data["keywords"] else 'No specific keywords provided'}
        - **Target Caption Length:** {form_data["caption_length"]} characters
        {f"- **Additional Context:** {form_data['custom_instructions']}" if form_data.get("custom_instructions") else ""}

        ## Platform-Specific Requirements:
        {platform_instructions}

        ## Analysis Process:
        1. First, carefully analyze the video frames to understand:
           - The main subject/focus of the video
           - The apparent action or activity taking place
           - The mood, tone, and aesthetic of the content
           - Any text or recognizable elements visible
           - The likely target audience based on visual cues

        2. Based on your analysis, create:
           - A strategic caption that will drive engagement
           - Relevant hashtags organized by reach potential
           - Specific recommendations to improve performance

        ## Engagement Optimization:
        - Include pattern interrupts or curiosity hooks to stop the scroll
        - Create a sense of authenticity and relatability
        - Use emotional triggers appropriate to the content
        - Incorporate trending elements without forcing irrelevant content
        - Suggest ways to encourage shares, saves, and comments

        ## Output Format:
        Structure your response in the following format:

        **VIDEO ANALYSIS:**
        [Provide a brief analysis of what you observe in the video frames]

        **CAPTION:**
        [The complete caption, optimized for the platform]

        **HASHTAGS:**
        [List of recommended hashtags, organized by category]

        **PERFORMANCE RECOMMENDATIONS:**
        [5 specific, actionable recommendations to improve engagement]

        ## Important Guidelines:
        - Be specific and actionable in your recommendations
        - Avoid generic advice that could apply to any video
        - Consider current platform algorithm preferences
        - Focus on authentic engagement rather than gimmicks
        - Ensure all suggestions align with the actual video content
        """
        
        return prompt
