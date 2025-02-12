"""
Error handling module for the Weather Dashboard application.

This module defines custom exceptions and error handlers for the application.
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional

class WeatherAPIError(HTTPException):
    """
    Custom exception for Weather API related errors.
    
    Attributes:
        status_code (int): HTTP status code
        detail (str): Error detail message
        headers (Optional[Dict[str, Any]]): Optional response headers
    """
    
    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Weather API error occurred",
        headers: Optional[Dict[str, Any]] = None
    ):
        """Initialize the WeatherAPIError."""
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class LocationNotFoundError(WeatherAPIError):
    """Exception raised when a location is not found."""
    
    def __init__(self, location: str):
        """Initialize the LocationNotFoundError."""
        super().__init__(
            status_code=404,
            detail=f"Location not found: {location}"
        )

class APIKeyError(WeatherAPIError):
    """Exception raised when there are API key related issues."""
    
    def __init__(self):
        """Initialize the APIKeyError."""
        super().__init__(
            status_code=500,
            detail="API key configuration error"
        )

async def weather_api_exception_handler(
    request: Request,
    exc: WeatherAPIError
) -> JSONResponse:
    """
    Handle WeatherAPIError exceptions.
    
    Args:
        request (Request): The request that caused the exception
        exc (WeatherAPIError): The exception instance
        
    Returns:
        JSONResponse: JSON formatted error response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": exc.__class__.__name__
            }
        }
    )

async def location_not_found_handler(
    request: Request,
    exc: LocationNotFoundError
) -> JSONResponse:
    """
    Handle LocationNotFoundError exceptions.
    
    Args:
        request (Request): The request that caused the exception
        exc (LocationNotFoundError): The exception instance
        
    Returns:
        JSONResponse: JSON formatted error response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "LocationNotFound"
            }
        }
    ) 