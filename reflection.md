# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core tasks: Should be able to add a pet, schedule feeding sessions, and see what tasks need to be done today.

1st class: Owner - Represents the person caring for the pet.

Attributes:
name
daily_time_available
preferences

Methods:
set_time_available()
update_preferences()

2nd class: Pet - represents the pet

Attributes:
name
species
age
energy_level
special_needs

Methods:
update_info()
get_summary()

3rd class: Task - Reperesents a pet care task

Attributes:
task_name
category
duration
priority
preferred_time
is_required

Methods:
edit_task()
mark_complete()
fits_time(available_time)


4th class: Scheduler - Creates the daily plan

Attributes:
owner
pet
tasks
daily_plan

Methods:
generate_plan()
sort_tasks_by_priority()
select_tasks()
explain_plan()

I chose four classes: Owner, Pet, Task, and Scheduler. Owner stores information about the pet owner, like their name, available time, and preferences. Pet stores the pet’s basic details, such as name, species, age, energy level, and special needs.

Task represents each care activity the pet needs, like feeding, walking, or grooming, along with details like duration, priority, and preferred time. Scheduler is the main planning class that uses the owner, pet, and task information to build a daily plan by sorting tasks and selecting the ones that fit the owner’s available time.

classDiagram
    class Owner {
        +String name
        +int daily_time_available
        +Map preferences
        +set_time_available()
        +update_preferences()
    }

    class Pet {
        +String name
        +String species
        +int age
        +String energy_level
        +String special_needs
        +update_info()
        +get_summary()
    }

    class Task {
        +String task_name
        +String category
        +int duration
        +int priority
        +String preferred_time
        +bool is_required
        +edit_task()
        +mark_complete()
        +fits_time(available_time)
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +List~Task~ tasks
        +List~Task~ daily_plan
        +generate_plan()
        +sort_tasks_by_priority()
        +select_tasks()
        +explain_plan()
    }

    Scheduler --> Owner
    Scheduler --> Pet
    Scheduler --> Task : manages
    Pet --> Task : has

**b. Design changes**

- Did your design change during implementation?
Yes my design changed during implementation.
- If yes, describe at least one change and why you made it.

One change I made was adding a clearer connection between Pet and Task in the design/code. I made this change because my original UML showed that a pet “has” tasks, but the code did not actually store or link tasks to a specific pet. Updating that relationship made the system more logical, since care tasks like feeding, walking, and grooming are meant to belong to a pet’s care plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler checks a few key constraints: owner available time, task priority, whether a task is required, task completion status, and owner preferences for preferred/avoided categories. I prioritized required tasks first, then preferred categories and higher-priority tasks, because a pet owner needs essential care done before optional items, and preferences help make the daily plan more useful.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One different tradeoff is that the scheduler only returns warnings instead of trying to fully resolve overlaps. That is reasonable because it keeps the planner simple and still surfaces scheduling issues for the owner without making the app crash or overcomplicating the algorithm.

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
