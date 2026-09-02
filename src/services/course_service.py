from typing import List, Optional

from src.models.course import Course
from src.repositories.course_repository import CourseRepository
from src.repositories.department_repository import DepartmentRepository


class CourseService:
    """Provides business logic for course management."""

    def __init__(
        self,
        course_repository: Optional[CourseRepository] = None,
        department_repository: Optional[DepartmentRepository] = None,
    ) -> None:
        self.course_repository = (
            course_repository or CourseRepository()
        )
        self.department_repository = (
            department_repository or DepartmentRepository()
        )

    def create_course(
        self,
        course_code: str,
        course_name: str,
        credit_hours: int,
        department_id: int,
        description: str = "",
    ) -> Course:
        """Create a new course after validation."""

        course_code = course_code.strip().upper()
        course_name = course_name.strip()

        if self.course_repository.exists_by_code(course_code):
            raise ValueError(
                f"Course code '{course_code}' already exists."
            )

        if self.course_repository.exists_by_name(course_name):
            raise ValueError(
                f"Course name '{course_name}' already exists."
            )

        department = self.department_repository.find_by_id(
            department_id
        )

        if department is None:
            raise ValueError(
                f"Department ID {department_id} does not exist."
            )

        course = Course(
            course_code=course_code,
            course_name=course_name,
            credit_hours=credit_hours,
            department_id=department_id,
            description=description,
        )

        return self.course_repository.create(course)

    def get_course(self, course_id: int) -> Optional[Course]:
        """Get a course by ID."""

        return self.course_repository.find_by_id(course_id)

    def get_course_by_code(
        self,
        course_code: str,
    ) -> Optional[Course]:
        """Get a course by course code."""

        return self.course_repository.find_by_code(
            course_code
        )

    def get_course_by_name(
        self,
        course_name: str,
    ) -> Optional[Course]:
        """Get a course by course name."""

        return self.course_repository.find_by_name(
            course_name
        )

    def get_all_courses(self) -> List[Course]:
        """Return all courses."""

        return self.course_repository.list_all()

    def update_course(self, course: Course) -> Course:
        """Update an existing course after validation."""

        if course.id is None:
            raise ValueError("Course ID is required for update.")

        if self.course_repository.exists_by_code(
            course.course_code,
            exclude_id=course.id,
        ):
            raise ValueError(
                f"Course code '{course.course_code}' already exists."
            )

        if self.course_repository.exists_by_name(
            course.course_name,
            exclude_id=course.id,
        ):
            raise ValueError(
                f"Course name '{course.course_name}' already exists."
            )

        department = self.department_repository.find_by_id(
            course.department_id
        )

        if department is None:
            raise ValueError(
                f"Department ID {course.department_id} does not exist."
            )

        return self.course_repository.update(course)

    def delete_course(self, course_id: int) -> bool:
        """Delete a course by ID."""

        if self.course_repository.find_by_id(course_id) is None:
            return False

        return self.course_repository.delete(course_id)
