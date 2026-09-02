from typing import Optional

from src.models.grade import Grade
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.grade_repository import GradeRepository


class GradeService:
    """Business logic for grade management."""

    def __init__(
        self,
        grade_repository: Optional[GradeRepository] = None,
        enrollment_repository: Optional[EnrollmentRepository] = None,
    ) -> None:
        self.grade_repository = (
            grade_repository or GradeRepository()
        )
        self.enrollment_repository = (
            enrollment_repository or EnrollmentRepository()
        )

    def create_grade(
        self,
        enrollment_id: int,
        assessment_score: float,
        exam_score: float,
        remarks: str = "",
    ) -> Grade:
        """Create and calculate a new grade."""

        if not isinstance(enrollment_id, int):
            raise TypeError("Enrollment ID must be an integer.")

        if enrollment_id <= 0:
            raise ValueError(
                "Enrollment ID must be greater than zero."
            )

        enrollment = self.enrollment_repository.find_by_id(
            enrollment_id
        )

        if enrollment is None:
            raise ValueError(
                "Enrollment does not exist."
            )

        if self.grade_repository.exists_for_enrollment(
            enrollment_id
        ):
            raise ValueError(
                "A grade already exists for this enrollment."
            )

        grade = Grade(
            enrollment_id=enrollment_id,
            assessment_score=assessment_score,
            exam_score=exam_score,
            remarks=remarks,
        )

        grade.calculate_final_score()
        grade.calculate_grade()

        return self.grade_repository.create(grade)

    def get_grade(self, grade_id: int) -> Optional[Grade]:
        """Get a grade by ID."""

        if not isinstance(grade_id, int):
            raise TypeError("Grade ID must be an integer.")

        return self.grade_repository.find_by_id(grade_id)

    def get_grade_by_enrollment(
        self,
        enrollment_id: int,
    ) -> Optional[Grade]:
        """Get the grade associated with an enrollment."""

        if not isinstance(enrollment_id, int):
            raise TypeError(
                "Enrollment ID must be an integer."
            )

        return self.grade_repository.find_by_enrollment(
            enrollment_id
        )

    def get_all_grades(self) -> list[Grade]:
        """Return all grades."""

        return self.grade_repository.list_all()

    def update_grade(
        self,
        grade: Grade,
    ) -> Grade:
        """Update and recalculate an existing grade."""

        if grade.id is None:
            raise ValueError(
                "Grade ID is required for update."
            )

        enrollment = self.enrollment_repository.find_by_id(
            grade.enrollment_id
        )

        if enrollment is None:
            raise ValueError(
                "Enrollment does not exist."
            )

        if self.grade_repository.exists_for_enrollment(
            grade.enrollment_id,
            exclude_id=grade.id,
        ):
            raise ValueError(
                "A grade already exists for this enrollment."
            )

        grade.calculate_final_score()
        grade.calculate_grade()

        return self.grade_repository.update(grade)

    def delete_grade(self, grade_id: int) -> bool:
        """Delete a grade."""

        if not isinstance(grade_id, int):
            raise TypeError("Grade ID must be an integer.")

        if grade_id <= 0:
            raise ValueError(
                "Grade ID must be greater than zero."
            )

        return self.grade_repository.delete(grade_id)
