from typing import Callable

from sqlalchemy.orm import Session

from ..domain.events import PetEvent, PetObserver
from .repositories import EventRepository, PetRepository


class DbEventLoggerObserver:
    """Observer that logs events to db and sync pet current state."""

    def __init__(self,
                 session_factory: Callable[[], Session],
                 get_pet_domain) -> None:
        """get_pet_domain: returns the domain object (pet) to read its state."""
        self._session_factory = session_factory
        self._get_pet_domain = get_pet_domain

    def update(self, event: PetEvent) -> None:
        pet_domain = self._get_pet_domain()
        db = self._session_factory()
        try:
            pet_repo = PetRepository(db)
            event_repo = EventRepository(db)

            pet_model = pet_repo.save_pet_state(pet_domain)
            event_repo.add_event(pet_model, event)
        finally:
            db.close()
