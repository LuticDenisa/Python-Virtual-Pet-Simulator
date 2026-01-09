from dataclasses import dataclass
from typing import Protocol, Optional


@dataclass
class PetEvent:
    type: str
    message: str
    pet_name: Optional[str] = None


class PetObserver(Protocol):
    def update(self, event: PetEvent) -> None:
        ...

        