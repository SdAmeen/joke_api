# app/routes/jokes.py
import httpx
import logging
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.joke import Joke
from ..schemas.joke import JokeResponse, JokeAPIResponse

router = APIRouter()
logger = logging.getLogger(__name__)

async def fetch_jokes(num_jokes: int = 100):
    """
    Fetch jokes from JokeAPI asynchronously
    
    :param num_jokes: Number of jokes to fetch
    :return: List of processed jokes
    """
    async with httpx.AsyncClient() as client:
        jokes = []
        
        # JokeAPI supports max 10 jokes per request
        for _ in range(num_jokes // 10 + 1):
            try:
                response = await client.get(
                    "https://v2.jokeapi.dev/joke/Any",
                    params={
                        "type": "single,twopart",
                        "amount": 10,
                        "blacklistFlags": "",  # No blacklisting
                        "lang": "en"
                    }
                )
                response.raise_for_status()
                joke_data = response.json()
                
                # Handle both single joke and multiple jokes responses
                jokes_batch = joke_data.get('jokes', [joke_data] if 'type' in joke_data else [])
                jokes.extend(jokes_batch)
                
                # Break if we have enough jokes
                if len(jokes) >= num_jokes:
                    break
            
            except httpx.RequestError as e:
                logger.error(f"Request error occurred: {e}")
                break
        
        return jokes[:num_jokes]

def process_and_store_jokes(jokes, db: Session):
    """
    Process and store jokes in the database
    
    :param jokes: List of jokes from JokeAPI
    :param db: Database session
    """
    try:
        for joke_data in jokes:
            # Handle different joke types
            if joke_data['type'] == 'single':
                joke_entry = Joke(
                    category=joke_data.get('category', 'Unknown'),
                    joke_type=joke_data['type'],
                    joke_text=joke_data.get('joke', ''),
                    is_nsfw=joke_data['flags'].get('nsfw', False),
                    is_political=joke_data['flags'].get('political', False),
                    is_sexist=joke_data['flags'].get('sexist', False),
                    is_safe=joke_data.get('safe', True),
                    language=joke_data.get('lang', 'en')
                )
            else:  # two-part joke
                joke_entry = Joke(
                    category=joke_data.get('category', 'Unknown'),
                    joke_type=joke_data['type'],
                    setup=joke_data.get('setup', ''),
                    delivery=joke_data.get('delivery', ''),
                    is_nsfw=joke_data['flags'].get('nsfw', False),
                    is_political=joke_data['flags'].get('political', False),
                    is_sexist=joke_data['flags'].get('sexist', False),
                    is_safe=joke_data.get('safe', True),
                    language=joke_data.get('lang', 'en')
                )
            
            db.add(joke_entry)
        
        db.commit()
        logger.info(f"Successfully stored {len(jokes)} jokes")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error storing jokes: {e}")

@router.post("/fetch-jokes", response_model=JokeAPIResponse)
async def fetch_and_store_jokes(
    background_tasks: BackgroundTasks, 
    num_jokes: int = 100,
    db: Session = Depends(get_db)
):
    """
    Endpoint to fetch and store jokes asynchronously
    
    :param background_tasks: Background task handler
    :param num_jokes: Number of jokes to fetch
    :param db: Database session
    :return: Confirmation message
    """
    try:
        jokes = await fetch_jokes(num_jokes)
        
        # Use background task for storing jokes
        background_tasks.add_task(process_and_store_jokes, jokes, db)
        
        return {
            "status": "Processing",
            "message": f"Fetching and storing {num_jokes} jokes",
            "jokes_fetched": len(jokes)
        }
    
    except Exception as e:
        logger.error(f"Error in fetch_and_store_jokes: {e}")
        return {
            "status": "Error",
            "message": str(e),
            "jokes_fetched": 0
        }

@router.get("/jokes", response_model=List[JokeResponse])
async def get_jokes(
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """
    Retrieve stored jokes from database
    
    :param skip: Number of jokes to skip
    :param limit: Maximum number of jokes to return
    :param db: Database session
    :return: List of jokes
    """
    jokes = db.query(Joke).offset(skip).limit(limit).all()
    return jokes