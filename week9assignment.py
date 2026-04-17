from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    student_id: str
    assignments_done: int = 0
    scores: list[int] = field(default_factory=list)

    def submit(self, score: int):
        self.assignments_done += 1
        self.scores.append(score)

    def avg_score(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

@dataclass
class Course:
    course_name: str
    professor: str
    capacity: int
    students: list[Student] = field(default_factory=list)
    enrolled: int = field(init=False)

    def __post_init__(self):
        self._refresh()

    def _refresh(self):
        self.enrolled = len(self.students)

    def enroll(self, student: Student) -> bool:
        if self.enrolled >= self.capacity:
            return False
        self.students.append(student)
        self._refresh()
        return True

    def top_student(self) -> str:
        if not self.students:
            return "No data"
        best = max(self.students, key=lambda s: s.avg_score())
        return best.name if best.avg_score() > 0 else "No data"

    def course_stats(self) -> str:
        stats = [f"{self.course_name} (Prof. {self.professor}):"]
        for s in self.students:
            stats.append(
                f"  {s.name} - {s.assignments_done} assignments, avg {s.avg_score():.1f} pts"
            )
        stats.append(f"Enrolled: {self.enrolled}/{self.capacity}")
        return "\n".join(stats)


# --- Example Usage ---
s1 = Student("Liam", "S101")
s2 = Student("Nora", "S102")
s3 = Student("Omar", "S103")

s1.submit(72)
s1.submit(88)
s1.submit(91)
s2.submit(95)
s2.submit(89)
s3.submit(60)

c = Course("Data Structures", "Prof. Kim", 3)
print(c.enroll(s1))
print(c.enroll(s2))
print(c.enroll(s3))
print(c.enroll(Student("Priya", "S104")))
print(c.enrolled)
print(c.top_student())
print(c.course_stats())
