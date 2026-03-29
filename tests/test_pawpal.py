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


def test_scheduler_respects_priority_and_time():
    from pawpal_system import Owner, Scheduler

    owner = Owner(name="Jordan", available_time=120.0)
    pet = Pet(name="Mochi", species="cat", age=2)
    high = Task(task_name="Urgent meds", duration=90.0, priority=3, frequency="daily", pet_name="Mochi")
    medium = Task(task_name="Walk", duration=45.0, priority=2, frequency="daily", pet_name="Mochi")
    low = Task(task_name="Play", duration=30.0, priority=1, frequency="daily", pet_name="Mochi")

    pet.add_task(high)
    pet.add_task(medium)
    pet.add_task(low)
    owner.add_pet(pet)

    schedule = Scheduler(owner).generate_schedule()

    assert len(schedule) == 2
    assert schedule[0][1].task_name == "Urgent meds"
    assert schedule[1][1].task_name == "Play"


def test_scheduler_no_duplicates_for_same_task():
    from pawpal_system import Owner, Scheduler

    owner = Owner(name="Jordan", available_time=30.0)
    pet = Pet(name="Mochi", species="cat", age=2)
    task = Task(task_name="Feed", duration=30.0, priority=3, frequency="daily", pet_name="Mochi")
    pet.add_task(task)
    owner.add_pet(pet)

    schedule = Scheduler(owner).generate_schedule()

    assert len(schedule) == 1
    assert schedule[0][1].task_name == "Feed"
