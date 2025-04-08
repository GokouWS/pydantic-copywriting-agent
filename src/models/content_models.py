"""
Data models for the AI copywriting agent.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ContentType(str, Enum):
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    LANDING_PAGE = "landing_page"
    PRODUCT_DESCRIPTION = "product_description"
    AD_COPY = "ad_copy"
    PRESS_RELEASE = "press_release"
    CUSTOM = "custom"


class ToneType(str, Enum):
    PROFESSIONAL = "professional"
    CONVERSATIONAL = "conversational"
    PERSUASIVE = "persuasive"
    INFORMATIVE = "informative"
    ENTHUSIASTIC = "enthusiastic"
    HUMOROUS = "humorous"
    FORMAL = "formal"
    CASUAL = "casual"


class AudienceType(str, Enum):
    GENERAL = "general"
    BUSINESS = "business"
    TECHNICAL = "technical"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    CONSUMER = "consumer"
    EXPERT = "expert"
    BEGINNER = "beginner"


class SocialPlatform(str, Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TIKTOK = "tiktok"


class VideoContentType(str, Enum):
    INSTAGRAM_REEL = "instagram_reel"
    YOUTUBE_SHORT = "youtube_short"
    TIKTOK = "tiktok"


class ResearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str


class ContentRequest(BaseModel):
    content_type: ContentType
    topic: str
    tone: ToneType
    audience: AudienceType
    keywords: Optional[List[str]] = None
    word_count: int = 500
    include_research: bool = False
    custom_instructions: Optional[str] = None
    social_platform: Optional[SocialPlatform] = None


class VideoAnalysisRequest(BaseModel):
    video_path: str
    content_type: VideoContentType
    keywords: Optional[List[str]] = None
    caption_length: int = 100
    custom_instructions: Optional[str] = None


class VideoAnalysisResult(BaseModel):
    caption: str
    hashtags: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]


class ContentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any]
    research_results: Optional[List[ResearchResult]] = None
