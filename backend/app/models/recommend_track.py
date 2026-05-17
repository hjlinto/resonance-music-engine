"""
Recommend track database model.

This model stores generated track recommendations for users.

Recommendations are persisted so the frontend can load them without regenerating recommendations on every request.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class RecommendedTrack(Base):
    """Represents a generated recommendation for a user."""

    __tablename__ = "recommended_tracks"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    track_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tracks.id"),
        nullable=False
    )

    recommendation_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    recommendation_reason: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
