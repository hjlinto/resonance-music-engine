"""
Application entry point for the Resonance backend API.

This file owns the responsibility of creating the FastAPI app instance, 
registering global settings, and exposing health-check routes used 
during local development and deployment.
"""

from fastapi import FastAPI

from app.routes.test_db import router as test_db_router
from app.routes.test_config import router as test_config_router
from app.routes.auth import router as auth_router
from app.routes.spotify_data import router as spotify_data_router

from app.db.database import Base, engine

from app import models

# Initialize the FastAPI application with metadata for documentation
app = FastAPI(
    title="Resonance API",
    description="Backend API for the Resonance music recommendation system.",
    version="0.1.0")

# Create database tables based on the defined models
Base.metadata.create_all(bind=engine) 

# Register API routes
app.include_router(test_config_router)
app.include_router(test_db_router)
app.include_router(auth_router)
app.include_router(spotify_data_router)

# Health check endpoint for local development and deployment monitoring
@app.get("/health")
def health_check():
    """
    Confirm that the backend API is running.
    """
    return {"status": "ok"}
