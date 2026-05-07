"""
Temporary database test routes.

These routes exist only to verify database connectivity during early development.
"""

from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import SessionLocal

router = APIRouter()

@router.get("/test-db")
def test_database_connection() -> dict[str, str]:
    """
    Verify that the backend can successfully connect to PostgreSQL.
    """
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {"database": "connected"}
    
    finally:
        db.close()
    