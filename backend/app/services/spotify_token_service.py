"""
Spotify token persistence service.

This module owns the responsibility of saving and retrieving Spotify
tokens from the database.

Routes should not directly decide how token records are created or
updated. Instead, they should call the methods in this service, which
encapsulates the logic for token management and ensures that the database
operations are handled consistently across the application.
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.spotify_token import SpotifyToken
from app.services.token_crypto_service import encrypt_token
from app.services.token_crypto_service import decrypt_token

def upsert_spotify_token(
    db: Session,
    spotify_user_id: str,
    access_token: str,
    refresh_token: str,
    expires_in: int,
) -> SpotifyToken:
    """
    Create or update a Spotify token record for a given user.

    Upsert behavior matters because a returning user should refresh
    their stored credentials rather than creating a new record each 
    time they log in.
    """

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    token_row = (
        db.query(SpotifyToken)
        .filter(SpotifyToken.spotify_user_id == spotify_user_id)
        .first()
    )

    if token_row is None:
        token_row = SpotifyToken(
            spotify_user_id=spotify_user_id,
            encrypted_access_token=encrypt_token(access_token),
            encrypted_refresh_token=encrypt_token(refresh_token),
            expires_at=expires_at,
        )
        db.add(token_row)

    else:
        token_row.encrypted_access_token = encrypt_token(access_token)
        token_row.encrypted_refresh_token = encrypt_token(refresh_token)
        token_row.expires_at = expires_at

    db.commit()
    db.refresh(token_row)

    return token_row

def get_decrypted_access_token(db: Session, spotify_user_id: str) -> str:
    """
    Retrieve and decrypt the access token for a given Spotify user ID.

    This method abstracts away the details of how tokens are stored and
    encrypted, allowing other parts of the application to simply request
    the decrypted token when needed.
    """

    token_row = (
        db.query(SpotifyToken)
        .filter(SpotifyToken.spotify_user_id == spotify_user_id)
        .first()
    )

    if token_row is None:
        raise ValueError(f"No Spotify token found for user ID: {spotify_user_id}")

    return decrypt_token(token_row.encrypted_access_token)

def get_token_row(db: Session, spotify_user_id: str) -> SpotifyToken:
    """
    Retrieve the full token record for a given Spotify user ID.

    This can be useful for operations that need access to the refresh token
    or expiration time, in addition to the access token.
    """

    token_row = (
        db.query(SpotifyToken)
        .filter(SpotifyToken.spotify_user_id == spotify_user_id)
        .first()
    )

    if token_row is None:
        raise ValueError(f"No Spotify token found for user ID: {spotify_user_id}")

    return token_row

def get_decrypted_refresh_token(db: Session, spotify_user_id: str) -> str:
    """
    Retrieve and decrypt the refresh token for a given Spotify user ID.

    Similar to get_decrypted_access_token, but specifically for the refresh token.
    """

    token_row = get_token_row(db, spotify_user_id)

    return decrypt_token(token_row.encrypted_refresh_token)

def update_access_token(
    db: Session,
    spotify_user_id: str,
    new_access_token: str,
    expires_in: int,
) -> SpotifyToken:
    """
    Update the access token and expiration time for a given Spotify user ID.

    This is typically used after refreshing the access token using the refresh token.
    """

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    token_row = get_token_row(db, spotify_user_id)

    token_row.encrypted_access_token = encrypt_token(new_access_token)
    token_row.expires_at = expires_at

    db.commit()
    db.refresh(token_row)

    return token_row