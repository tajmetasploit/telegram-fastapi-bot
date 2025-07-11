"""from sqlalchemy import Column, Integer, String
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), index=True)  # Limit max length to 1000 characters
"""

from sqlalchemy import Column, Integer, String
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)



