from typing import Optional
from sqlalchemy.orm import Session

from .models import PetModel, EventModel
from ..domain.events import PetEvent


class PetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_name(self, name: str) -> Optional[PetModel]:
        return self.db.query(PetModel).filter_by(name=name).first()
    
    def save_pet_state(self, pet_domain) -> PetModel:
        pet = self.get_by_name(pet_domain.name)
        if pet is None:
            pet = PetModel(name=pet_domain.name)
            self.db.add(pet)

        pet.hunger = pet_domain.hunger
        pet.energy = pet_domain.energy
        pet.health = pet_domain.health
        pet.happiness = pet_domain.happiness
        pet.state = pet_domain.state

        self.db.commit()
        self.db.refresh(pet)
        return pet
    

class EventRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_event(self, pet: PetModel, event: PetEvent) -> EventModel:
        ev = EventModel(
            pet = pet,
            type = event.type,
            message = event.message,
        )
        self.db.add(ev)
        self.db.commit()
        self.db.refresh(ev)
        return ev

