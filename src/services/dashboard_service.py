from typing import Optional

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


class DashboardService:
    """Provides data required by the system dashboard."""

    def __init__(
        self,
        student_repository: Optional[StudentRepository] = None,
    ) -> None:
        """Initialize the dashboard service."""

        self.student_repository = (
            student_repository or StudentRepository()
        )

    def get_total_students(self) -> int:
        """Return the total number of students."""

        return self.student_repository.count_all()

    def get_active_students(self) -> int:
        """Return the number of active students."""

        return self.student_repository.count_active()

    def get_inactive_students(self) -> int:
        """Return the number of inactive students."""

        return self.student_repository.count_inactive()

    def get_program_count(self) -> int:
        """Return the number of distinct student programs."""

        return self.student_repository.count_programs()

    def get_recent_students(
        self,
        limit: int = 5,
    ) -> list[Student]:
        """Return recently registered students."""

        return self.student_repository.find_recent(limit)
