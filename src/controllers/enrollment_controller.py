from typing import List, Optional

from src.models.enrollment import Enrollment
from src.services.enrollment_service import EnrollmentService


class EnrollmentController:
    """Coordinates enrollment management operations."""

    def __init__(
        self,
        enrollment_service: Optional[EnrollmentService] = None,
    ) -> None:
        self.enrollment_service = (
            enrollment_service or EnrollmentService()
        )

    def create_enrollment(
        self,
        student_id: int,
        course_id: int,
        term_id: int,
        status: str = "Enrolled",
    ) -> Enrollment:
        """Create a new enrollment."""

        return self.enrollment_service.create_enrollment(
            student_id=student_id,
            course_id=course_id,
            term_id=term_id,
            status=status,
        )

    def get_enrollment(
        self,
        enrollment_id: int,
    ) -> Optional[Enrollment]:
        """Get an enrollment by ID."""

        return self.enrollment_service.get_enrollment(
            enrollment_id
        )

    def get_student_enrollments(
        self,
        student_id: int,
    ) -> List[Enrollment]:
        """Get enrollments for a student."""

        return self.enrollment_service.get_student_enrollments(
            student_id
        )

    def get_course_enrollments(
        self,
        course_id: int,
    ) -> List[Enrollment]:
        """Get enrollments for a course."""

        return self.enrollment_service.get_course_enrollments(
            course_id
        )

    def get_term_enrollments(
        self,
        term_id: int,
    ) -> List[Enrollment]:
        """Get enrollments for an academic term."""

        return self.enrollment_service.get_term_enrollments(
            term_id
        )

    def get_all_enrollments(self) -> List[Enrollment]:
        """Return all enrollments."""

        return self.enrollment_service.get_all_enrollments()

    def update_enrollment(
        self,
        enrollment: Enrollment,
    ) -> Enrollment:
        """Update an existing enrollment."""

        return self.enrollment_service.update_enrollment(
            enrollment
        )

    def delete_enrollment(
        self,
        enrollment_id: int,
    ) -> bool:
        """Delete an enrollment."""

        return self.enrollment_service.delete_enrollment(
            enrollment_id
        )
