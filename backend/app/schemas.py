from pydantic import BaseModel
from typing import Optional, List

class Video(BaseModel):
    id: str
    title: str
    description: str
    thumbnail: str
    channel: str
    duration: str
    views: Optional[int] = None

class Recommendation(BaseModel):
    video: Video
    reason: str

class MoodRecommendation(BaseModel):
    mood: str
    videos: List[Recommendation]