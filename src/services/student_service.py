from typing import Optional

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class StudentService:
    """Handles student-related business operations."""

    def __init__(
        self,
        student_repository: Optional[StudentRepository] = None,
    ) -> None:
        """Initialize the student service."""

        self.student_repository = (
            student_repository or StudentRepository()
        )

    def create_student(self, student: Student) -> Student:
        """Create a new student."""

        if self.student_repository.exists_by_student_number(
            student.student_number
        ):
            raise ValueError("Student number already exists.")

        return self.student_repository.create(student)

    def find_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by database ID."""

        return self.student_repository.find_by_id(student_id)

    def find_by_student_number(
        self,
        student_number: str,
    ) -> Optional[Student]:
        """Find a student by student number."""

        if not student_number.strip():
            return None

        return self.student_repository.find_by_student_number(
            student_number
        )

    def find_all(self) -> list[Student]:
        """Return all students."""

        return self.student_repository.find_all()

    def exists_by_student_number(self, student_number: str) -> bool:
        """Check whether a student number already exists."""

        if not student_number.strip():
            return False

        return self.student_repository.exists_by_student_number(
            student_number
        )

    def update_student(self, student: Student) -> Student:
        """Update an existing student."""

        if student.id is None:
            raise ValueError("Student ID is required for update.")

        existing_student = self.student_repository.find_by_student_number(
            student.student_number
        )

        if (
            existing_student is not None
            and existing_student.id != student.id
        ):
            raise ValueError("Student number already exists.")

        return self.student_repository.update(student)

    def delete_student(self, student_id: int) -> bool:
        """Delete a student by database ID."""

        return self.student_repository.delete(student_id)