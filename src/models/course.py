from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    """Represents a course in the Student Management System."""

    course_code: str
    course_name: str
    credit_hours: int
    department_id: int
    description: str = ""
    id: Optional[int] = None

    def __post_init__(self) -> None:
        self.course_code = self.course_code.strip().upper()
        self.course_name = self.course_name.strip()
        self.description = self.description.strip()

        if not self.course_code:
            raise ValueError("Course code cannot be empty.")

        if not self.course_name:
            raise ValueError("Course name cannot be empty.")

        if not isinstance(self.credit_hours, int):
            raise TypeError("Credit hours must be an integer.")

        if self.credit_hours <= 0:
            raise ValueError("Credit hours must be greater than zero.")

        if not isinstance(self.department_id, int):
            raise TypeError("Department ID must be an integer.")

        if self.department_id <= 0:
            raise ValueError("Department ID must be greater than zero.")

    def __str__(self) -> str:
        return (
            f"{self.course_code} - "
            f"{self.course_name} "
            f"({self.credit_hours} credits)"
        )
