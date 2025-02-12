"""
Weather Dashboard Application Package.

A modern weather dashboard built with FastAPI and HTMX, featuring real-time
weather updates and interactive visualizations.
"""

__version__ = "1.0.0"
__author__ = "Weather Dashboard Team"
__email__ = "contact@weatherdashboard.com"

from .main import app
from .services.weather_service import WeatherService
from .core.config import settings

__all__ = ["app", "WeatherService", "settings"] 