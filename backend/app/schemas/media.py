from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MediaBase(BaseModel):
    type: str
    storage_url: str
    thumb_url: Optional[str] = None
    duration_sec: Optional[int] = None
    summary: Optional[str] = None
    elements: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    mood: Optional[str] = None
    song: Optional[str] = None
    song_artist: Optional[str] = None
    embed: Optional[str] = None
    user_mood: Optional[str] = None

class MediaCreate(MediaBase):
    pass

class MediaAnalyzeRequest(BaseModel):
    storage_url: str
    type: str

class MediaUpdate(BaseModel):
    summary: Optional[str] = None
    elements: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class MediaResponse(MediaBase):
    id: str
    ts: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SongRecommendation(BaseModel):
    name: str
    artist: str

class SongRecommendationResponse(BaseModel):
    message: str
    media_id: str
    recommendation: SongRecommendation
    context: dict