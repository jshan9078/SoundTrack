from pydantic import BaseModel
from typing import List

class VideoGenerateRequest(BaseModel):
    media_ids: List[str]  # List of media IDs in order
    music_prompt: str = "Exciting music at a competition. High tempo, rich harmonies. tension is building"
    negative_prompt: str = ""

class VideoGenerateResponse(BaseModel):
    message: str
    video_url: str
    media_ids: List[str]
