"""
Artist database model.

This model owns the normalized artist records imported from Spotify.

Artists are stored once and reused across tracks, top-artist rankings, and
future recommendation features.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Artist(Base):
    """
    Represents a Spotify artist in our database.
    """

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    spotify_artist_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    genres: Mapped[str | None] = mapped_column(String, nullable=True)
    popularity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)