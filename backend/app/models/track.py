"""
Track database model.

This model owns normalized Spotify track records.

Tracks are stored independently from user rankings, so the
same track can be reused across different users and 
recommendation flows.
"""

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Track(Base):
    """
    Represents a Spotify track in the database.
    """

    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    spotify_track_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    album_name: Mapped[str | None] = mapped_column(String, nullable=True)

    artist_name: Mapped[str | None] = mapped_column(String, nullable=True)
    album_image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    preview_url: Mapped[str | None] = mapped_column(String, nullable=True)
    popularity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    danceability: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy: Mapped[float | None] = mapped_column(Float, nullable=True)
    valence: Mapped[float | None] = mapped_column(Float, nullable=True)
    tempo: Mapped[float | None] = mapped_column(Float, nullable=True)
    acousticness: Mapped[float | None] = mapped_column(Float, nullable=True)
    instrumentalness: Mapped[float | None] = mapped_column(Float, nullable=True)