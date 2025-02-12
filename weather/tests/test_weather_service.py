"""
Tests for the weather service module.
"""
import pytest
from app.services.weather_service import WeatherService, WeatherData, ForecastData
from unittest.mock import patch, AsyncMock
import os

@pytest.fixture
def weather_service():
    """Fixture for creating a WeatherService instance."""
    # Set a dummy API key for testing
    os.environ["OPENWEATHERMAP_API_KEY"] = "dummy_key"
    return WeatherService()

@pytest.mark.asyncio
async def test_get_current_weather_success(weather_service):
    """Test successful current weather retrieval."""
    mock_response = {
        "main": {
            "temp": 20.5,
            "feels_like": 21.0,
            "humidity": 65
        },
        "weather": [
            {
                "description": "clear sky",
                "icon": "01d"
            }
        ]
    }
    
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )
        
        result = await weather_service.get_current_weather("London")
        
        assert isinstance(result, WeatherData)
        assert result.temperature == 20.5
        assert result.feels_like == 21.0
        assert result.humidity == 65
        assert result.description == "clear sky"
        assert result.icon == "01d"

@pytest.mark.asyncio
async def test_get_current_weather_failure(weather_service):
    """Test failed current weather retrieval."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = Exception("API Error")
        
        result = await weather_service.get_current_weather("InvalidCity")
        assert result is None

@pytest.mark.asyncio
async def test_get_forecast_success(weather_service):
    """Test successful forecast retrieval."""
    mock_response = {
        "list": [
            {
                "dt_txt": "2024-02-10 12:00:00",
                "main": {"temp": 20.5},
                "weather": [{"description": "clear sky", "icon": "01d"}]
            },
            {
                "dt_txt": "2024-02-11 12:00:00",
                "main": {"temp": 22.0},
                "weather": [{"description": "few clouds", "icon": "02d"}]
            }
        ]
    }
    
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )
        
        result = await weather_service.get_forecast("London")
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], ForecastData)
        assert result[0].temperature == 20.5
        assert result[0].description == "clear sky"
        assert result[0].icon == "01d"

@pytest.mark.asyncio
async def test_get_forecast_failure(weather_service):
    """Test failed forecast retrieval."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = Exception("API Error")
        
        result = await weather_service.get_forecast("InvalidCity")
        assert isinstance(result, list)
        assert len(result) == 0

def test_get_weather_icon_url(weather_service):
    """Test weather icon URL generation."""
    icon_code = "01d"
    expected_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    
    result = weather_service.get_weather_icon_url(icon_code)
    assert result == expected_url 