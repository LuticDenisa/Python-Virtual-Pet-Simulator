import threading
import time

from ..domain.pet import Pet
from ..domain.observers import ConsoleObserver, DangerAlertObserver
from ..infrastructure.db import Base, engine, SessionLocal
from ..infrastructure.db_observers import DbEventLoggerObserver


def init_db():
    Base.metadata.create_all(bind=engine)


def print_menu():
    print("\nChoose action:")
    print("1. Feed")
    print("2. Play")
    print("3. Sleep")
    print("4. Cure")
    print("5. Show Status")
    print("0. Exit")


def run_cli():
    init_db()

    name = input("Enter your pet's name: ")
    pet = Pet(name)

    pet.attach(ConsoleObserver())
    pet.attach(DangerAlertObserver())
    pet.attach(DbEventLoggerObserver(SessionLocal, lambda: pet))

    print(f"Virtual pet '{name}' created!\n")

    # -- background thread for time --
    stop_event = threading.Event()

    def time_loop():
        while not stop_event.is_set():
            time.sleep(5)
            pet.tick()

    t = threading.Thread(target=time_loop, daemon=True)
    t.start()
    # ------------------------------------------------

    try:
        while True:
            print_menu()
            choice = input(">>> ").strip()

            if choice == "1":
                pet.feed()
            elif choice == "2":
                pet.play()
            elif choice == "3":
                pet.sleep()
            elif choice == "4":
                pet.cure()
            elif choice == "5":
                print(pet.stats())
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        stop_event.set()
        t.join()