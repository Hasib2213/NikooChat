from fastapi import Request
from sqlalchemy.orm import Session
from database import SessionLocal
import uuid

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session_id(request: Request) -> str:
    """Get or create session ID from cookies"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id