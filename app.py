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

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, daily_time_available=120, preferences={})
else:
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name

if "pet" not in st.session_state:
    st.session_state.pet = Pet(
        name=pet_name,
        species=species,
        age=2,
        energy_level="medium",
        special_needs="none",
    )
else:
    st.session_state.pet.update_info(name=pet_name, species=species)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    category = st.selectbox("Category", ["feeding", "exercise", "grooming", "health", "training"], index=0)
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)

preferred_time = st.text_input("Preferred time", value="08:00")
is_required = st.checkbox("Required task", value=True)

priority_map = {"low": 1, "medium": 2, "high": 3}
priority = priority_map[priority_label]

if st.button("Add task"):
    new_task = Task(
        task_name=task_title,
        category=category,
        duration=int(duration),
        priority=priority,
        preferred_time=preferred_time,
        is_required=is_required,
    )
    st.session_state.pet.add_task(new_task)
    st.session_state.tasks.append(new_task)

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Task": task.task_name,
                "Category": task.category,
                "Duration": task.duration,
                "Priority": task.priority,
                "Preferred time": task.preferred_time,
                "Required": task.is_required,
            }
            for task in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("No tasks available. Add a task first.")
    else:
        scheduler = Scheduler(
            owner=st.session_state.owner,
            pet=st.session_state.pet,
            tasks=list(st.session_state.tasks),
        )
        scheduler.sort_by_time()
        daily_plan = scheduler.generate_plan()

        if scheduler.conflict_warnings:
            for warning in scheduler.conflict_warnings:
                st.warning(warning)

        if daily_plan:
            st.success("Schedule generated successfully.")
            st.table(
                [
                    {
                        "Task": task.task_name,
                        "Time": task.preferred_time,
                        "Duration": task.duration,
                        "Priority": task.priority,
                        "Required": task.is_required,
                    }
                    for task in daily_plan
                ]
            )
            st.markdown("**Plan details:**")
            st.write(scheduler.explain_plan())
        else:
            st.info("No tasks could be scheduled based on current availability.")
