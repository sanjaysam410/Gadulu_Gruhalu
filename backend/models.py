# backend/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime  # <--- ADD THIS LINE

# Import Base from the database.py file
from .database import Base

# In backend/models.py, inside the User class
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # <-- ADD THIS LINE
    badge = Column(String, default="New Contributor ✨")
    contributions = Column(Integer, default=0)
    
    places = relationship("Place", back_populates="contributor")
class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    region = Column(String)
    area = Column(String, nullable=True)
    era = Column(String)
    story = Column(Text)
    tags = Column(String)
    image_url = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) # This line now works
    
    contributor_id = Column(Integer, ForeignKey("users.id"))
    contributor = relationship("User", back_populates="places")
