from typing import Optional

from src.models.student import Student
from src.services.student_service import StudentService


class StudentController:
    """Coordinates student operations between the view and service."""

    def __init__(
        self,
        student_service: Optional[StudentService] = None,
    ) -> None:
        """Initialize the student controller."""

        self.student_service = (
            student_service or StudentService()
        )

    def create_student(self, student: Student) -> Student:
        """Create a new student."""

        return self.student_service.create_student(student)

    def find_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by database ID."""

        return self.student_service.find_by_id(student_id)

    def find_by_student_number(
        self,
        student_number: str,
    ) -> Optional[Student]:
        """Find a student by student number."""

        return self.student_service.find_by_student_number(
            student_number
        )

    def search_students(
        self,
        search_term: str = "",
        status: Optional[str] = None,
    ) -> list[Student]:
        """Search students and optionally filter by status."""

        return self.student_service.search_students(
            search_term=search_term,
            status=status,
        )

    def find_all(self) -> list[Student]:
        """Return all students."""

        return self.student_service.find_all()

    def exists_by_student_number(
        self,
        student_number: str,
    ) -> bool:
        """Check whether a student number exists."""

        return self.student_service.exists_by_student_number(
            student_number
        )

    def update_student(self, student: Student) -> Student:
        """Update an existing student."""

        return self.student_service.update_student(student)

    def deactivate_student(self, student_id: int) -> Student:
        """Deactivate a student."""

        return self.student_service.deactivate_student(
            student_id
        )

    def activate_student(self, student_id: int) -> Student:
        """Activate a student."""

        return self.student_service.activate_student(
            student_id
        )

    def delete_student(self, student_id: int) -> bool:
        """Delete a student by database ID."""

        return self.student_service.delete_student(
            student_id
        )