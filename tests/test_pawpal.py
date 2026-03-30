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


def test_sort_by_time_returns_correct_order():
    from pawpal_system import Owner, Scheduler

    owner = Owner(name="Jordan", available_time=100.0)
    pet = Pet(name="Mochi", species="cat", age=2)
    task_a = Task(task_name="Groom", duration=30.0, priority=1, frequency="daily", pet_name="Mochi")
    task_b = Task(task_name="Walk", duration=10.0, priority=2, frequency="daily", pet_name="Mochi")
    task_c = Task(task_name="Play", duration=20.0, priority=3, frequency="daily", pet_name="Mochi")

    pet.add_task(task_a)
    pet.add_task(task_b)
    pet.add_task(task_c)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    sorted_by_time = scheduler.sort_by_time()

    durations = [task.duration for _, task in sorted_by_time]
    assert durations == [10.0, 20.0, 30.0]


def test_recurring_task_sets_next_due():
    from datetime import date, timedelta

    task = Task(task_name="Feed", duration=0.5, priority=1, frequency="daily", pet_name="Buddy")
    task.mark_complete()

    expected_next_due = (date.today() + timedelta(days=1)).isoformat()
    assert task.next_due == expected_next_due


def test_detect_conflicts_returns_warning():
    from pawpal_system import Owner, Scheduler

    owner = Owner(name="Jordan", available_time=120.0)
    pet = Pet(name="Mochi", species="cat", age=2)
    task1 = Task(task_name="Feed", duration=5.0, priority=1, frequency="daily", pet_name="Mochi", next_due="2026-04-01")
    task2 = Task(task_name="Play", duration=10.0, priority=2, frequency="daily", pet_name="Mochi", next_due="2026-04-01")

    scheduler = Scheduler(owner)
    scheduler.schedule = [(pet, task1), (pet, task2)]

    conflicts = scheduler.detect_conflicts()

    assert conflicts
    assert "Conflict" in conflicts[0]
