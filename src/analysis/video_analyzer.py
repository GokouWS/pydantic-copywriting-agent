"""
Video analysis functionality for social media content optimization.
"""

import os
import cv2
import tempfile
from typing import List, Dict, Any, Optional, Union
import numpy as np
from src.api.gemini_api import GeminiAPI
from src.api.brave_search import BraveSearchAPI
from src.models.content_models import VideoContentType, VideoAnalysisResult


class VideoAnalyzer:
    """Analyzes video content for social media optimization."""

    def __init__(
        self,
        gemini_api: Optional[GeminiAPI] = None,
        brave_api: Optional[BraveSearchAPI] = None,
    ):
        """
        Initialize the video analyzer.

        Args:
            gemini_api: GeminiAPI instance (optional)
            brave_api: BraveSearchAPI instance (optional)
        """
        self.gemini_api = gemini_api or GeminiAPI()
        self.brave_api = brave_api or BraveSearchAPI()

    def analyze_video(
        self,
        video_path: str,
        content_type: VideoContentType,
        keywords: List[str] = None,
        max_frames: int = 5,
        custom_instructions: str = None,
    ) -> VideoAnalysisResult:
        """
        Analyze video content and generate platform-specific captions and hashtags.

        Args:
            video_path: Path to the video file
            content_type: Type of video content (instagram_reel, youtube_short, etc.)
            keywords: List of target keywords
            max_frames: Maximum number of frames to extract

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

        # Generate content based on content type
        if content_type == VideoContentType.INSTAGRAM_REEL:
            result = self.gemini_api.get_instagram_reel_content(
                frame_bytes, keywords or []
            )

            # Combine generated hashtags with trending hashtags
            all_hashtags = list(set(result["hashtags"] + trending_hashtags))

            # Limit to 30 hashtags (Instagram limit)
            if len(all_hashtags) > 30:
                all_hashtags = all_hashtags[:30]

            return VideoAnalysisResult(
                caption=result["caption"],
                hashtags=all_hashtags,
                recommendations=result["recommendations"],
                metadata={
                    "platform": "instagram",
                    "content_type": "reel",
                    "frame_count": len(frames),
                    "keywords": keywords or [],
                },
            )

        elif content_type == VideoContentType.YOUTUBE_SHORT:
            result = self.gemini_api.get_youtube_shorts_content(
                frame_bytes, keywords or []
            )

            # Combine title and description for the caption
            caption = f"{result['title']}\n\n{result['description']}"

            # Combine generated hashtags with trending hashtags
            all_hashtags = list(set(result["hashtags"] + trending_hashtags))

            # Limit to 15 hashtags (reasonable for YouTube)
            if len(all_hashtags) > 15:
                all_hashtags = all_hashtags[:15]

            return VideoAnalysisResult(
                caption=caption,
                hashtags=all_hashtags,
                recommendations=result["recommendations"],
                metadata={
                    "platform": "youtube",
                    "content_type": "short",
                    "title": result["title"],
                    "description": result["description"],
                    "frame_count": len(frames),
                    "keywords": keywords or [],
                },
            )

        else:
            # Default to Instagram Reel if content type is not recognized
            result = self.gemini_api.get_instagram_reel_content(
                frame_bytes, keywords or []
            )

            return VideoAnalysisResult(
                caption=result["caption"],
                hashtags=result["hashtags"],
                recommendations=result["recommendations"],
                metadata={
                    "platform": "unknown",
                    "content_type": str(content_type),
                    "frame_count": len(frames),
                    "keywords": keywords or [],
                },
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
                frame_indices = [
                    int(i * total_frames / max_frames) for i in range(max_frames)
                ]

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

    def _get_trending_hashtags(
        self, keywords: Optional[List[str]], platform: str
    ) -> List[str]:
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
