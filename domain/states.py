from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pet import Pet  


class PetState(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...
    
    def on_enter(self, pet: "Pet") -> None:
        pass

    # -- User actions --
    def feed(self, pet: "Pet") -> None:
        pet.hunger = max(0, pet.hunger - 3)
        pet.happiness = min(10, pet.happiness + 1)

    def play(self, pet: "Pet") -> None:
        pet.happiness = min(10, pet.happiness + 2)
        pet.energy = max(0, pet.energy - 2)
        pet.hunger = min(10, pet.hunger + 1)

    def sleep(self, pet: "Pet") -> None:
        pet.energy = min(10, pet.energy + 4)
        pet.hunger = max(0, pet.hunger - 1)

    def cure(self, pet: "Pet") -> None:
        pet.health = min(10, pet.health + 3)

    # -- time passinh -- 
    def tick(self, pet: "Pet") -> None:
        pet.hunger = min(10, pet.hunger + 1)
        pet.energy = max(0, pet.energy - 1)

        if pet.hunger >= 7 or pet.energy <= 3:
            pet.happiness = max(0, pet.happiness - 1)


class HappyState(PetState):
    @property
    def name(self) -> str:
        return "happy"
    
    def tick(self, pet: "Pet") -> None:
        super().tick(pet)


class HungryState(PetState):
    @property
    def name(self) -> str:
        return "hungry"
    
    def feed(self, pet: "Pet") -> None:
        super().feed(pet)

    def tick(self, pet: "Pet") -> None:
        super().tick(pet)

        if pet.hunger >= 8:
            pet.health = max(0, pet.health - 1)


class SleepyState(PetState):
    @property
    def name(self) -> str:
        return "sleepy"
    
    def sleep(self, pet: "Pet") -> None:
        super().sleep(pet)

    def play(self, pet: "Pet") -> None:
        pet.happiness = min(10, pet.happiness + 1)
        pet.energy = max(0, pet.energy - 3)
        pet.hunger = min(10, pet.hunger + 1)

    def tick(self, pet: "Pet") -> None:
        super().tick(pet)


class SickState(PetState):
    @property
    def name(self) -> str:
        return "sick"
    
    def cure(self, pet: "Pet") -> None:
        super().cure(pet)

    def tick(self, pet: "Pet") -> None:
        super().tick(pet)

        pet.health = max(0, pet.health - 1)
        pet.happiness = max(0, pet.happiness - 1)
        if pet.health <= 2:
            pet._notify_danger("Pet is very sick!")
        if pet.hunger >= 8:
            pet.health = max(0, pet.health - 1)

    


