"""
Utility functions for video processing.
"""

import os
import cv2
import tempfile
from typing import List, Optional, Tuple
import numpy as np


def extract_frames(video_path: str, max_frames: int = 5) -> List[np.ndarray]:
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


def get_video_info(video_path: str) -> Tuple[int, float, Tuple[int, int]]:
    """
    Get information about a video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Tuple of (frame_count, duration_seconds, (width, height))
    """
    try:
        # Open the video file
        video = cv2.VideoCapture(video_path)
        
        # Check if video opened successfully
        if not video.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        # Release the video
        video.release()
        
        return frame_count, duration, (width, height)
    
    except Exception as e:
        print(f"Error getting video info: {e}")
        return 0, 0.0, (0, 0)


def save_frame_as_image(frame: np.ndarray, output_path: str) -> bool:
    """
    Save a frame as an image file.
    
    Args:
        frame: Frame as numpy array
        output_path: Path to save the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert from RGB to BGR (OpenCV uses BGR by default)
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Save the frame as an image
        cv2.imwrite(output_path, bgr_frame)
        
        return True
    
    except Exception as e:
        print(f"Error saving frame as image: {e}")
        return False


def create_video_thumbnail(video_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Create a thumbnail from a video file.
    
    Args:
        video_path: Path to the video file
        output_path: Path to save the thumbnail (optional)
        
    Returns:
        Path to the thumbnail if successful, None otherwise
    """
    try:
        # Extract the first frame
        frames = extract_frames(video_path, max_frames=1)
        
        if not frames:
            return None
        
        # If output_path is not provided, create a temporary file
        if not output_path:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
                output_path = temp.name
        
        # Save the frame as an image
        if save_frame_as_image(frames[0], output_path):
            return output_path
        
        return None
    
    except Exception as e:
        print(f"Error creating video thumbnail: {e}")
        return None
