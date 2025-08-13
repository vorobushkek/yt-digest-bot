"""Main FastAPI application for YouTube Digest Bot."""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn
from app.config import settings
from app.database.models import init_db
from app.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Initialize database
    await init_db()
    yield


# Create FastAPI application
app = FastAPI(
    title="YouTube Digest Bot API",
    description="REST API for YouTube Digest Bot with Telegram integration",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "YouTube Digest Bot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        reload=settings.FASTAPI_DEBUG
    )
