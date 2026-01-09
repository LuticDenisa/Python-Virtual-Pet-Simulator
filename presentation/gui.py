from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from queue import Queue, Empty
from typing import Optional

from ..domain.pet import Pet
from ..domain.events import PetEvent, PetObserver


class TkQueueObserver(PetObserver):
    """
    Observer that doesnt touch directly the UI. 
    It puts the events in a queue, and the UI uses with root.after()
    """
    def __init__(self, queue: Queue[PetEvent]) -> None:
        self._queue = queue

    def update(self, event: PetEvent) -> None:
        self._queue.put(event)


class PetApp(tk.Tk):
    def __init__(self, pet: Pet, tick_ms: int = 5000) -> None:
        super().__init__()
        self.pet = pet
        self.tick_ms = tick_ms

        self.title(f"Virtual Pet Simulator - {self.pet.name}")
        self.geometry("900x520")
        self.minsize(700, 500)

        # queue for events
        self.event_queue: Queue[PetEvent] = Queue()
        self.pet.attach(TkQueueObserver(self.event_queue))

        # layout UI
        self._build_ui()

        # start loops
        self.after(self.tick_ms, self._auto_tick)
        self.after(100, self._drain_events)
        self.after(300, self._refresh_stats)

        # when close the window - detach the observer
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def _build_ui(self) -> None:
        # main containers
        root = ttk.Frame(self, paddin=12)
        root.pack(fill="both", expand=True)

        left = ttk.Frame(root)
        left.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(root)
        right.pack(side="right", fill="y")

        # titlu and state
        self.lbl_name = ttk.Label(left, text=f"🐾 {self.pet.name}", font=("Segoe UI", 18, "bold"))
        self.lbl_name.pack(anchor="w", pady=(0,6))

        self.lbl_state = ttk.Label(left, text=f"State: -", font=("Segoe UI", 12))
        self.lbl_state.pack(anchor="w", pady=(0,12))

        # stats area - bars
        stats = ttk.LabelFrame(left, text="Stats", padding=10)
        stats.pack(fill="x", pady=(0,12))

        self.pb_hunger = self._stat_row(stats, "Hunger", 0)
        self.pb_energy = self._stat_row(stats, "Energy", 1)
        self.pb_health = self._stat_row(stats, "Health", 2)
        self.pb_happiness = self._stat_row(stats, "Happiness", 3)

        # buttons
        actions = ttk.LabelFrame(left, text="Actions", padding=10)
        actions.pack(fill="x", pady=(0,12))

        ttk.Button(actions, text="Feed", command=self._do_feed).grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        ttk.Button(actions, text="Play", command=self._do_play).grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        ttk.Button(actions, text="Sleep", command=self._do_sleep).grid(row=0, column=2, padx=6, pady=6, sticky="ew")
        ttk.Button(actions, text="Cure", command=self._do_cure).grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        for i in range(4):
            actions.grid_columnconfigure(i, weight=1)

        # event log
        log_frame = ttk.LabelFrame(left, text="Event log", padding=10)
        log_frame.pack(fill="both", expand=True)

        self.txt_log = tk.Text(log_frame, height=10, wrap="word")
        self.txt_log.pack(fill="both", expand=True)

        # right panel - setting and info
        settings = ttk.LabelFrame(right, text="Settings", padding=10)
        settings.pack(fill="x")

        ttk.Label(settings, text="Tick interval (seconds):").pack(anchor="w")

        self.tick_var = tk.IntVar(value=max(1, self.tick_ms // 1000))
        spin = ttk.Spinbox(settings, from_=1, to=60, textvariable=self.tick_var, width=6, command=self._apply_tick_interval)
        spin.pack(anchor="w", pady=(4, 10))

        ttk.Button(settings, text="Apply", command=self._apply_tick_interval).pack(anchor="w")

        help_box = ttk.LabelFrame(right, text="Tips", padding=10)
        help_box.pack(fill="x", pady=(12, 0))
        ttk.Label(help_box, text="- Keep hunger low\n- Let it sleep when sleepy\n- Play to increase happiness", justify="left").pack(anchor="w")

    def _stat_row(self, parent: ttk.Frame, label: str, row: int) -> ttk.Progressbar:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=6)
        pb = ttk.Progressbar(parent, orient="horizontal", mode="determinate", maximum=10, length=260)
        pb.grid(row=row, column=1, sticky="ew", pady=6)
        val = ttk.Label(parent, text="0/10")
        val.grid(row=row, column=2, sticky="e", padx=(10, 0), pady=6)

        parent.grid_columnconfigure(1, weight=1)
        pb._value_label = val
        return pb
    

    # actions
    def _do_feed(self) -> None:
        self.pet.feed()
    
    def _do_play(self) -> None:
        self.pet.play()

    def _do_sleep(self) -> None:
        self.pet.sleep()

    def _do_cure(self) -> None:
        self.pet.cure()

    # auto tick
    def _auto_tick(self) -> None:
        self.pet.tick()
        self.after(self.tick_ms, self._auto_tick)

    def _apply_tick_interval(self) -> None:
        seconds = int(self.tick_var.get())
        self.tick_ms = max(1, seconds) * 1000
        self._log_local(f"[INFO] Tick interval set to {seconds}s")

    # events and ui refresh
    def _drain_events(self) -> None:
        while True:
            try:
                event = self.event_queue.get_nowait()
            except Empty:
                break
            self._render_event(event)

        self.after(100, self._drain_events)

    def _render_event(self, event: PetEvent) -> None:
        ev = event.type.upper()

        if event.type == "tick":
            line = "[TICK]\n"
        else:
            line = f"[{ev}] {event.message}\n"

        self.txt_log.insert("end", line)
        self.txt_log.see("end")

    def _refresh_stats(self) -> None:
        s = self.pet.stats()

        self.lbl_state.config(text=f"State: {s['state']}")

        self._set_bar(self.pb_hunger, s["hunger"])
        self._set_bar(self.pb_energy, s["energy"])
        self._set_bar(self.pb_health, s["health"])
        self._set_bar(self.pb_happiness, s["happiness"])

        self.after(300, self._refresh_stats)
   
    def _set_bar(self, pb: ttk.Progressbar, value: int) -> None:
        pb["value"] = value
        pb._value_label.config(text=f"{value}/10")

    def _log_local(self, msg: str) -> None:
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.see("end")

    def _on_close(self) -> None:
        self.destroy()


def run_gui(pet_name: Optional[str] = None) -> None:
    name = pet_name or input("Enter your pet's name: ").strip() or "Pet"
    pet = Pet(name)
    app = PetApp(pet, tick_ms=4000)
    app.mainloop()
    



