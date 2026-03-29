from dataclasses import dataclass, field
from typing import List, Optional


class Owner:
    """Represents a pet owner who manages pets and schedules."""

    def __init__(self, name: str, available_time: float):
        self.name = name
        self.available_time = available_time
        self.pets: List[Pet] = []

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner's list of pets."""
        pass

    def get_pets(self) -> List["Pet"]:
        """Return the list of pets owned by this owner."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Assign a task to this pet."""
        pass

    def get_tasks(self) -> List["Task"]:
        """Return the list of tasks assigned to this pet."""
        pass


@dataclass
class Task:
    task_name: str
    duration: float
    priority: int
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def is_due(self) -> bool:
        """Determine whether this task is due."""
        pass


class Scheduler:
    """Handles schedule generation and constraints for pet care tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: List[Task] = []

    def generate_schedule(self) -> List[Task]:
        """Generate a schedule of tasks for the owner and their pets."""
        pass

    def sort_by_priority(self) -> None:
        """Sort the scheduler tasks by priority."""
        pass

    def check_time_constraints(self) -> bool:
        """Check if scheduled tasks fit within the owner's available time."""
        pass
