"""
Spotify OAuth service logic.

This module owns Spotify authentication behavior that should not live directly
inside route handlers.

Routes are responsbile for HTTP request/response behavior.
Services are responsbile for business logic and external API communication.
"""
import base64
from urllib.parse import urlencode

import requests
from app.config import settings

def build_spotify_login_url() -> str:
    """
    Build the Spotify login URL for user authentication.
    
    This function constructs the Spotify authorization URL used during the OAuth login flow.
    """

    if not settings.SPOTIFY_CLIENT_ID:
        raise ValueError("Spotify client ID is not configured.")
    if not settings.SPOTIFY_REDIRECT_URI:
        raise ValueError("Spotify redirect URI is not configured.")
    
    client_id = settings.SPOTIFY_CLIENT_ID
    redirect_uri = settings.SPOTIFY_REDIRECT_URI
    
    """
    Query parameters define the OAuth request Spotify expects before redirecting
    the user to the authorization screen.
    """
    query_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": settings.SPOTIFY_SCOPES,
        "show_dialog": "true",
    }

    return f"{settings.SPOTIFY_AUTH_URL}?{urlencode(query_params)}"

def exchange_code_for_token(code: str) -> dict:
    """
    Exchange a Spotify authorization code for an access token.
    
    Spotify sends our callback route a temporary authorization code. The backend
    must trade that code for tokens before it can call Spotify's API on the user's behalf.
    """

    if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
        raise ValueError("Spotify client credentials are not configured.")
    
    credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
    }

    response = requests.post(
        settings.SPOTIFY_TOKEN_URL,
        headers=headers,
        data=payload,
        timeout=10,
    )

    response.raise_for_status() # Raise an error for bad responses

    return response.json()

def refresh_access_token(refresh_token: str) -> dict:
    """
    Request a new Spotify access token using a stored refresh token.

    This keeps the user authenticated without needing to log in again after the access 
    token expires, without needing to go through the full OAuth flow again.
    """

    if not settings.SPOTIFY_CLIENT_ID or not settings.SPOTIFY_CLIENT_SECRET:
        raise ValueError("Spotify client credentials are not configured.")
    
    credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(
        settings.SPOTIFY_TOKEN_URL,
        headers=headers,
        data=payload,
        timeout=10,
    )

    response.raise_for_status() # Raise an error for bad responses

    return response.json()