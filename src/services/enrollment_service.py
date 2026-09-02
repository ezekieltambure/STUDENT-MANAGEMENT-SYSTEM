from typing import List, Optional

from src.models.enrollment import Enrollment
from src.repositories.enrollment_repository import EnrollmentRepository
from src.repositories.student_repository import StudentRepository
from src.repositories.course_repository import CourseRepository


class EnrollmentService:
    """Provides business logic for enrollment management."""

    def __init__(
        self,
        enrollment_repository: Optional[EnrollmentRepository] = None,
        student_repository: Optional[StudentRepository] = None,
        course_repository: Optional[CourseRepository] = None,
    ) -> None:
        self.enrollment_repository = (
            enrollment_repository or EnrollmentRepository()
        )
        self.student_repository = (
            student_repository or StudentRepository()
        )
        self.course_repository = (
            course_repository or CourseRepository()
        )

    def _validate_references(
        self,
        student_id: int,
        course_id: int,
        term_id: int,
    ) -> None:
        """Validate related records exist."""

        if self.student_repository.find_by_id(student_id) is None:
            raise ValueError(
                f"Student ID {student_id} does not exist."
            )

        if self.course_repository.find_by_id(course_id) is None:
            raise ValueError(
                f"Course ID {course_id} does not exist."
            )

        if not isinstance(term_id, int) or term_id <= 0:
            raise ValueError(
                "Academic Term ID must be a valid positive integer."
            )

    def create_enrollment(
        self,
        student_id: int,
        course_id: int,
        term_id: int,
        status: str = "Enrolled",
    ) -> Enrollment:
        """Create a new enrollment."""

        self._validate_references(
            student_id,
            course_id,
            term_id,
        )

        if status not in Enrollment.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid enrollment status '{status}'."
            )

        if self.enrollment_repository.exists(
            student_id,
            course_id,
            term_id,
        ):
            raise ValueError(
                "This student is already enrolled in "
                "this course for this academic term."
            )

        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            term_id=term_id,
            status=status,
        )

        return self.enrollment_repository.create(
            enrollment
        )

    def get_enrollment(
        self,
        enrollment_id: int,
    ) -> Optional[Enrollment]:
        """Get an enrollment by ID."""

        return self.enrollment_repository.find_by_id(
            enrollment_id
        )

    def get_student_enrollments(
        self,
        student_id: int,
    ) -> List[Enrollment]:
        """Get all enrollments for a student."""

        return self.enrollment_repository.find_by_student(
            student_id
        )

    def get_course_enrollments(
        self,
        course_id: int,
    ) -> List[Enrollment]:
        """Get all enrollments for a course."""

        return self.enrollment_repository.find_by_course(
            course_id
        )

    def get_term_enrollments(
        self,
        term_id: int,
    ) -> List[Enrollment]:
        """Get all enrollments for a term."""

        return self.enrollment_repository.find_by_term(
            term_id
        )

    def get_all_enrollments(self) -> List[Enrollment]:
        """Return all enrollments."""

        return self.enrollment_repository.list_all()

    def update_enrollment(
        self,
        enrollment: Enrollment,
    ) -> Enrollment:
        """Update an existing enrollment."""

        if enrollment.id is None:
            raise ValueError(
                "Enrollment ID is required for update."
            )

        self._validate_references(
            enrollment.student_id,
            enrollment.course_id,
            enrollment.term_id,
        )

        if enrollment.status not in Enrollment.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid enrollment status "
                f"'{enrollment.status}'."
            )

        if self.enrollment_repository.exists(
            enrollment.student_id,
            enrollment.course_id,
            enrollment.term_id,
            exclude_id=enrollment.id,
        ):
            raise ValueError(
                "This student is already enrolled in "
                "this course for this academic term."
            )

        return self.enrollment_repository.update(
            enrollment
        )

    def delete_enrollment(
        self,
        enrollment_id: int,
    ) -> bool:
        """Delete an enrollment by ID."""

        if self.enrollment_repository.find_by_id(
            enrollment_id
        ) is None:
            return False

        return self.enrollment_repository.delete(
            enrollment_id
        )
