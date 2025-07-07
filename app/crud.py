"""# app/crud.py
from sqlalchemy.orm import Session
from app import models

def create_message(db: Session, text: str) -> models.Message:
    db_message = models.Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session):
    return db.query(models.Message).all()



def update_message(db: Session, message_id: int, new_text: str):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        message.text = new_text
        db.commit()
        db.refresh(message)
        return message
    return None

def delete_message(db: Session, message_id: int):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False

def search_messages(db: Session, keyword: str):
    return db.query(models.Message).filter(models.Message.text.ilike(f"%{keyword}%")).all()

def update_message(db: Session, message_id: int, new_text: str):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        msg.text = new_text
        db.commit()
        return True
    return False

def delete_message(db: Session, message_id: int):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if msg:
        db.delete(msg)
        db.commit()
        return True
    return False

def search_messages(db: Session, query: str):
    return db.query(models.Message).filter(models.Message.text.contains(query)).all()

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



