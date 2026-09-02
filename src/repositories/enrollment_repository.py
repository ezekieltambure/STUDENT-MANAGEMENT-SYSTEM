from typing import List, Optional

from src.database.connection import get_connection
from src.models.enrollment import Enrollment


class EnrollmentRepository:
    """Handles database operations for enrollments."""

    def create(self, enrollment: Enrollment) -> Enrollment:
        """Create a new enrollment."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO enrollments (
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status
                )
                VALUES (?, ?, ?, COALESCE(?, CURRENT_DATE), ?)
                """,
                (
                    enrollment.student_id,
                    enrollment.course_id,
                    enrollment.term_id,
                    (
                        enrollment.enrollment_date.isoformat()
                        if enrollment.enrollment_date
                        else None
                    ),
                    enrollment.status,
                ),
            )

            connection.commit()
            enrollment.id = cursor.lastrowid

            return enrollment

        finally:
            connection.close()

    def find_by_id(
        self,
        enrollment_id: int,
    ) -> Optional[Enrollment]:
        """Find an enrollment by ID."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    enrollment_id,
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status,
                    created_at
                FROM enrollments
                WHERE enrollment_id = ?
                """,
                (enrollment_id,),
            ).fetchone()

            if row is None:
                return None

            return self._row_to_enrollment(row)

        finally:
            connection.close()

    def find_by_student(
        self,
        student_id: int,
    ) -> List[Enrollment]:
        """Return all enrollments for a student."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    enrollment_id,
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status,
                    created_at
                FROM enrollments
                WHERE student_id = ?
                ORDER BY enrollment_date DESC, enrollment_id DESC
                """,
                (student_id,),
            ).fetchall()

            return [
                self._row_to_enrollment(row)
                for row in rows
            ]

        finally:
            connection.close()

    def find_by_course(
        self,
        course_id: int,
    ) -> List[Enrollment]:
        """Return all enrollments for a course."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    enrollment_id,
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status,
                    created_at
                FROM enrollments
                WHERE course_id = ?
                ORDER BY enrollment_date DESC, enrollment_id DESC
                """,
                (course_id,),
            ).fetchall()

            return [
                self._row_to_enrollment(row)
                for row in rows
            ]

        finally:
            connection.close()

    def find_by_term(
        self,
        term_id: int,
    ) -> List[Enrollment]:
        """Return all enrollments for an academic term."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    enrollment_id,
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status,
                    created_at
                FROM enrollments
                WHERE term_id = ?
                ORDER BY enrollment_date DESC, enrollment_id DESC
                """,
                (term_id,),
            ).fetchall()

            return [
                self._row_to_enrollment(row)
                for row in rows
            ]

        finally:
            connection.close()

    def list_all(self) -> List[Enrollment]:
        """Return all enrollments."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    enrollment_id,
                    student_id,
                    course_id,
                    term_id,
                    enrollment_date,
                    status,
                    created_at
                FROM enrollments
                ORDER BY enrollment_id DESC
                """
            ).fetchall()

            return [
                self._row_to_enrollment(row)
                for row in rows
            ]

        finally:
            connection.close()

    def update(self, enrollment: Enrollment) -> Enrollment:
        """Update an existing enrollment."""

        if enrollment.id is None:
            raise ValueError(
                "Enrollment ID is required for update."
            )

        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE enrollments
                SET
                    student_id = ?,
                    course_id = ?,
                    term_id = ?,
                    enrollment_date = ?,
                    status = ?
                WHERE enrollment_id = ?
                """,
                (
                    enrollment.student_id,
                    enrollment.course_id,
                    enrollment.term_id,
                    (
                        enrollment.enrollment_date.isoformat()
                        if enrollment.enrollment_date
                        else None
                    ),
                    enrollment.status,
                    enrollment.id,
                ),
            )

            connection.commit()

            return enrollment

        finally:
            connection.close()

    def delete(self, enrollment_id: int) -> bool:
        """Delete an enrollment by ID."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM enrollments
                WHERE enrollment_id = ?
                """,
                (enrollment_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def exists(
        self,
        student_id: int,
        course_id: int,
        term_id: int,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check whether a student is already enrolled."""

        connection = get_connection()

        try:
            if exclude_id is None:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM enrollments
                    WHERE student_id = ?
                      AND course_id = ?
                      AND term_id = ?
                    LIMIT 1
                    """,
                    (
                        student_id,
                        course_id,
                        term_id,
                    ),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM enrollments
                    WHERE student_id = ?
                      AND course_id = ?
                      AND term_id = ?
                      AND enrollment_id != ?
                    LIMIT 1
                    """,
                    (
                        student_id,
                        course_id,
                        term_id,
                        exclude_id,
                    ),
                ).fetchone()

            return row is not None

        finally:
            connection.close()

    @staticmethod
    def _row_to_enrollment(row) -> Enrollment:
        """Convert a database row into an Enrollment object."""

        from datetime import date, datetime

        enrollment_date = None

        if row["enrollment_date"]:
            try:
                enrollment_date = date.fromisoformat(
                    row["enrollment_date"]
                )
            except ValueError:
                enrollment_date = None

        created_at = None

        if row["created_at"]:
            try:
                created_at = datetime.fromisoformat(
                    row["created_at"]
                )
            except ValueError:
                created_at = None

        return Enrollment(
            id=row["enrollment_id"],
            student_id=row["student_id"],
            course_id=row["course_id"],
            term_id=row["term_id"],
            enrollment_date=enrollment_date,
            status=row["status"],
            created_at=created_at,
        )
