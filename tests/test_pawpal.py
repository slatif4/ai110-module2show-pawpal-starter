import pytest
from pawpal_system import Pet, Task


def test_mark_complete():
    task = Task(task_name="Feed", duration=0.5, priority=1, frequency="daily", pet_name="Buddy")
    assert task.completed is False
    assert task.last_completed is None

    task.mark_complete()

    assert task.completed is True
    assert task.last_completed is not None


def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", age=3)
    task = Task(task_name="Walk", duration=1.0, priority=2, frequency="daily", pet_name="Buddy")

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1
