# app/models/joke.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from ..database import Base

class Joke(Base):
    """
    SQLAlchemy model for storing jokes
    """
    __tablename__ = "jokes"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    joke_type = Column(String)
    joke_text = Column(Text)
    setup = Column(Text)
    delivery = Column(Text)
    is_nsfw = Column(Boolean, default=False)
    is_political = Column(Boolean, default=False)
    is_sexist = Column(Boolean, default=False)
    is_safe = Column(Boolean, default=True)
    language = Column(String)