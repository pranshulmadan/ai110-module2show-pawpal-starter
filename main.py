from pawpal_system import Owner, Pet, Task


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
        preferred_time="10:00",
        is_required=False,
    )

    grooming = Task(
        task_name="Grooming",
        category="care",
        duration=25,
        priority=2,
        preferred_time="18:00",
        is_required=False,
    )

    buddy.add_task(morning_walk)
    buddy.add_task(breakfast)
    mittens.add_task(play_time)
    mittens.add_task(grooming)

    print("Today's Schedule")
    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.daily_time_available} minutes\n")

    for pet in (buddy, mittens):
        for task in pet.tasks:
            print(
                f"- {task.task_name} for {pet.name} at {task.preferred_time} "
                f"({task.duration} min, category={task.category})"
            )


if __name__ == "__main__":
    main()
