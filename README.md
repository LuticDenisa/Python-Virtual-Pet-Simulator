# 🐾 Virtual Pet Simulator

*A Python application using the State and Observer design patterns*

This project implements a simple **virtual pet simulator**, inspired by Tamagotchi.
The pet has needs, emotions, and changing behavior base on time, interactions and internal conditions.

The application uses:
-  **State Pattern (Behavioral)** - to model pet behavior based on its current condition
-  **Observer Pattern (Behavioral)** - to broadcast events (state changes, needs, actions, time passing)

Time passes automatically using a backgroun thread creating a dynamic and interactice experience.

## 🎮 Game Rules and Atributes
Each pet has 5 dynamic attributes controlling its behavior:
### Hunger
- increases over time
- decreases when feeding
- increases slightly when playing
- decreases slightly when sleeping

### Energy
- decreases over time
- decreases when plying
- restored when sleeping

### Happiness
- increases when playing
- decreases if: hunger is too high or energy is too low

### Health
- decreases if the pet remains hungry
- decreases more rapidly in sick state
- restored when the pet is cured

### Behavioral State
The pet can be in one of four states, determined by attribute thresholds:

| Option | Type | 
|--------|------|
| `healt <= 4` | Sick | 
| `hunger >= 7` | Hungry | 
| `energy <= 3` | Sleepy | 
| otherwise | Happy | 

### Time System
A background thread triggers a **tick** every few seconds:
- `hunger += 1`
- `energy -= 1`
- `happiness -= 1` (if hunger or energy are in critical ranges)

## 🧠 Design Pattern #1: State Pattern
**Why State Pattern?**

The pet's behavior depends on its current state. Feeding, playing or sleeping should not behave the same way when the pet is:
- Happy
- Hungry
- Sleepy
- Sick

Using the State Pattern avoids large `if/elif/else` blocks in the Pet class and makes behavior modular and easy to extend.

**Where it is implemented**

File: `domain/states.py`
Classes:
- `PetState` (abstract)
- `HappyState`
- `HungryState`
- `SleepyState`
- `SickState`
  
The `Pet` class delegates actions such as `feed`, `play`, `sleep` and `tick` to the active state object.

## 🧠 Design Pattern #2: Observer Pattern
**Why Observer Pattern?**

The system needs to react automatically when
- the pet state changes
- time passes (`tick`)
- the pet has a need (hungru, sleepy etc.)
- the pet is in danger (very low health)
- user actions occur

Observers allow components (console, ui, logs, db) to react without tightly coupling them to the pet logic.

**Where it is implemented**

Files: 
- `domain/events.py` - event & observer interfaces
- `domain/observers.py` - console + alert observers
- `infrastructure/db_observers.py` - logs events to db
- `domain/pet.py` - subject that notifies observers

**Examples of events**
- `[ACTION] Misi was fed.`
- `[STATE_CHANGED] Misi is now hungy!`
- `[NEED] Misi is hungry! Try feeding them`
- `[TICK]`
- `!!! ALERT: Pet is very sick!`

## 🏃 Running the application
### Install dependencies
```
pip install -r requirements.txt
```

### Start the CLI
```
python -m virtual_pet
```





