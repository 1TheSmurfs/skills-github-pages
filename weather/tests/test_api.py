"""
Tests for the Weather Dashboard API routes.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.weather_service import WeatherService
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.fixture
def mock_weather_service():
    """Fixture for mocking WeatherService."""
    with patch("app.api.weather.weather_service") as mock_service:
        yield mock_service

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_home_page():
    """Test the home page endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Weather Dashboard" in response.text
    assert "Real-time weather information" in response.text

def test_search_weather_success(mock_weather_service):
    """Test successful weather search."""
    # Mock weather service responses
    mock_weather_service.get_current_weather.return_value = AsyncMock(return_value={
        "temperature": 20.5,
        "feels_like": 21.0,
        "humidity": 65,
        "description": "clear sky",
        "icon": "01d"
    })
    
    mock_weather_service.get_forecast.return_value = AsyncMock(return_value=[
        {
            "date": "2024-02-10",
            "temperature": 20.5,
            "description": "clear sky",
            "icon": "01d"
        }
    ])
    
    response = client.get("/api/weather/search?location=London")
    assert response.status_code == 200
    assert "Current Weather in London" in response.text
    assert "Temperature Trend" in response.text

def test_search_weather_not_found(mock_weather_service):
    """Test weather search with invalid location."""
    mock_weather_service.get_current_weather.return_value = AsyncMock(return_value=None)
    
    response = client.get("/api/weather/search?location=InvalidCity")
    assert response.status_code == 404
    assert "Location not found" in response.json()["detail"]

def test_search_weather_error(mock_weather_service):
    """Test weather search with API error."""
    mock_weather_service.get_current_weather.side_effect = Exception("API Error")
    
    response = client.get("/api/weather/search?location=London")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"] 