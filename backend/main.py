# backend/main.py
from dotenv import load_dotenv
load_dotenv() # Loads environment variables from the .env file

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm 

import googlemaps

from geopy.geocoders import Nominatim

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

# These imports will now work correctly
from . import models, schemas
# ... rest of the imports
import os
import google.generativeai as genai
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class StoryPoints(BaseModel):
    place_name: str
    points: List[str]
# These imports will now work correctly
from . import models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="గడులు & గృహాలు API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Signup endpoint"""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint"""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": user.username, "message": "Login successful"}

@app.post("/places/", response_model=schemas.Place)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    # User creation logic remains the same
    db_user = db.query(models.User).filter(models.User.username == place.contributor_username).first()
    if not db_user:
        db_user = models.User(username=place.contributor_username, contributions=0)
        db.add(db_user)

    db_user.contributions += 1

    place_dict = place.dict(exclude={"contributor_username"})

    # The entire geocoding block has been removed from here

    # Convert empty strings to None before saving
    for key, value in place_dict.items():
        if value == "":
            place_dict[key] = None

    db_place = models.Place(**place_dict, contributor=db_user)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@app.get("/places/", response_model=List[schemas.Place])
def read_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    places = db.query(models.Place).offset(skip).limit(limit).all()
    return places

@app.post("/ai/generate-story")
async def get_ai_story(story_points: StoryPoints):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if not story_points.points:
        raise HTTPException(status_code=400, detail="No points provided for story generation.")
        
    prompt = f"""
    You are a historical storyteller for a cultural heritage project called "గడులు & గృహాలు".
    Your task is to weave the following key points about a place named "{story_points.place_name}" into a short, engaging, and respectful narrative story of about 2-3 paragraphs.

    Key Points:
    - {'\n- '.join(story_points.points)}

    Generated Story:
    """
    try:
        response = model.generate_content(prompt)
        return {"story": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI story generation failed: {str(e)}")