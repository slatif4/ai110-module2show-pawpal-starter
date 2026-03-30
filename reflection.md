# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has four classes:
- Owner: stores the name of the owner and the available time per day.
- Pet: stores the name of the pet, type of pet, and age of pet.
- Task: stores the name of the task, duration of task in minutes, level of priority of task, and status of task.
- Scheduler: takes an Owner with their pets and tasks, sorts by level of priority and time constraint, and generates a daily schedule.

The three major user operations are:
- Adding a pet.
- Adding/editing tasks with duration and level of priority.
- Generating a daily schedule based on available time and level of priority.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After asking Claude to review the skeleton, I made a number of minor changes. I added last_completed to the Task data structure to allow the scheduler to determine if a task is due. I added pet_name to the Task data structure to allow the scheduler to tag which pet the task is for. I also changed the schedule list in the Scheduler data structure to hold pairs of Pet and Task rather than just tasks, providing more context to the scheduler in creating the daily plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers two main constraints: available time and task priority. The available time is set by the owner and limits how many tasks can be scheduled in a day. Tasks are added until the total duration reaches the limit. Priority is an integer where higher numbers mean 
more important tasks, so the scheduler always picks the most critical tasks first when time is limited.

I decided that time and priority mattered most because a pet owner has a fixed amount of time each day, and some tasks, like medication, are 
more urgent than others, like grooming.Frequency (daily vs weekly) also plays a role; only tasks that are due today are included in the schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler detects conflicts by checking for exact next_due date matches for the same pet, rather than checking for overlapping time 
windows. This means two tasks scheduled at different times on the same day would not trigger a conflict warning. This tradeoff keeps the logic simple and readable while still catching the most common scheduling problem, duplicate tasks on the same day for the same pet.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude in VS Code as my primary AI tool throughout all phases 
of this project. In Phase 1, I used it to brainstorm the UML design 
and generate the Mermaid class diagram. In Phase 2, I used Agent mode 
to implement the full class logic and create the demo script. In Phase 
4, I used it to implement sorting, filtering, conflict detection, and 
recurring task logic. The most helpful prompts were specific ones that 
referenced exact file names and described the exact behavior needed.

**b. Judgment and verification**

At one point Claude suggested implementing detect_conflicts() using 
next_due date matching. I evaluated this and accepted it but noted it 
as a tradeoff — it only catches exact date matches, not overlapping 
time windows. I verified every AI suggestion by running pytest and 
testing the live Streamlit app in the browser before committing.

---

## 4. Testing and Verification

**a. What you tested**

I tested seven core behaviors: task completion status, adding tasks 
to pets, scheduler priority and time constraints, duplicate task 
prevention, sorting by duration, recurring task next_due calculation, 
and conflict detection. These tests were important because they verify 
both happy paths and edge cases like duplicate tasks and time limits.

**b. Confidence**

I am confident at 4 out of 5 stars that the scheduler works correctly 
for core use cases. All 7 tests pass consistently. Edge cases I would 
test next include a pet with no tasks, an owner with zero available 
time, tasks with the same priority, and weekly recurring tasks crossing 
month boundaries.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the algorithmic layer came together in 
Phase 4. The sorting, filtering, conflict detection, and recurring 
task logic all worked after fixing one missing attribute. Using Claude 
in VS Code to implement multiple features in one pass saved a lot of time.

**b. What you would improve**

If I had another iteration I would add a time-slot system so tasks 
could be scheduled at specific times of day rather than just fitting 
within a total duration. I would also improve conflict detection to 
check across different pets.

**c. Key takeaway**

The most important thing I learned is that AI tools are powerful 
collaborators but require a human architect to stay in control. Claude 
could generate code quickly, but I had to verify every suggestion by 
running tests and checking the live app. Being specific with prompts 
and using separate chat sessions for each phase kept the work organized.
