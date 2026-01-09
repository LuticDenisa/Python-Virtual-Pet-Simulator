from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class PetModel(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique = True, nullable=False)
    hunger = Column(Integer, default=3)
    energy = Column(Integer, default=7)
    health = Column(Integer, default=8)
    happiness = Column(Integer, default=7)
    state = Column(String, default="happy")

    events = relationship("EventModel", back_populates="pet")


class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("PetModel", back_populates="events")
    