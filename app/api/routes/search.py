from fastapi import APIRouter, HTTPException
from app.models.schemas.search import WebSearchQuery, WebSearchResult
from app.services.search_service import SearchService  # Import the instance
from core.config import settings

router = APIRouter(
    prefix=f"{settings.API_V1_STR}/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=WebSearchResult)
async def search(query: WebSearchQuery):
    """
    Perform a web search based on the provided query
    """
    try:
        result = SearchService().perform_search_operation(query.query)
        return WebSearchResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")
