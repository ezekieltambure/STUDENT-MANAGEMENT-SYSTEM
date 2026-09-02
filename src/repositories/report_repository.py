import sqlite3
from typing import Any

from src.config import DATABASE_PATH


class ReportRepository:
    """Repository for generating database-backed reports."""

    def __init__(self, database_path: str = DATABASE_PATH) -> None:
        """Initialize the report repository."""

        self.database_path = database_path

    def _connect(self) -> sqlite3.Connection:
        """Create a database connection."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _fetch_report(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        """Execute a report query and return dictionary rows."""

        with self._connect() as connection:
            cursor = connection.execute(query, parameters)
            return [dict(row) for row in cursor.fetchall()]

    def student_summary(self) -> list[dict[str, Any]]:
        """Return a summary of students by status."""

        query = """
            SELECT
                status,
                COUNT(*) AS student_count
            FROM students
            GROUP BY status
            ORDER BY status
        """

        return self._fetch_report(query)

    def students_by_department(self) -> list[dict[str, Any]]:
        """Return student counts grouped by department."""

        query = """
            SELECT
                COALESCE(d.department_code, 'UNASSIGNED')
                    AS department_code,
                COALESCE(d.department_name, 'Unassigned')
                    AS department_name,
                COUNT(s.student_id) AS student_count
            FROM students s
            LEFT JOIN departments d
                ON s.department_id = d.department_id
            GROUP BY
                d.department_id,
                d.department_code,
                d.department_name
            ORDER BY department_name
        """

        return self._fetch_report(query)

    def course_summary(self) -> list[dict[str, Any]]:
        """Return a summary of courses by department."""

        query = """
            SELECT
                d.department_code,
                d.department_name,
                COUNT(c.course_id) AS course_count
            FROM departments d
            LEFT JOIN courses c
                ON d.department_id = c.department_id
            GROUP BY
                d.department_id,
                d.department_code,
                d.department_name
            ORDER BY d.department_name
        """

        return self._fetch_report(query)

    def enrollment_summary(self) -> list[dict[str, Any]]:
        """Return enrollment counts by status."""

        query = """
            SELECT
                status,
                COUNT(*) AS enrollment_count
            FROM enrollments
            GROUP BY status
            ORDER BY status
        """

        return self._fetch_report(query)

    def enrollment_by_term(self) -> list[dict[str, Any]]:
        """Return enrollment counts grouped by academic term."""

        query = """
            SELECT
                t.term_name,
                t.academic_year,
                COUNT(e.enrollment_id) AS enrollment_count
            FROM academic_terms t
            LEFT JOIN enrollments e
                ON t.term_id = e.term_id
            GROUP BY
                t.term_id,
                t.term_name,
                t.academic_year
            ORDER BY
                t.academic_year DESC,
                t.term_name
        """

        return self._fetch_report(query)

    def grade_summary(self) -> list[dict[str, Any]]:
        """Return grade counts grouped by grade letter."""

        query = """
            SELECT
                grade_letter,
                COUNT(*) AS grade_count,
                ROUND(AVG(final_score), 2) AS average_score
            FROM grades
            GROUP BY grade_letter
            ORDER BY grade_letter
        """

        return self._fetch_report(query)

    def student_performance(self) -> list[dict[str, Any]]:
        """Return student academic performance details."""

        query = """
            SELECT
                s.student_number,
                s.first_name,
                s.last_name,
                c.course_code,
                c.course_name,
                t.term_name,
                t.academic_year,
                g.final_score,
                g.grade_letter,
                g.grade_point
            FROM grades g
            INNER JOIN enrollments e
                ON g.enrollment_id = e.enrollment_id
            INNER JOIN students s
                ON e.student_id = s.student_id
            INNER JOIN courses c
                ON e.course_id = c.course_id
            INNER JOIN academic_terms t
                ON e.term_id = t.term_id
            ORDER BY
                s.last_name,
                s.first_name,
                c.course_code
        """

        return self._fetch_report(query)

    def system_overview(self) -> list[dict[str, Any]]:
        """Return high-level system statistics."""

        query = """
            SELECT 'Students' AS category, COUNT(*) AS total
            FROM students

            UNION ALL

            SELECT 'Departments', COUNT(*)
            FROM departments

            UNION ALL

            SELECT 'Courses', COUNT(*)
            FROM courses

            UNION ALL

            SELECT 'Enrollments', COUNT(*)
            FROM enrollments

            UNION ALL

            SELECT 'Grades', COUNT(*)
            FROM grades

            UNION ALL

            SELECT 'Users', COUNT(*)
            FROM users
        """

        return self._fetch_report(query)