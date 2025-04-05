from fastapi import APIRouter
from core.config import settings
from app.models.schemas.health import HealthCheck

router = APIRouter(
    prefix=f"{settings.API_V1_STR}/health",
    tags=["Health"],
)

@router.get("/", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "healthy", "message": "API is running"}
