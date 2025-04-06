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
    ENTHUSIASTIC = "enthusiastic"
    INFORMATIVE = "informative"
    PERSUASIVE = "persuasive"
    HUMOROUS = "humorous"
    FORMAL = "formal"
    CASUAL = "casual"


class AudienceType(str, Enum):
    GENERAL = "general"
    TECHNICAL = "technical"
    BUSINESS = "business"
    CONSUMER = "consumer"
    EXPERT = "expert"
    BEGINNER = "beginner"
    YOUTH = "youth"
    SENIOR = "senior"


class ContentRequest(BaseModel):
    content_type: ContentType = Field(..., description="Type of content to generate")
    topic: str = Field(..., description="Main topic or subject of the content")
    tone: ToneType = Field(default=ToneType.CONVERSATIONAL, description="Tone of the content")
    audience: AudienceType = Field(default=AudienceType.GENERAL, description="Target audience for the content")
    keywords: List[str] = Field(default_factory=list, description="Keywords to include in the content")
    word_count: Optional[int] = Field(default=None, description="Target word count for the content")
    include_research: bool = Field(default=True, description="Whether to include web research")
    custom_instructions: Optional[str] = Field(default=None, description="Additional custom instructions")
    references: Optional[List[str]] = Field(default=None, description="URLs or sources to reference")
    
    class Config:
        use_enum_values = True


class ResearchResult(BaseModel):
    source: str
    title: str
    snippet: str
    url: str


class ContentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    research_results: Optional[List[ResearchResult]] = Field(default=None)
