from datetime import date
from typing import Optional

from src.database.connection import get_connection
from src.models.student import Student


class StudentRepository:
    """Handles database operations for students."""

    def create(self, student: Student) -> Student:
        """Create a student and return it with its database ID."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO students (
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    enrollment_year,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student.student_number,
                    student.first_name,
                    student.last_name,
                    student.date_of_birth.isoformat(),
                    student.gender,
                    student.program,
                    student.email,
                    student.phone,
                    date.today().year,
                    "Active" if student.is_active else "Inactive",
                ),
            )

            connection.commit()

            student.id = cursor.lastrowid

            return student

        finally:
            connection.close()

    def find_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by database ID."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                WHERE student_id = ?
                """,
                (student_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_student(row)

        finally:
            connection.close()

    def find_by_student_number(
        self,
        student_number: str,
    ) -> Optional[Student]:
        """Find a student by student number."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                WHERE student_number = ?
                """,
                (student_number,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_student(row)

        finally:
            connection.close()

    def find_by_email(
        self,
        email: str,
    ) -> Optional[Student]:
        """Find a student by email address."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                WHERE email = ?
                """,
                (email,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_student(row)

        finally:
            connection.close()

    def search(
        self,
        search_term: str = "",
        status: Optional[str] = None,
    ) -> list[Student]:
        """Search students and optionally filter by status."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            query = """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                WHERE 1 = 1
            """

            parameters = []

            if search_term.strip():
                search_pattern = f"%{search_term.strip()}%"

                query += """
                    AND (
                        student_number LIKE ?
                        OR first_name LIKE ?
                        OR last_name LIKE ?
                        OR email LIKE ?
                        OR program LIKE ?
                    )
                """

                parameters.extend(
                    [
                        search_pattern,
                        search_pattern,
                        search_pattern,
                        search_pattern,
                        search_pattern,
                    ]
                )

            if status in {
                "Active",
                "Inactive",
            }:
                query += """
                    AND status = ?
                """

                parameters.append(status)

            query += """
                ORDER BY last_name ASC, first_name ASC
            """

            cursor.execute(
                query,
                parameters,
            )

            rows = cursor.fetchall()

            return [
                self._row_to_student(row)
                for row in rows
            ]

        finally:
            connection.close()

    def count_all(self) -> int:
        """Return the total number of students."""

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM students
                """
            )
            result = cursor.fetchone()
            return int(result[0])
        finally:
            connection.close()

    def count_active(self) -> int:
        """Return the number of active students."""

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM students
                WHERE status = ?
                """,
                ("Active",),
            )
            result = cursor.fetchone()
            return int(result[0])
        finally:
            connection.close()

    def count_inactive(self) -> int:
        """Return the number of inactive students."""

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM students
                WHERE status = ?
                """,
                ("Inactive",),
            )
            result = cursor.fetchone()
            return int(result[0])
        finally:
            connection.close()

    def count_programs(self) -> int:
        """Return the number of distinct student programs."""

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(DISTINCT program)
                FROM students
                WHERE program IS NOT NULL
                  AND TRIM(program) != ''
                """
            )
            result = cursor.fetchone()
            return int(result[0])
        finally:
            connection.close()

    def find_recent(self, limit: int = 5) -> list[Student]:
        """Return the most recently registered students."""

        if limit <= 0:
            return []

        connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [
                self._row_to_student(row)
                for row in rows
            ]
        finally:
            connection.close()

    def find_all(self) -> list[Student]:
        """Return all students ordered by last name and first name."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    student_id,
                    student_number,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    program,
                    email,
                    phone,
                    status
                FROM students
                ORDER BY last_name ASC, first_name ASC
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_student(row)
                for row in rows
            ]

        finally:
            connection.close()

    def exists_by_student_number(self, student_number: str) -> bool:
        """Check whether a student number exists."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT 1
                FROM students
                WHERE student_number = ?
                LIMIT 1
                """,
                (student_number,),
            )

            return cursor.fetchone() is not None

        finally:
            connection.close()

    def exists_by_email(self, email: str) -> bool:
        """Check whether an email address exists."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT 1
                FROM students
                WHERE email = ?
                LIMIT 1
                """,
                (email,),
            )

            return cursor.fetchone() is not None

        finally:
            connection.close()

    def update(self, student: Student) -> Student:
        """Update an existing student."""

        if student.id is None:
            raise ValueError("Student ID is required for update.")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE students
                SET
                    student_number = ?,
                    first_name = ?,
                    last_name = ?,
                    date_of_birth = ?,
                    gender = ?,
                    program = ?,
                    email = ?,
                    phone = ?,
                    status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE student_id = ?
                """,
                (
                    student.student_number,
                    student.first_name,
                    student.last_name,
                    student.date_of_birth.isoformat(),
                    student.gender,
                    student.program,
                    student.email,
                    student.phone,
                    "Active" if student.is_active else "Inactive",
                    student.id,
                ),
            )

            connection.commit()

            return student

        finally:
            connection.close()

    def delete(self, student_id: int) -> bool:
        """Delete a student by ID."""

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM students
                WHERE student_id = ?
                """,
                (student_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    @staticmethod
    def _row_to_student(row) -> Student:
        """Convert a database row into a Student object."""

        return Student(
            id=row["student_id"],
            student_number=row["student_number"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            date_of_birth=date.fromisoformat(row["date_of_birth"]),
            gender=row["gender"],
            program=row["program"],
            email=row["email"],
            phone=row["phone"],
            is_active=row["status"] == "Active",
        )