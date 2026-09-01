from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Student:
    """Represents a student in the Student Management System."""

    student_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    program: str
    email: str
    phone: str
    id: Optional[int] = None
    is_active: bool = True

    def __post_init__(self) -> None:
        """Validate student data after initialization."""

        if not self.student_number.strip():
            raise ValueError("Student number cannot be empty.")

        if not self.first_name.strip():
            raise ValueError("First name cannot be empty.")

        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty.")

        if not isinstance(self.date_of_birth, date):
            raise TypeError("Date of birth must be a date.")

        if self.gender not in {"Male", "Female", "Other"}:
            raise ValueError("Gender must be Male, Female, or Other.")

        if not self.program.strip():
            raise ValueError("Program cannot be empty.")

        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email address.")

        if not self.phone.strip():
            raise ValueError("Phone number cannot be empty.")

    @property
    def full_name(self) -> str:
        """Return the student's full name."""

        return f"{self.first_name} {self.last_name}"

    def deactivate(self) -> None:
        """Deactivate the student."""

        self.is_active = False

    def activate(self) -> None:
        """Activate the student."""

        self.is_active = True

    def __str__(self) -> str:
        """Return a readable student representation."""

        return f"{self.student_number} - {self.full_name}"