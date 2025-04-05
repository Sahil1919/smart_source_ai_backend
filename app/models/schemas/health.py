
from pydantic import BaseModel

class HealthCheck(BaseModel):
    status: str = "healthy"
    message: str = "API is running"

