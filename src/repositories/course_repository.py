from typing import List, Optional

from src.database.connection import get_connection
from src.models.course import Course


class CourseRepository:
    """Handles database operations for courses."""

    def create(self, course: Course) -> Course:
        """Create a new course."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO courses (
                    course_code,
                    course_name,
                    description,
                    credit_hours,
                    department_id
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    course.course_code,
                    course.course_name,
                    course.description,
                    course.credit_hours,
                    course.department_id,
                ),
            )

            connection.commit()
            course.id = cursor.lastrowid

            return course

        finally:
            connection.close()

    def find_by_id(self, course_id: int) -> Optional[Course]:
        """Find a course by ID."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    course_id,
                    course_code,
                    course_name,
                    description,
                    credit_hours,
                    department_id
                FROM courses
                WHERE course_id = ?
                """,
                (course_id,),
            ).fetchone()

            if row is None:
                return None

            return self._row_to_course(row)

        finally:
            connection.close()

    def find_by_code(self, course_code: str) -> Optional[Course]:
        """Find a course by course code."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    course_id,
                    course_code,
                    course_name,
                    description,
                    credit_hours,
                    department_id
                FROM courses
                WHERE course_code = ?
                """,
                (course_code.strip().upper(),),
            ).fetchone()

            if row is None:
                return None

            return self._row_to_course(row)

        finally:
            connection.close()

    def find_by_name(self, course_name: str) -> Optional[Course]:
        """Find a course by name."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    course_id,
                    course_code,
                    course_name,
                    description,
                    credit_hours,
                    department_id
                FROM courses
                WHERE course_name = ?
                """,
                (course_name.strip(),),
            ).fetchone()

            if row is None:
                return None

            return self._row_to_course(row)

        finally:
            connection.close()

    def list_all(self) -> List[Course]:
        """Return all courses ordered by course code."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    course_id,
                    course_code,
                    course_name,
                    description,
                    credit_hours,
                    department_id
                FROM courses
                ORDER BY course_code
                """
            ).fetchall()

            return [self._row_to_course(row) for row in rows]

        finally:
            connection.close()

    def update(self, course: Course) -> Course:
        """Update an existing course."""

        if course.id is None:
            raise ValueError("Course ID is required for update.")

        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE courses
                SET
                    course_code = ?,
                    course_name = ?,
                    description = ?,
                    credit_hours = ?,
                    department_id = ?
                WHERE course_id = ?
                """,
                (
                    course.course_code,
                    course.course_name,
                    course.description,
                    course.credit_hours,
                    course.department_id,
                    course.id,
                ),
            )

            connection.commit()

            return course

        finally:
            connection.close()

    def delete(self, course_id: int) -> bool:
        """Delete a course by ID."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM courses
                WHERE course_id = ?
                """,
                (course_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def exists_by_code(
        self,
        course_code: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check whether a course code already exists."""

        connection = get_connection()

        try:
            if exclude_id is None:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM courses
                    WHERE course_code = ?
                    LIMIT 1
                    """,
                    (course_code.strip().upper(),),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM courses
                    WHERE course_code = ?
                      AND course_id != ?
                    LIMIT 1
                    """,
                    (
                        course_code.strip().upper(),
                        exclude_id,
                    ),
                ).fetchone()

            return row is not None

        finally:
            connection.close()

    def exists_by_name(
        self,
        course_name: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check whether a course name already exists."""

        connection = get_connection()

        try:
            if exclude_id is None:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM courses
                    WHERE course_name = ?
                    LIMIT 1
                    """,
                    (course_name.strip(),),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM courses
                    WHERE course_name = ?
                      AND course_id != ?
                    LIMIT 1
                    """,
                    (
                        course_name.strip(),
                        exclude_id,
                    ),
                ).fetchone()

            return row is not None

        finally:
            connection.close()

    @staticmethod
    def _row_to_course(row) -> Course:
        """Convert a database row into a Course object."""

        return Course(
            id=row["course_id"],
            course_code=row["course_code"],
            course_name=row["course_name"],
            description=row["description"] or "",
            credit_hours=row["credit_hours"],
            department_id=row["department_id"],
        )
