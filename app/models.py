from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    # … any other raw fields …

class ScoreRule(Base):
    __tablename__ = "score_rules"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    weight = Column(Float)
    # … rule definition columns …

    # e.g. rule might say: if engine_size > X, add Y points, etc.
