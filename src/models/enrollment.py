from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Enrollment:
    """Represents a student course enrollment."""

    student_id: int
    course_id: int
    term_id: int
    enrollment_date: Optional[date] = None
    status: str = "Enrolled"
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    ALLOWED_STATUSES = {
        "Enrolled",
        "Completed",
        "Dropped",
        "Withdrawn",
    }

    def __post_init__(self) -> None:
        if not isinstance(self.student_id, int):
            raise TypeError("Student ID must be an integer.")

        if self.student_id <= 0:
            raise ValueError("Student ID must be greater than zero.")

        if not isinstance(self.course_id, int):
            raise TypeError("Course ID must be an integer.")

        if self.course_id <= 0:
            raise ValueError("Course ID must be greater than zero.")

        if not isinstance(self.term_id, int):
            raise TypeError("Term ID must be an integer.")

        if self.term_id <= 0:
            raise ValueError("Term ID must be greater than zero.")

        if self.enrollment_date is not None:
            if not isinstance(self.enrollment_date, date):
                raise TypeError(
                    "Enrollment date must be a date."
                )

        if self.status not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid enrollment status '{self.status}'. "
                f"Allowed statuses: "
                f"{', '.join(sorted(self.ALLOWED_STATUSES))}."
            )

    def complete(self) -> None:
        """Mark the enrollment as completed."""

        self.status = "Completed"

    def drop(self) -> None:
        """Mark the enrollment as dropped."""

        self.status = "Dropped"

    def withdraw(self) -> None:
        """Mark the enrollment as withdrawn."""

        self.status = "Withdrawn"

    def __str__(self) -> str:
        return (
            f"Enrollment {self.id}: "
            f"Student {self.student_id}, "
            f"Course {self.course_id}, "
            f"Term {self.term_id} "
            f"({self.status})"
        )
