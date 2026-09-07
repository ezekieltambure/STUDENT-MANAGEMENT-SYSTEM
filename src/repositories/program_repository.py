from typing import List, Optional

from src.database.connection import get_connection
from src.models.program import Program


class ProgramRepository:
    """Repository for academic program database operations."""

    def create(self, program: Program) -> Program:
        """Create a new academic program."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO programs (
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    program.program_code,
                    program.program_name,
                    program.qualification,
                    program.duration_years,
                    program.department_id,
                    program.description,
                    program.status,
                ),
            )

            connection.commit()
            program.id = cursor.lastrowid

            return program

        finally:
            connection.close()

    def find_by_id(self, program_id: int) -> Optional[Program]:
        """Find a program by its database ID."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    program_id,
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status,
                    created_at
                FROM programs
                WHERE program_id = ?
                """,
                (program_id,),
            ).fetchone()

            return self._row_to_program(row)

        finally:
            connection.close()

    def find_by_code(self, program_code: str) -> Optional[Program]:
        """Find a program by its unique code."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    program_id,
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status,
                    created_at
                FROM programs
                WHERE program_code = ?
                """,
                (program_code.strip().upper(),),
            ).fetchone()

            return self._row_to_program(row)

        finally:
            connection.close()

    def find_by_name(self, program_name: str) -> Optional[Program]:
        """Find a program by its unique name."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    program_id,
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status,
                    created_at
                FROM programs
                WHERE program_name = ?
                """,
                (program_name.strip(),),
            ).fetchone()

            return self._row_to_program(row)

        finally:
            connection.close()

    def list_all(self) -> List[Program]:
        """Return all programs ordered by program name."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    program_id,
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status,
                    created_at
                FROM programs
                ORDER BY program_name ASC
                """
            ).fetchall()

            return [self._row_to_program(row) for row in rows]

        finally:
            connection.close()

    def search(self, search_term: str = "") -> List[Program]:
        """Search programs by code, name, qualification, or description."""

        connection = get_connection()

        try:
            term = f"%{search_term.strip()}%"

            rows = connection.execute(
                """
                SELECT
                    program_id,
                    program_code,
                    program_name,
                    qualification,
                    duration_years,
                    department_id,
                    description,
                    status,
                    created_at
                FROM programs
                WHERE
                    program_code LIKE ?
                    OR program_name LIKE ?
                    OR qualification LIKE ?
                    OR description LIKE ?
                ORDER BY program_name ASC
                """,
                (term, term, term, term),
            ).fetchall()

            return [self._row_to_program(row) for row in rows]

        finally:
            connection.close()

    def update(self, program: Program) -> bool:
        """Update an existing academic program."""

        if program.id is None:
            raise ValueError("Program ID is required for update.")

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE programs
                SET
                    program_code = ?,
                    program_name = ?,
                    qualification = ?,
                    duration_years = ?,
                    department_id = ?,
                    description = ?,
                    status = ?
                WHERE program_id = ?
                """,
                (
                    program.program_code,
                    program.program_name,
                    program.qualification,
                    program.duration_years,
                    program.department_id,
                    program.description,
                    program.status,
                    program.id,
                ),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def delete(self, program_id: int) -> bool:
        """Delete a program by ID."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM programs
                WHERE program_id = ?
                """,
                (program_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def exists_by_code(self, program_code: str) -> bool:
        """Check whether a program code already exists."""

        return self.find_by_code(program_code) is not None

    def exists_by_name(self, program_name: str) -> bool:
        """Check whether a program name already exists."""

        return self.find_by_name(program_name) is not None

    def _row_to_program(self, row) -> Optional[Program]:
        """Convert a database row into a Program object."""

        if row is None:
            return None

        return Program(
            id=row["program_id"],
            program_code=row["program_code"],
            program_name=row["program_name"],
            qualification=row["qualification"],
            duration_years=row["duration_years"],
            department_id=row["department_id"],
            description=row["description"] or "",
            status=row["status"],
            created_at=row["created_at"],
        )
