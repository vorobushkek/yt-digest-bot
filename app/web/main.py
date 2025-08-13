import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YT Digest Bot",
    description="YouTube Digest Telegram Bot API - Render Optimized",
    version="1.0.0"
)

# Environment variables
X_CRON_KEY = os.getenv("X_CRON_KEY", "default_cron_key")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Pydantic models
class WebhookUpdate(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

class DigestRequest(BaseModel):
    channel_id: Optional[str] = None
    limit: Optional[int] = 10

@app.get("/")
async def root():
    """Health check endpoint for Render"""
    return {
        "status": "healthy",
        "service": "yt-digest-bot",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "bot_configured": bool(BOT_TOKEN),
        "webhook_configured": bool(WEBHOOK_URL)
    }

@app.post("/webhook")
async def webhook(update: WebhookUpdate):
    """Telegram webhook endpoint"""
    try:
        logger.info(f"Received webhook update: {update.update_id}")
        
        # Process the update here
        # This is where you'd add your bot logic
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/cron/digest")
async def trigger_digest(
    digest_request: DigestRequest,
    x_cron_key: str = Header(alias="X-CRON-KEY")
):
    """Cron endpoint for digest generation"""
    if x_cron_key != X_CRON_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        logger.info(f"Triggering digest for channel: {digest_request.channel_id}")
        
        # This is where you'd add your digest generation logic
        
        return {
            "status": "success",
            "message": "Digest generation triggered",
            "channel_id": digest_request.channel_id,
            "limit": digest_request.limit
        }
    except Exception as e:
        logger.error(f"Error generating digest: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate digest")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("YT Digest Bot API starting up...")
    if not BOT_TOKEN:
        logger.warning("BOT_TOKEN not configured")
    if not WEBHOOK_URL:
        logger.warning("WEBHOOK_URL not configured")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("YT Digest Bot API shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
