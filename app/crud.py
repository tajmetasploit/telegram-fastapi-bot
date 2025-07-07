

from sqlalchemy.orm import Session
from app import models

def create_message(db: Session, text: str) -> models.Message:
    db_message = models.Message(text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

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


def get_messages(db: Session):
    return db.query(models.Message).all()



