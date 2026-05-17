"""
Spotify data routes.

These routes expose Spotify listening data through our backend.

The routes coordinate HTTP behaviior, database access, and service calls
while keeping Spotify API request details inside the service layer.
"""

from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.services.spotify_api_service import get_user_top_artists, get_user_top_tracks
from app.services.spotify_token_service import get_decrypted_access_token, update_access_token, get_decrypted_refresh_token
from app.services.spotify_auth_service import refresh_access_token

router = APIRouter(prefix="/spotify", tags=["spotify"])

def call_spotify_with_refresh(
        db,
        spotify_user_id: str,
        spotify_call,
) -> dict:
    """
    Call Spotify with the stored access token, refreshing it if the call fails due to an expired token.

    Route handles use this helper so each endpoint does not duplicate token refresh and retry logic.
    """

    access_token = get_decrypted_access_token(db, spotify_user_id)

    try:
        return spotify_call(access_token)
    
    except HTTPException as exc:
        if exc.status_code != 401:
            raise

        refresh_token = get_decrypted_refresh_token(db, spotify_user_id)
        refreshed_token_response = refresh_access_token(refresh_token)

        new_access_token = refreshed_token_response["access_token"]
        expires_in = refreshed_token_response["expires_in"]

        update_access_token(
            db=db,
            spotify_user_id=spotify_user_id,
            new_access_token=new_access_token,
            expires_in=expires_in,
        )

        return spotify_call(new_access_token)


@router.get("/{spotify_user}/top-tracks")
def get_top_tracks(spotify_user: str) -> dict:
    """
    Fetch the user's top tracks from Spotify from an authorized Spotify user.
    """

    spotify_user_id = spotify_user
    db = SessionLocal()

    try:
        return call_spotify_with_refresh(
            db=db,
            spotify_user_id=spotify_user_id,
            spotify_call=get_user_top_tracks,
        )
    
    # Exc is raised when the user doesn't exist or doesn't have a Spotify token
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    finally:
        db.close()

@router.get("/{spotify_user}/top-artists")
def get_top_artists(spotify_user: str) -> dict:
    """
    Fetch the user's top artists from Spotify from an authorized Spotify user.
    """

    spotify_user_id = spotify_user
    db = SessionLocal()

    try:
        return call_spotify_with_refresh(
            db=db,
            spotify_user_id=spotify_user_id,
            spotify_call=get_user_top_artists,
        )
    
    # Exc is raised when the user doesn't exist or doesn't have a Spotify token
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    finally:
        db.close()