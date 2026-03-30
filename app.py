import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
available_time_minutes = st.number_input("Available time today (minutes)", min_value=10, max_value=1440, value=120)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Click to generate a task plan based on your tasks, priorities, and available time.")

if st.button("Generate schedule"):
    if not owner_name or not pet_name:
        st.error("Please enter owner and pet names before generating a schedule.")
    elif not st.session_state.tasks:
        st.error("No tasks to schedule. Add tasks first.")
    else:
        owner = Owner(name=owner_name, available_time=float(available_time_minutes))
        pet = Pet(name=pet_name, species=species, age=1)

        priority_map = {"low": 1, "medium": 2, "high": 3}
        for t in st.session_state.tasks:
            task_obj = Task(
                task_name=t["title"],
                duration=float(t["duration_minutes"]),
                priority=priority_map.get(t["priority"], 1),
                frequency="daily",
                pet_name=pet.name,
            )
            pet.add_task(task_obj)

        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()

        if not schedule:
            st.info("No tasks fit in the available time window. Try more available time or shorter tasks.")
        else:
            st.success("Schedule generated successfully!")
            st.markdown("### Today's plan")
            output = []
            for idx, (scheduled_pet, scheduled_task) in enumerate(schedule, start=1):
                output.append(
                    {
                        "Order": idx,
                        "Task": scheduled_task.task_name,
                        "Pet": scheduled_pet.name,
                        "Duration (min)": scheduled_task.duration,
                        "Priority": scheduled_task.priority,
                    }
                )
            st.table(output)

            chosen_minutes = sum(task.duration for _, task in schedule)
            st.markdown(f"**Total scheduled time:** {chosen_minutes} minutes")
            st.markdown(
                f"**Available time:** {available_time_minutes} minutes\n"
                "**Reasoning:** Tasks are selected by descending priority and included while staying within the available time limit."
            )

            # New algorithmic feature outputs
            sorted_schedule = scheduler.sort_by_time()
            if sorted_schedule:
                st.markdown("### Sorted schedule (by task duration)")
                sorted_output = []
                for idx, (scheduled_pet, scheduled_task) in enumerate(sorted_schedule, start=1):
                    sorted_output.append(
                        {
                            "Order": idx,
                            "Task": scheduled_task.task_name,
                            "Pet": scheduled_pet.name,
                            "Duration (min)": scheduled_task.duration,
                            "Priority": scheduled_task.priority,
                        }
                    )
                st.table(sorted_output)

            conflicts = scheduler.detect_conflicts()
            if conflicts:
                st.markdown("### Conflicts detected")
                for conflict in conflicts:
                    st.warning(conflict)

            incomplete_tasks = scheduler.filter_tasks(completed=False)
            st.markdown("### Incomplete tasks filter")
            if incomplete_tasks:
                for pet, task in incomplete_tasks:
                    st.info(f"{task.task_name} (Pet: {pet.name}, Duration: {task.duration} min, Priority: {task.priority})")
            else:
                st.info("No incomplete tasks at the moment.")

