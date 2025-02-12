"""
Weather API routes module.
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..services.weather_service import WeatherService
from ..core.errors import WeatherAPIError, APIKeyError
import plotly.graph_objects as go
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()
weather_service = WeatherService()

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

@router.get("/search")
async def search_weather(request: Request, location: str):
    """
    Search for weather data by location and return HTML partial.
    
    Args:
        request (Request): The incoming request object
        location (str): The location to search for
        
    Returns:
        TemplateResponse: Rendered weather data partial
    """
    try:
        logger.debug(f"Received weather search request for location: {location}")
        logger.debug(f"Using API key: {weather_service.api_key[:5]}...")  # Only log first 5 chars for security
        
        if not weather_service.api_key or weather_service.api_key == "your_api_key_here":
            logger.error("API key not configured properly")
            raise APIKeyError()
            
        # Get current weather and forecast data
        logger.debug("Fetching current weather data...")
        current_weather = await weather_service.get_current_weather(location)
        if not current_weather:
            logger.error(f"Location not found: {location}")
            raise HTTPException(
                status_code=404,
                detail=f"Location not found: {location}"
            )
            
        logger.debug("Fetching forecast data...")
        forecast = await weather_service.get_forecast(location)
        
        # Create temperature trend chart
        logger.debug("Creating temperature trend chart...")
        dates = [f.date for f in forecast]
        temps = [f.temperature for f in forecast]
        
        fig = go.Figure(data=go.Scatter(x=dates, y=temps, mode='lines+markers'))
        fig.update_layout(
            title="5-Day Temperature Trend",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=300
        )
        chart_html = fig.to_html(full_html=False)
        
        # Render the weather data partial
        logger.debug("Rendering weather data template...")
        return templates.TemplateResponse(
            "partials/weather_data.html",
            {
                "request": request,
                "current": current_weather,
                "forecast": forecast,
                "chart_html": chart_html,
                "location": location
            }
        )
        
    except APIKeyError:
        logger.error("OpenWeatherMap API key configuration error")
        raise HTTPException(
            status_code=500,
            detail="OpenWeatherMap API key is not configured. Please update your .env file with a valid API key."
        )
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching weather data: {str(e)}"
        ) 