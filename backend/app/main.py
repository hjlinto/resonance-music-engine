"""
Application entry point for the Resonance backend API.

This file owns the responsibility of creating the FastAPI app instance, 
registering global settings, and exposing health-check routes used 
during local development and deployment.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Resonance API",
    description="Backend API for the Resonance music recommendation system.",
    version="0.1.0")

@app.get("/health")
def health_check():
    """
    Confirm that the backend API is running.
    """
    return {"status": "ok"}