from __future__ import annotations
from typing import List

from .events import PetEvent, PetObserver
from .states import PetState, HappyState, HungryState, SickState, SleepyState


class Pet:
    def __init__(self, name: str) -> None:
        self.name = name

        self.hunger = 3
        self.energy = 7
        self.health = 8
        self.happiness = 7

        # state pattern
        self._state: PetState = HappyState()

        # observer pattern
        self._observers: List[PetObserver] = []

    # -- Observer API --
    def attach(self, observer: PetObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: PetObserver) -> None:
        self._observers.remove(observer)

    def _notify(self, event: PetEvent) -> None:
        for observer in list(self._observers):
            observer.update(event)

    def _notify_need(self, message: str) -> None:
        self._notify(PetEvent("need", message, pet_name=self.name))

    def _notify_danger(self, message: str) -> None:
        self._notify(PetEvent("danger", message, pet_name=self.name))

    # -- State management --
    @property
    def state(self) -> str:
        return self._state.name

    def change_state(self, new_state: PetState) -> None:
        self._state = new_state
        self._state.on_enter(self)

        self._notify(
            PetEvent("state_changed",
                     f"{self.name} is now {self._state.name}",
                     pet_name=self.name)
        )

        if self._state.name == "hungry":
            self._notify_need(f"{self.name} is hungry! Try feeding them.")
        elif self._state.name == "sleepy":
            self._notify_need(f"{self.name} is sleepy. Maybe let them sleep.")
        elif self._state.name == "sick":
            self._notify_need(f"{self.name} feels sick. You should cure them.") 


    def _recalculate_state_from_stats(self) -> None:
        new_state: PetState

        if self.health <= 4:
            new_state = SickState()
        elif self.hunger >= 7:
            new_state = HungryState()
        elif self.energy <= 3:
            new_state = SleepyState()
        else:
            new_state = HappyState()

        if new_state.name != self._state.name:
            self.change_state(new_state)
        
    # Actions
    def feed(self) -> None:
        self._state.feed(self)
        self._recalculate_state_from_stats()
        self._notify(PetEvent("action", f"{self.name} was fed.", pet_name=self.name))

    def play(self) -> None:
        self._state.play(self)
        self._recalculate_state_from_stats()
        self._notify(PetEvent("action", f"You played with {self.name}.", pet_name=self.name))

    def sleep(self) -> None:
        self._state.sleep(self)
        self._recalculate_state_from_stats()
        self._notify(PetEvent("action", f"{self.name} went to sleep.", pet_name=self.name))

    def cure(self) -> None:
        self._state.cure(self)
        self._recalculate_state_from_stats()
        self._notify(PetEvent("action", f"{self.name} received medicine.", pet_name=self.name))

    def tick(self) -> None:
        self._state.tick(self)
        self._recalculate_state_from_stats()
        self._notify(PetEvent("tick", "", pet_name=self.name))
        if self.happiness <= 3 and self.energy >= 4:
            self._notify_need(f"{self.name} looks bored. Try playing with them!")

    

    def stats(self) -> dict:
        self._recalculate_state_from_stats()
        
        return{
            "name": self.name,
            "state": self.state,
            "hunger": self.hunger,
            "energy": self.energy,
            "health": self.health,
            "happiness": self.happiness
        }