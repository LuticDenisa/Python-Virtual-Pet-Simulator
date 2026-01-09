from .events import PetEvent, PetObserver


class ConsoleObserver:
    """show all events in the console"""

    def update(self, event: PetEvent) -> None:
        if event.type == "tick":
            print("[TICK]")
        else:
            print(f"[{event.type.upper()}] {event.message}")


class DangerAlertObserver:
    """show special alerts when pet is in danger"""

    def update(self, event: PetEvent) -> None:
        if event.type == "danger":
            print(f"!!! ALERT:", event.message)

