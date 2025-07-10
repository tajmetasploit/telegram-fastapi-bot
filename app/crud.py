

"""from typing import Optional, List
from sqlalchemy.orm import Session
from app import models

def create_message(db: Session, text: str) -> models.Message:
    #Create and save a new message with the given text.
    db_message = models.Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, new_text: str) -> Optional[models.Message]:
    
    #Update the text of a message by its ID.
    #Returns the updated message if found, else None.
    
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        message.text = new_text
        db.commit()
        db.refresh(message)
        return message
    return None

def delete_message(db: Session, message_id: int) -> bool:
    
    #Delete a message by its ID.
    #Returns True if the message was deleted, False if not found.
    
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False

def search_messages(db: Session, keyword: str, limit: int = 50) -> List[models.Message]:
    
    #Search for messages containing the keyword (case-insensitive).
    #Returns a list limited to 'limit' results.
    
    return db.query(models.Message).filter(models.Message.text.ilike(f"%{keyword}%")).limit(limit).all()

def get_messages(db: Session) -> List[models.Message]:
    #Return all messages stored in the database.
    return db.query(models.Message).all()
"""

# app/crud.py

from sqlalchemy.orm import Session
from app import models

# Create a new message
def create_message(db: Session, text: str) -> models.Message:
    db_message = models.Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# Update message by ID
def update_message(db: Session, message_id: int, new_text: str):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        message.text = new_text
        db.commit()
        db.refresh(message)
        return message
    return None

# Delete message by ID
def delete_message(db: Session, message_id: int):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False



# Search messages by keyword (case-insensitive)
def search_messages(db: Session, keyword: str):
    return db.query(models.Message).filter(models.Message.text.ilike(f"%{keyword}%")).all()

"""def get_message_by_id(db: Session, msg_id: int):
    return db.query(models.Message).filter(models.Message.id == msg_id).first()
"""

# Get all messages
def get_messages(db: Session):
    return db.query(models.Message).all()




