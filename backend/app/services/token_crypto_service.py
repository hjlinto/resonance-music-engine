"""
Token encryption service.

This module owns the responsibility of encrypting and decrypting
Spotify access tokens before they are stored or used by the application.

Keeping the encryption logic in a separate service allows for better 
separation of concerns and makes it easier to manage the encryption keys 
and algorithms used.
"""

from cryptography.fernet import Fernet

from app.config import settings

if not settings.TOKEN_ENCRYPTION_KEY:
    raise ValueError("TOKEN_ENCRYPTION_KEY is not configured.")

fernet = Fernet(settings.TOKEN_ENCRYPTION_KEY.encode())

def encrypt_token(token: str) -> str:
    """
    Encrypts a Spotify access token.

    Tokens should never be stored in plain text because they grant access to a
    user's Spotify account. Encrypting tokens before storage helps protect them.
    """
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypts an encrypted Spotify access token.

    This is used when the application needs to use the token to make API calls
    on behalf of the user. The token is decrypted in memory and not stored in
    plain text anywhere.
    """
    return fernet.decrypt(encrypted_token.encode()).decode()