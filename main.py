from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(
        name="Alex",
        daily_time_available=90,
        preferences={"preferred_categories": ["exercise", "feeding"]},
    )

    buddy = Pet(
        name="Buddy",
        species="dog",
        age=3,
        energy_level="high",
        special_needs="none",
    )

    mittens = Pet(
        name="Mittens",
        species="cat",
        age=2,
        energy_level="medium",
        special_needs="indoor only",
    )

    morning_walk = Task(
        task_name="Morning walk",
        category="exercise",
        duration=30,
        priority=5,
        preferred_time="08:00",
        is_required=True,
    )

    breakfast = Task(
        task_name="Feed breakfast",
        category="feeding",
        duration=15,
        priority=4,
        preferred_time="08:30",
        is_required=True,
    )

    play_time = Task(
        task_name="Play with toy",
        category="play",
        duration=20,
        priority=3,
        preferred_time="08:00",
        is_required=False,
        pet_name="Mittens",
    )

    grooming = Task(
        task_name="Grooming",
        category="care",
        duration=25,
        priority=2,
        preferred_time="18:00",
        is_required=False,
        pet_name="Mittens",
    )

    buddy.add_task(morning_walk)
    buddy.add_task(breakfast)
    mittens.add_task(play_time)
    mittens.add_task(grooming)

    # Add tasks out of order and introduce same-time conflicts.
    late_snack = Task(
        task_name="Late snack",
        category="feeding",
        duration=10,
        priority=2,
        preferred_time="08:00",
        is_required=False,
        pet_name="Buddy",
    )
    buddy.add_task(late_snack)

    out_of_order_tasks = [grooming, breakfast, late_snack, morning_walk, play_time]

    scheduler = Scheduler(owner=owner, pet=buddy, tasks=out_of_order_tasks)

    print("Tasks before sort_by_time:")
    for task in scheduler.tasks:
        print(f"- {task.task_name} ({task.pet_name}) at {task.preferred_time}")

    scheduler.sort_by_time()
    print("\nTasks after sort_by_time:")
    for task in scheduler.tasks:
        print(f"- {task.task_name} ({task.pet_name}) at {task.preferred_time}")

    print("\nConflict warnings:")
    warnings = scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No conflicts detected.")


if __name__ == "__main__":
    main()
