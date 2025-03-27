# app/schemas/joke.py
from pydantic import BaseModel, Field
from typing import Optional

class JokeBase(BaseModel):
    """
    Base Pydantic model for joke data validation
    """
    category: str = Field(default="Unknown")
    joke_type: str
    is_nsfw: bool = False
    is_political: bool = False
    is_sexist: bool = False
    is_safe: bool = True
    language: str = "en"

class JokeSingleCreate(JokeBase):
    """
    Schema for creating a single-type joke
    """
    joke_text: Optional[str] = None

class JokeTwoPartCreate(JokeBase):
    """
    Schema for creating a two-part joke
    """
    setup: Optional[str] = None
    delivery: Optional[str] = None

class JokeResponse(JokeBase):
    """
    Response schema for jokes
    """
    id: int
    
    class Config:
        orm_mode = True

class JokeAPIResponse(BaseModel):
    """
    Response schema for joke fetching endpoint
    """
    status: str
    message: str
    jokes_fetched: int