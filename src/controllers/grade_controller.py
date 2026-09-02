from typing import Optional

from src.models.grade import Grade
from src.services.grade_service import GradeService


class GradeController:
    """Controller for Grade Management operations."""

    def __init__(
        self,
        grade_service: Optional[GradeService] = None,
    ) -> None:
        self.grade_service = (
            grade_service or GradeService()
        )

    def create_grade(
        self,
        enrollment_id: int,
        assessment_score: float,
        exam_score: float,
        remarks: str = "",
    ) -> Grade:
        """Create a new grade."""

        return self.grade_service.create_grade(
            enrollment_id=enrollment_id,
            assessment_score=assessment_score,
            exam_score=exam_score,
            remarks=remarks,
        )

    def get_grade(
        self,
        grade_id: int,
    ) -> Optional[Grade]:
        """Get a grade by ID."""

        return self.grade_service.get_grade(grade_id)

    def get_grade_by_enrollment(
        self,
        enrollment_id: int,
    ) -> Optional[Grade]:
        """Get a grade by enrollment ID."""

        return self.grade_service.get_grade_by_enrollment(
            enrollment_id
        )

    def get_all_grades(self) -> list[Grade]:
        """Get all grades."""

        return self.grade_service.get_all_grades()

    def update_grade(
        self,
        grade: Grade,
    ) -> Grade:
        """Update an existing grade."""

        return self.grade_service.update_grade(grade)

    def delete_grade(
        self,
        grade_id: int,
    ) -> bool:
        """Delete a grade."""

        return self.grade_service.delete_grade(grade_id)
