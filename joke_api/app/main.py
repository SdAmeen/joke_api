# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routes import jokes

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Jokes Fetcher API")

# Include router
app.include_router(jokes.router, prefix="/api/v1/jokes", tags=["jokes"])

# Optional: Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Jokes Fetcher API"}