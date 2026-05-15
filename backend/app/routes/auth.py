"""
Authentication routes for the application.

This module defines the routes related to user authentication, including login, logout, and registration. 
It uses FastAPI for handling HTTP requests and responses, and integrates with the authentication 
service to manage user sessions and credentials.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from requests import HTTPError

from app.services.spotify_auth_service import build_spotify_login_url
from app.services.spotify_auth_service import exchange_code_for_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/spotify/login")
def spotify_login() -> RedirectResponse:
    """
    Redirects the user to the Spotify login page.

    The route only handles HTTP behavior. The URL-building logic lives in the Spotify 
    auth service so it can be tested and reused in other contexts.
    """
    
    login_url = build_spotify_login_url()

    return RedirectResponse(url=login_url)

@router.get("/spotify/callback")
def spotify_callback(
    code: str | None = Query(default=None),
    error: str | None = Query(default=None),
) -> dict:
    """
    Handle Spotify's OAuth callback.
    
    Spotify redirects to this endpoint with either an authorization code
    or an error message. If a code is provided, we exchange it for an access 
    token. If an error is provided, we raise an HTTPException with the error details.
    """

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify authentication failed: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="Spotify authentication failed: No code provided")
    
    try:
        token_response = exchange_code_for_token(code)

    except HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to exchange Spotify authorization code for access token.",
        ) from exc
    
    return {
        "message": "Spotify authentication successful.",
        "access_token_received": "access_token" in token_response,
        "refresh_token_received": "refresh_token" in token_response,
        "expires_in": token_response.get("expires_in"),
    }