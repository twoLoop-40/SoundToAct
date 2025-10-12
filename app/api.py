"""
FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.models import (
    KeywordActionCreate,
    KeywordActionResponse,
    ListenRequest,
    ListenResponse,
    StatusResponse,
)
from app.voice_listener import VoiceListener
from app.actions import action_registry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global voice listener instance
voice_listener: VoiceListener = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global voice_listener
    voice_listener = VoiceListener()
    logger.info("VoiceListener initialized")
    yield
    logger.info("Shutting down VoiceListener")


app = FastAPI(
    title="SoundToAct API",
    description="Voice-triggered automation API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SoundToAct API",
        "docs": "/docs",
        "version": "0.1.0",
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current listener status"""
    return StatusResponse(
        is_listening=voice_listener.is_listening,
        registered_keywords=voice_listener.get_registered_keywords(),
        message="Voice listener status retrieved successfully",
    )


@app.post("/keywords", response_model=KeywordActionResponse)
async def create_keyword_action(keyword_action: KeywordActionCreate):
    """Register a new keyword-action mapping"""
    try:
        # Create action from registry
        action = action_registry.create_action(
            keyword_action.action_type, keyword_action.action_params
        )

        # Register with voice listener
        voice_listener.register_action(keyword_action.keyword, action)

        return KeywordActionResponse(
            keyword=keyword_action.keyword,
            action_type=keyword_action.action_type,
            action_params=keyword_action.action_params,
            is_active=True,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating keyword action: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/keywords", response_model=list[str])
async def list_keywords():
    """List all registered keywords"""
    return voice_listener.get_registered_keywords()


@app.delete("/keywords/{keyword}")
async def delete_keyword(keyword: str):
    """Delete a keyword-action mapping"""
    success = voice_listener.unregister_action(keyword)
    if not success:
        raise HTTPException(status_code=404, detail=f"Keyword '{keyword}' not found")
    return {"message": f"Keyword '{keyword}' deleted successfully"}


@app.post("/listen", response_model=ListenResponse)
async def listen(request: ListenRequest):
    """Listen for voice input once"""
    try:
        # Initialize microphone if needed
        if not voice_listener.microphone:
            voice_listener.initialize()

        # Listen for input
        text = voice_listener.listen_once(
            timeout=request.timeout, phrase_time_limit=request.phrase_time_limit
        )

        # Check for keyword triggers
        triggered, messages = voice_listener.check_keywords(text) if text else ([], [])

        return ListenResponse(
            recognized_text=text,
            triggered_keywords=triggered,
            action_messages=messages,
            success=True
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error during listening: {e}")
        raise HTTPException(status_code=500, detail="Error during voice recognition")


@app.post("/listen/test")
async def test_listen(text: str):
    """
    Test endpoint - simulate voice recognition without actual microphone
    Usage: POST /listen/test?text=엄마
    """
    logger.info(f"Test mode: simulating recognition of '{text}'")

    # Check for keyword triggers
    triggered, messages = voice_listener.check_keywords(text.lower()) if text else ([], [])

    return ListenResponse(
        recognized_text=text.lower(),
        triggered_keywords=triggered,
        action_messages=messages,
        success=True
    )


@app.post("/listen/start")
async def start_listening():
    """Start continuous listening (background task)"""
    if voice_listener.is_listening:
        raise HTTPException(status_code=400, detail="Already listening")

    # Note: In production, this should run in a background task
    # For now, just return a message
    return {
        "message": "Continuous listening would start here. Use /listen endpoint for single recognition."
    }


@app.post("/listen/stop")
async def stop_listening():
    """Stop continuous listening"""
    if not voice_listener.is_listening:
        raise HTTPException(status_code=400, detail="Not currently listening")

    voice_listener.stop_listening()
    return {"message": "Stopped listening"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
