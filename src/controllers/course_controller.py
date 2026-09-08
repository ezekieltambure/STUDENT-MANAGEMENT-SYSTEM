from typing import List, Optional

from src.models.course import Course
from src.services.course_service import CourseService


class CourseController:
    """Coordinates course management operations."""

    def __init__(
        self,
        course_service: Optional[CourseService] = None,
    ) -> None:
        self.course_service = (
            course_service or CourseService()
        )

    def create_course(
        self,
        course_code: str,
        course_name: str,
        credit_hours: int,
        department_id: int,
        description: str = "",
    ) -> Course:
        """Create a new course."""

        return self.course_service.create_course(
            course_code=course_code,
            course_name=course_name,
            credit_hours=credit_hours,
            department_id=department_id,
            description=description,
        )

    def get_course(
        self,
        course_id: int,
    ) -> Optional[Course]:
        """Get a course by ID."""

        return self.course_service.get_course(course_id)

    def get_course_by_code(
        self,
        course_code: str,
    ) -> Optional[Course]:
        """Get a course by code."""

        return self.course_service.get_course_by_code(
            course_code
        )

    def get_course_by_name(
        self,
        course_name: str,
    ) -> Optional[Course]:
        """Get a course by name."""

        return self.course_service.get_course_by_name(
            course_name
        )

    def get_all_courses(self) -> List[Course]:
        """Return all courses."""

        return self.course_service.get_all_courses()

    def search_courses(self, query: str) -> List[Course]:
        """Search courses by code, name, or description."""

        return self.course_service.search_courses(query)

    def update_course(self, course: Course) -> Course:
        """Update an existing course."""

        return self.course_service.update_course(course)

    def delete_course(self, course_id: int) -> bool:
        """Delete a course."""

        return self.course_service.delete_course(course_id)
