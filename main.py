from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # 2. Create an Owner named "Alex" with 120 minutes available
    owner = Owner(name="Alex", available_time=120.0)

    # 3. Create two pets: "Buddy" (Dog, age 4) and "Whiskers" (Cat, age 2)
    buddy = Pet(name="Buddy", species="Dog", age=4)
    whiskers = Pet(name="Whiskers", species="Cat", age=2)

    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # 4. Add at least 3 tasks across the two pets with different priorities and durations
    tasks = [
        Task(task_name="Feed Buddy", duration=15, priority=5, frequency="daily", pet_name="Buddy"),
        Task(task_name="Walk Buddy", duration=30, priority=8, frequency="daily", pet_name="Buddy"),
        Task(task_name="Play with Whiskers", duration=25, priority=6, frequency="daily", pet_name="Whiskers"),
        Task(task_name="Clean Litter", duration=20, priority=9, frequency="daily", pet_name="Whiskers"),
        Task(task_name="Groom Buddy", duration=40, priority=4, frequency="weekly", pet_name="Buddy"),
    ]

    # assign tasks to pets
    buddy.add_task(tasks[0])
    buddy.add_task(tasks[1])
    buddy.add_task(tasks[4])
    whiskers.add_task(tasks[2])
    whiskers.add_task(tasks[3])

    # 5. Create a Scheduler and generate the schedule
    scheduler = Scheduler(owner)
    scheduled = scheduler.generate_schedule()

    # 6. Print a clean "Today's Schedule" to the terminal
    print("Today's Schedule")
    print("-----------------")
    print(f"Owner: {owner.name}")
    print(f"Available Time: {owner.available_time} minutes")
    print()

    total_used = 0.0
    if not scheduled:
        print("No tasks scheduled for today.")
    else:
        for pet, task in scheduled:
            print(f"- Pet: {pet.name} | Task: {task.task_name} | Duration: {task.duration} min | Priority: {task.priority}")
            total_used += task.duration

    print()
    print(f"Total Time Used: {total_used} minutes")

    # --- New algorithmic feature demos ---

    # 1. Add tasks out of order and print sorted results using sort_by_time()
    out_of_order_task1 = Task(task_name="Administer Medicine Buddy", duration=5, priority=10, frequency="daily", pet_name="Buddy")
    out_of_order_task2 = Task(task_name="Brush Whiskers", duration=10, priority=3, frequency="weekly", pet_name="Whiskers")
    buddy.add_task(out_of_order_task1)
    whiskers.add_task(out_of_order_task2)

    # Regenerate schedule to include new tasks
    scheduler.generate_schedule()
    sorted_by_time = scheduler.sort_by_time()

    print("\nSorted Schedule by Duration (after adding out-of-order tasks):")
    for pet, task in sorted_by_time:
        print(f"- {pet.name}: {task.task_name} ({task.duration} min)")

    # 2. Filter tasks by completion status using filter_tasks(completed=False)
    incomplete_tasks = scheduler.filter_tasks(completed=False)
    print("\nIncomplete Tasks:")
    for pet, task in incomplete_tasks:
        print(f"- {pet.name}: {task.task_name} (completed={task.completed})")

    # 3. Mark a task complete and show its next_due date
    if scheduler.schedule:
        task_to_complete = scheduler.schedule[0][1]
        task_to_complete.mark_complete()
        print(f"\nMarked complete: {task_to_complete.task_name}, next_due = {task_to_complete.next_due}")

    # 4. Add two tasks with same next_due for same pet and print conflict warnings from detect_conflicts()
    conflict_next_due = "2026-04-01"
    conflict_task1 = Task(task_name="Conflict Task A", duration=15, priority=1, frequency="weekly", pet_name="Buddy", next_due=conflict_next_due)
    conflict_task2 = Task(task_name="Conflict Task B", duration=20, priority=2, frequency="weekly", pet_name="Buddy", next_due=conflict_next_due)
    buddy.add_task(conflict_task1)
    buddy.add_task(conflict_task2)

    # Add conflict tasks into schedule for conflict detection
    scheduler.schedule.append((buddy, conflict_task1))
    scheduler.schedule.append((buddy, conflict_task2))

    conflicts = scheduler.detect_conflicts()
    print("\nConflict warnings:")
    if conflicts:
        for warning in conflicts:
            print(f"- {warning}")
    else:
        print("- No conflicts detected")


if __name__ == "__main__":
    main()
