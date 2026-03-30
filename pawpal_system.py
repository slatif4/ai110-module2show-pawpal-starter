from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional


class Owner:
    """Represents a pet owner who manages pets and schedules."""

    def __init__(self, name: str, available_time: float):
        self.name = name
        self.available_time = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's list of pets."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from the owner's list of pets."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List["Pet"]:
        """Return the list of pets owned by this owner."""
        return self.pets


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Assign a task to this pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List["Task"]:
        """Return the list of tasks assigned to this pet."""
        return self.tasks


@dataclass
class Task:
    task_name: str
    duration: float
    priority: int
    frequency: str
    pet_name: str
    next_due: Optional[str] = None
    completed: bool = False
    last_completed: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True
        today = date.today()
        self.last_completed = today.isoformat()

        if self.frequency.lower() == "daily":
            next_due_date = today + timedelta(days=1)
            self.next_due = next_due_date.isoformat()
        elif self.frequency.lower() == "weekly":
            next_due_date = today + timedelta(days=7)
            self.next_due = next_due_date.isoformat()
        else:
            self.next_due = None

    def is_due(self) -> bool:
        """Determine whether this task is due."""
        if self.last_completed is None:
            return True
        return self.frequency.lower() == "daily"


class Scheduler:
    """Handles schedule generation and constraints for pet care tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: List[tuple] = []

    def generate_schedule(self) -> List[tuple]:
        """Generate a schedule of tasks for the owner and their pets."""
        candidates: List[tuple] = []
        for pet in self.owner.get_pets():
            for task in pet.get_tasks():
                if task.is_due():
                    candidates.append((pet, task))

        candidates.sort(key=lambda pair: pair[1].priority, reverse=True)

        selected: List[tuple] = []
        total_time = 0.0
        for pet, task in candidates:
            if total_time + task.duration <= self.owner.available_time:
                selected.append((pet, task))
                total_time += task.duration

        self.schedule = selected
        return self.schedule

    def sort_by_priority(self) -> None:
        """Sort the scheduler tasks by priority."""
        self.schedule.sort(key=lambda pair: pair[1].priority, reverse=True)

    def sort_by_time(self) -> list:
        """Sort scheduled tasks by duration and return sorted list."""
        sorted_schedule = sorted(self.schedule, key=lambda pair: pair[1].duration)
        return sorted_schedule

    def filter_tasks(self, completed=None, pet_name=None) -> list:
        """Filter scheduled tasks by completion status and/or pet name."""
        results = []
        for pet, task in self.schedule:
            if completed is not None and task.completed != completed:
                continue
            if pet_name is not None and pet.name != pet_name:
                continue
            results.append((pet, task))
        return results

    def detect_conflicts(self) -> list:
        """Return list of warnings for tasks with same pet and same next_due time."""
        conflicts = []
        key_map = {}
        for pet, task in self.schedule:
            if task.next_due is None:
                continue
            key = (pet.name, task.next_due)
            key_map.setdefault(key, []).append(task)

        for (pet_name, next_due), tasks in key_map.items():
            if len(tasks) > 1:
                conflicts.append(
                    f"Conflict: {len(tasks)} tasks for {pet_name} are due at the same time ({next_due})."
                )
        return conflicts

    def check_time_constraints(self) -> bool:
        """Check if scheduled tasks fit within the owner's available time."""
        total = sum(task.duration for _, task in self.schedule)
        return total <= self.owner.available_time
