from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.api.routes import router as api_router

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Flexioke API",
    description="AI-Powered Audio Stem Separation & Multitrack Karaoke Web Player",
    version="0.2.6",
)

# Enable CORS for local and cross-origin usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router)

# Mount Static Assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
def serve_index():
    """Serve single-page application entrypoint."""
    index_file = STATIC_DIR / "index.html"
    return FileResponse(str(index_file))

@app.get("/favicon.ico", include_in_schema=False)
def serve_favicon():
    """Serve favicon icon."""
    favicon_file = STATIC_DIR / "favicon.ico"
    return FileResponse(str(favicon_file), media_type="image/x-icon")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
