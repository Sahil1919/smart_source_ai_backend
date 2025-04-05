from fastapi import APIRouter, HTTPException
from app.models.schemas.youtube import (
    YouTubeSearchQuery, 
    YouTubeSearchResult, 
    YouTubeVideo,
    YouTubeSummaryRequest,
    YouTubeSummaryResult
)
from app.services.youtube_service import YouTubeService  # Import the instance
from core.config import settings

router = APIRouter(
    prefix=f"{settings.API_V1_STR}/youtube",
    tags=["YouTube"],
    responses={404: {"description": "Not found"}},
)

@router.post("/search", response_model=YouTubeSearchResult)
async def youtube_search(query: YouTubeSearchQuery):
    """
    Search YouTube for videos matching the search term
    """
    try:
        results = YouTubeService().search_videos(query.search_term)
        videos = []
        
        for result in results:
            video = YouTubeVideo(
                id=result['id'],
                title=result['title'],
                url=f"https://www.youtube.com/watch?v={result['id']}"
            )
            videos.append(video)
        
        return YouTubeSearchResult(
            search_term=query.search_term,
            videos=videos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching YouTube: {str(e)}")

@router.post("/summarize", response_model=YouTubeSummaryResult)
async def youtube_summarize(request: YouTubeSummaryRequest):
    """
    Generate a summary of a YouTube video
    """
    try:
        summary = YouTubeService().summarize_video(request.video_url)
        return YouTubeSummaryResult(
            video_url=request.video_url,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing video: {str(e)}")
