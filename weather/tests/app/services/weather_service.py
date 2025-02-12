"""
Weather service module for handling OpenWeatherMap API integration.
"""
from typing import Dict, List, Optional
import httpx
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class WeatherData(BaseModel):
    """
    Pydantic model for weather data.
    """
    temperature: float
    feels_like: float
    humidity: int
    description: str
    icon: str

class ForecastData(BaseModel):
    """
    Pydantic model for forecast data.
    """
    date: str
    temperature: float
    description: str
    icon: str

class WeatherService:
    """
    Service class for interacting with OpenWeatherMap API.
    """
    
    def __init__(self):
        """Initialize the weather service with API configuration."""
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            logger.error("OpenWeatherMap API key not found in environment variables")
            raise ValueError("OpenWeatherMap API key not found in environment variables")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        logger.debug(f"WeatherService initialized with API key: {self.api_key[:5]}...")
        
    async def get_current_weather(self, city: str) -> Optional[WeatherData]:
        """
        Get current weather data for a city.
        
        Args:
            city (str): Name of the city
            
        Returns:
            Optional[WeatherData]: Weather data if found, None otherwise
        """
        logger.debug(f"Fetching current weather for city: {city}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "q": city,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                data = response.json()
                logger.debug(f"Received weather data: {data}")
                
                return WeatherData(
                    temperature=data["main"]["temp"],
                    feels_like=data["main"]["feels_like"],
                    humidity=data["main"]["humidity"],
                    description=data["weather"][0]["description"],
                    icon=data["weather"][0]["icon"]
                )
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {str(e)}")
                return None
            except KeyError as e:
                logger.error(f"Invalid data format received: {str(e)}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                return None
    
    async def get_forecast(self, city: str) -> List[ForecastData]:
        """
        Get 5-day forecast data for a city.
        
        Args:
            city (str): Name of the city
            
        Returns:
            List[ForecastData]: List of forecast data points
        """
        logger.debug(f"Fetching forecast for city: {city}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "q": city,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                data = response.json()
                logger.debug(f"Received forecast data with {len(data['list'])} entries")
                
                forecasts = []
                for item in data["list"][::8]:  # Get one forecast per day
                    forecast = ForecastData(
                        date=item["dt_txt"].split()[0],
                        temperature=item["main"]["temp"],
                        description=item["weather"][0]["description"],
                        icon=item["weather"][0]["icon"]
                    )
                    forecasts.append(forecast)
                
                return forecasts
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {str(e)}")
                return []
            except KeyError as e:
                logger.error(f"Invalid data format received: {str(e)}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}", exc_info=True)
                return []

    def get_weather_icon_url(self, icon_code: str) -> str:
        """
        Get the URL for a weather icon.
        
        Args:
            icon_code (str): The icon code from OpenWeatherMap
            
        Returns:
            str: The URL for the weather icon
        """
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png" 