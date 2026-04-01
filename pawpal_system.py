from __future__ import annotations

from dataclasses import dataclass, field


class Owner:
    def __init__(self, name: str, daily_time_available: int, preferences: dict):
        """Initialize a pet owner with availability and preferences."""
        self.name = name
        self.daily_time_available = daily_time_available
        self.preferences = preferences

    def set_time_available(self, minutes: int) -> None:
        """Update the owner's available time for the day."""
        self.daily_time_available = minutes

    def update_preferences(self, preferences: dict) -> None:
        """Update the owner's pet care preferences."""
        self.preferences = preferences


@dataclass
class Pet:
    name: str
    species: str
    age: int
    energy_level: str
    special_needs: str
    tasks: list[Task] = field(default_factory=list)

    def update_info(
        self,
        *,
        name: str | None = None,
        species: str | None = None,
        age: int | None = None,
        energy_level: str | None = None,
        special_needs: str | None = None,
    ) -> None:
        """Update pet details."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age
        if energy_level is not None:
            self.energy_level = energy_level
        if special_needs is not None:
            self.special_needs = special_needs

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def get_summary(self) -> str:
        """Return a short summary of the pet."""
        return (
            f"{self.name} is a {self.age}-year-old {self.species} "
            f"with energy level {self.energy_level} and special needs {self.special_needs}."
        )


@dataclass
class Task:
    task_name: str
    category: str
    duration: int
    priority: int
    preferred_time: str
    is_required: bool
    completed: bool = field(default=False)

    def edit_task(self, **kwargs) -> None:
        """Edit task properties with basic validation."""
        for key, value in kwargs.items():
            if not hasattr(self, key):
                continue
            if key == "duration" and value is not None and value < 0:
                raise ValueError("Task duration must be non-negative.")
            if key == "priority" and value is not None and value < 0:
                raise ValueError("Task priority must be non-negative.")
            setattr(self, key, value)

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def fits_time(self, available_time: int) -> bool:
        """Return True if this task can fit in the available time."""
        return self.duration <= available_time and not self.completed


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        """Initialize a scheduler with an owner, pet, and task list."""
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.daily_plan: list[Task] = []
        self.pet.tasks.extend(task for task in tasks if task not in self.pet.tasks)

    def generate_plan(self) -> list[Task]:
        """Build a daily plan from available tasks."""
        self.sort_tasks_by_priority()
        self.select_tasks()
        return self.daily_plan

    def _task_sort_key(self, task: Task) -> tuple[int, int, int, int]:
        """Return a sorting key for task prioritization."""
        preferred_categories = self.owner.preferences.get("preferred_categories", [])
        avoid_categories = self.owner.preferences.get("avoid_categories", [])
        preferred = isinstance(preferred_categories, list) and task.category in preferred_categories
        avoid = isinstance(avoid_categories, list) and task.category in avoid_categories
        return (
            int(task.completed),
            int(not task.is_required),
            int(not preferred),
            int(avoid),
            -task.priority,
        )

    def sort_tasks_by_priority(self) -> None:
        """Sort tasks so required and preferred items are chosen first."""
        self.tasks.sort(key=self._task_sort_key)

    def select_tasks(self) -> None:
        """Select tasks that fit into the owner's available time."""
        available_time = self.owner.daily_time_available
        self.daily_plan = []
        for task in self.tasks:
            if task.completed:
                continue
            if not task.fits_time(available_time):
                continue
            self.daily_plan.append(task)
            available_time -= task.duration

    def explain_plan(self) -> str:
        """Return a simple explanation of the generated daily plan."""
        if not self.daily_plan:
            return "No tasks were scheduled for today."
        lines = [
            f"Scheduled {task.task_name} ({task.duration} min)"
            + (" [required]" if task.is_required else "")
            for task in self.daily_plan
        ]
        return "\n".join(lines)
