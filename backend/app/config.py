"""
Application configuration
This module owns environment-based settings for the backend.
Keeping this in a separate file allows us to easily manage and override settings for different environments (development, testing, production).
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Centralized application settings.

    Best practice
    """