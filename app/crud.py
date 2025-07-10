

from typing import Optional, List
from sqlalchemy.orm import Session
from app import models

def create_message(db: Session, text: str) -> models.Message:
    """Create and save a new message with given text."""
    db_message = models.Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, new_text: str) -> Optional[models.Message]:
    """Update message text by ID. Returns updated message or None if not found."""
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        message.text = new_text
        db.commit()
        db.refresh(message)
        return message
    return None

def delete_message(db: Session, message_id: int) -> bool:
    """Delete message by ID. Returns True if deleted, else False."""
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False

def search_messages(db: Session, keyword: str, limit: int = 50) -> List[models.Message]:
    """Search messages by keyword in text, case-insensitive, limited to 50 results."""
    return db.query(models.Message).filter(models.Message.text.ilike(f"%{keyword}%")).limit(limit).all()

def get_messages(db: Session) -> List[models.Message]:
    """Return all messages from DB."""
    return db.query(models.Message).all()
