"""
Weather Dashboard main application module.

This module initializes the FastAPI application and sets up the main routes
and configuration for the Weather Dashboard.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .api import weather

# Initialize FastAPI app
app = FastAPI(
    title="Weather Dashboard",
    description="A modern weather dashboard with real-time updates and visualizations",
    version="1.0.0"
)

# Setup static files and templates
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR.parent / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include API routes
app.include_router(weather.router, prefix="/api/weather", tags=["weather"])

@app.get("/")
async def home(request: Request):
    """
    Render the home page of the weather dashboard.
    
    Args:
        request (Request): The incoming request object
        
    Returns:
        TemplateResponse: The rendered home page template
    """
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Weather Dashboard"}
    )

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.
    
    Returns:
        dict: A simple status message
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 