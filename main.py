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


if __name__ == "__main__":
    main()
