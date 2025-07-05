# app/crud.py
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
