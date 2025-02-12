"""
Configuration management module for the Weather Dashboard application.

This module handles all configuration settings using Pydantic's BaseSettings,
which allows for easy environment variable loading and validation.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    
    Attributes:
        app_name (str): Name of the application
        version (str): Application version
        debug (bool): Debug mode flag
        openweathermap_api_key (str): OpenWeatherMap API key
        api_base_url (str): Base URL for OpenWeatherMap API
        temperature_unit (str): Temperature unit (metric/imperial)
    """
    
    app_name: str = "Weather Dashboard"
    version: str = "1.0.0"
    debug: bool = False
    openweathermap_api_key: str
    api_base_url: str = "https://api.openweathermap.org/data/2.5"
    temperature_unit: str = "metric"
    
    # Path configurations
    base_dir: Path = Path(__file__).resolve().parent.parent
    templates_dir: Path = base_dir / "templates"
    static_dir: Path = base_dir.parent / "static"
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache application settings.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()

settings = get_settings() 