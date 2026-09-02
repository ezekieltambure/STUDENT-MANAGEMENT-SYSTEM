from typing import List, Optional

from src.database.connection import get_connection
from src.models.department import Department


class DepartmentRepository:
    """Handles database operations for departments."""

    def create(self, department: Department) -> Department:
        """Create a department and return it with its database ID."""

        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO departments (
                    department_code,
                    department_name,
                    description
                )
                VALUES (?, ?, ?)
                """,
                (
                    department.department_code,
                    department.department_name,
                    department.description,
                ),
            )

            department.id = cursor.lastrowid
            connection.commit()

        return department

    def find_by_id(
        self,
        department_id: int,
    ) -> Optional[Department]:
        """Find a department by ID."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    department_id,
                    department_code,
                    department_name,
                    description,
                    created_at
                FROM departments
                WHERE department_id = ?
                """,
                (department_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_department(row)

    def find_by_code(
        self,
        department_code: str,
    ) -> Optional[Department]:
        """Find a department by department code."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    department_id,
                    department_code,
                    department_name,
                    description,
                    created_at
                FROM departments
                WHERE department_code = ?
                """,
                (department_code,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_department(row)

    def find_by_name(
        self,
        department_name: str,
    ) -> Optional[Department]:
        """Find a department by department name."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    department_id,
                    department_code,
                    department_name,
                    description,
                    created_at
                FROM departments
                WHERE department_name = ?
                """,
                (department_name,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_department(row)

    def list_all(self) -> List[Department]:
        """Return all departments ordered by department name."""

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    department_id,
                    department_code,
                    department_name,
                    description,
                    created_at
                FROM departments
                ORDER BY department_name
                """
            ).fetchall()

        return [
            self._row_to_department(row)
            for row in rows
        ]

    def update(self, department: Department) -> Department:
        """Update an existing department."""

        if department.id is None:
            raise ValueError(
                "Department ID is required for update."
            )

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE departments
                SET
                    department_code = ?,
                    department_name = ?,
                    description = ?
                WHERE department_id = ?
                """,
                (
                    department.department_code,
                    department.department_name,
                    department.description,
                    department.id,
                ),
            )

            connection.commit()

        return department

    def delete(self, department_id: int) -> bool:
        """Delete a department by ID."""

        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM departments
                WHERE department_id = ?
                """,
                (department_id,),
            )

            connection.commit()

        return cursor.rowcount > 0

    def exists_by_code(self, department_code: str) -> bool:
        """Check whether a department code already exists."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM departments
                WHERE department_code = ?
                LIMIT 1
                """,
                (department_code,),
            ).fetchone()

        return row is not None

    def exists_by_name(self, department_name: str) -> bool:
        """Check whether a department name already exists."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM departments
                WHERE department_name = ?
                LIMIT 1
                """,
                (department_name,),
            ).fetchone()

        return row is not None

    @staticmethod
    def _row_to_department(row) -> Department:
        """Convert a database row into a Department object."""

        return Department(
            id=row["department_id"],
            department_code=row["department_code"],
            department_name=row["department_name"],
            description=row["description"] or "",
            created_at=row["created_at"],
        )
