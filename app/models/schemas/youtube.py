from pydantic import BaseModel
from typing import List

class YouTubeSearchQuery(BaseModel):
    search_term: str

class YouTubeVideo(BaseModel):
    id: str
    title: str
    url: str

class YouTubeSearchResult(BaseModel):
    search_term: str
    videos: List[YouTubeVideo]

class YouTubeSummaryRequest(BaseModel):
    video_url: str

class YouTubeSummaryResult(BaseModel):
    video_url: str
    summary: str
