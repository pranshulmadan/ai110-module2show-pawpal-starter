from pawpal_system import Pet, Task


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
