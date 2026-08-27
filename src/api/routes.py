from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
def health_check():
    """Health check endpoint verifying API availability."""
    return {
        "status": "ok",
        "app": "flexioke",
        "version": "0.1.0",
    }
