# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str # Add the password field for signup

class User(UserBase):
    id: int
    badge: str
    contributions: int

    class Config:
        from_attributes = True

class PlaceBase(BaseModel):
    name: str
    type: str
    region: str
    area: Optional[str] = None
    era: str
    story: str
    tags: Optional[str] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PlaceCreate(PlaceBase):
    contributor_username: str

class Place(PlaceBase):
    id: int
    created_at: datetime
    contributor: User

    class Config:
        from_attributes = True