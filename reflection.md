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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
