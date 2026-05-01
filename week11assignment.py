from dataclasses import dataclass, field

class WorkoutError(Exception):
    pass

@dataclass
class Exercise:
    code: str
    name: str
    duration: int
    calories: int
    status: str = field(default="PENDING", init=False)

    def __post_init__(self):
        if self.duration <= 0:
            raise WorkoutError(f"Duration not valid for {self.code}")

    @property
    def intensity(self):
        return round(self.calories / self.duration, 1)

    def __str__(self):
        return f"[{self.code}] {self.name} {self.duration}min {self.calories}cal ({self.status})"

    def __lt__(self, other):
        return self.calories < other.calories


class CalorieChecker:
    def __init__(self, exercises, max_cal):
        self.exercises = exercises
        self.max_cal = max_cal
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.exercises):
            raise StopIteration
        ex = self.exercises[self.index]
        self.index += 1

        ex.status = "APPROVED" if ex.calories <= self.max_cal else "EXCESSIVE"
        return ex


def workout_report(checker):
    ok, over = 0, 0
    for ex in checker:
        if ex.status == "APPROVED":
            ok += 1
        else:
            over += 1
        yield str(ex)
    yield f"Summary: {ok} approved, {over} excessive"


class GymSession:
    def __init__(self, name):
        self.name = name
        self.exercises = []

    def __enter__(self):
        print(f"=== Start: {self.name} ===")
        return self

    def add(self, exercise):
        self.exercises.append(exercise)

    def evaluate(self, max_cal):
        checker = CalorieChecker(self.exercises, max_cal)
        return workout_report(checker)

    def __exit__(self, exc_type, exc, tb):
        if exc_type is WorkoutError:
            print(f"!!! Error: {exc}")
        print(f"=== End: {self.name} ({len(self.exercises)} exercises) ===")
        return exc_type is WorkoutError


with GymSession("Cardio Plan") as gym:
    gym.add(Exercise("E01", "Running", 30, 250))
    gym.add(Exercise("E02", "Cycling", 45, 400))
    gym.add(Exercise("E03", "Swimming", 60, 650))

    for line in gym.evaluate(500):
        print(line)

    print(gym.exercises[0] < gym.exercises[1])

print()

with GymSession("Strength Plan") as gym:
    gym.add(Exercise("E04", "Deadlift", -10, 300))
