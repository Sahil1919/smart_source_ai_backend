from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import search, youtube, health
from fastapi.openapi.docs import get_redoc_html

# Include routers


def init_routers(app_: FastAPI) -> None:
    app_.include_router(health.router)
    app_.include_router(search.router)
    app_.include_router(youtube.router)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Smart Source AI API",
    description="API for web search and YouTube video analysis",
    version="1.0.0",
        docs_url=None,
        redoc_url=None
    )
    app_.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    init_routers(app_=app_)


    @app_.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url="/openapi.json",
             title="Smart Source AI API",
        )
    
    return app_


app = create_app()
