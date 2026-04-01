from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_marks_completed() -> None:
    task = Task(
        task_name="Take a walk",
        category="exercise",
        duration=20,
        priority=3,
        preferred_time="08:00",
        is_required=True,
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_task_count() -> None:
    pet = Pet(
        name="Buddy",
        species="dog",
        age=4,
        energy_level="high",
        special_needs="none",
    )

    assert len(pet.tasks) == 0

    task = Task(
        task_name="Feed breakfast",
        category="feeding",
        duration=15,
        priority=4,
        preferred_time="08:30",
        is_required=True,
    )

    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_scheduler_sort_by_time_orders_tasks_by_time() -> None:
    owner = Owner(name="Alex", daily_time_available=60, preferences={})
    pet = Pet(name="Buddy", species="dog", age=4, energy_level="high", special_needs="none")

    task1 = Task(
        task_name="Lunch",
        category="feeding",
        duration=20,
        priority=2,
        preferred_time="12:30",
        is_required=False,
    )
    task2 = Task(
        task_name="Morning walk",
        category="exercise",
        duration=30,
        priority=3,
        preferred_time="08:00",
        is_required=True,
    )
    task3 = Task(
        task_name="Evening play",
        category="play",
        duration=15,
        priority=1,
        preferred_time="18:00",
        is_required=False,
    )

    scheduler = Scheduler(owner=owner, pet=pet, tasks=[task1, task2, task3])
    scheduler.sort_by_time()

    assert [task.task_name for task in scheduler.tasks] == ["Morning walk", "Lunch", "Evening play"]


def test_daily_recurring_task_creates_next_occurrence() -> None:
    today = date.today()
    task = Task(
        task_name="Feed breakfast",
        category="feeding",
        duration=15,
        priority=4,
        preferred_time="08:30",
        is_required=True,
        recurrence="daily",
        due_date=today,
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.recurrence == "daily"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_scheduler_detects_same_time_conflicts() -> None:
    owner = Owner(name="Alex", daily_time_available=90, preferences={})
    pet1 = Pet(name="Buddy", species="dog", age=3, energy_level="high", special_needs="none")
    pet2 = Pet(name="Mittens", species="cat", age=2, energy_level="medium", special_needs="none")

    task1 = Task(
        task_name="Feed breakfast",
        category="feeding",
        duration=15,
        priority=4,
        preferred_time="08:00",
        is_required=True,
        pet_name="Buddy",
    )
    task2 = Task(
        task_name="Morning walk",
        category="exercise",
        duration=30,
        priority=5,
        preferred_time="08:00",
        is_required=True,
        pet_name="Buddy",
    )
    task3 = Task(
        task_name="Grooming",
        category="care",
        duration=20,
        priority=2,
        preferred_time="08:00",
        is_required=False,
        pet_name="Mittens",
    )

    scheduler = Scheduler(owner=owner, pet=pet1, tasks=[task1, task2, task3])
    warnings = scheduler.detect_conflicts()

    assert any("same pet Buddy" in warning for warning in warnings)
    assert any("between pets" in warning for warning in warnings)
