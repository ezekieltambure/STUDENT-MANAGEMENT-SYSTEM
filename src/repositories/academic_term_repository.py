import sqlite3
from datetime import date
from typing import List, Optional

from src.models.academic_term import AcademicTerm


class AcademicTermRepository:
    """Handles database operations for academic terms."""

    def __init__(
        self,
        db_path: str = "database/student_management.db",
    ) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        """Create and configure a database connection."""

        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create(self, term: AcademicTerm) -> AcademicTerm:
        """Create a new academic term."""

        query = """
            INSERT INTO academic_terms (
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            )
            VALUES (?, ?, ?, ?, ?)
        """

        with self._connect() as connection:
            cursor = connection.execute(
                query,
                (
                    term.term_name,
                    term.academic_year,
                    term.start_date.isoformat(),
                    term.end_date.isoformat(),
                    int(term.is_current),
                ),
            )

            term.id = cursor.lastrowid

        return term

    def find_by_id(
        self,
        term_id: int,
    ) -> Optional[AcademicTerm]:
        """Find an academic term by its ID."""

        query = """
            SELECT
                term_id,
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            FROM academic_terms
            WHERE term_id = ?
        """

        with self._connect() as connection:
            row = connection.execute(
                query,
                (term_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_term(row)

    def find_by_name_and_year(
        self,
        term_name: str,
        academic_year: int,
    ) -> Optional[AcademicTerm]:
        """Find a term using its name and academic year."""

        query = """
            SELECT
                term_id,
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            FROM academic_terms
            WHERE term_name = ?
              AND academic_year = ?
        """

        with self._connect() as connection:
            row = connection.execute(
                query,
                (
                    term_name.strip(),
                    academic_year,
                ),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_term(row)

    def list_all(self) -> List[AcademicTerm]:
        """Return all academic terms."""

        query = """
            SELECT
                term_id,
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            FROM academic_terms
            ORDER BY academic_year DESC, start_date ASC
        """

        with self._connect() as connection:
            rows = connection.execute(query).fetchall()

        return [
            self._row_to_term(row)
            for row in rows
        ]

    def search(self, query: str) -> List[AcademicTerm]:
        """Search academic terms by name or academic year."""

        search_term = query.strip()

        if not search_term:
            return self.list_all()

        sql = """
            SELECT
                term_id,
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            FROM academic_terms
            WHERE term_name LIKE ?
               OR CAST(academic_year AS TEXT) LIKE ?
            ORDER BY academic_year DESC, start_date ASC
        """

        pattern = f"%{search_term}%"

        with self._connect() as connection:
            rows = connection.execute(
                sql,
                (
                    pattern,
                    pattern,
                ),
            ).fetchall()

        return [
            self._row_to_term(row)
            for row in rows
        ]

    def update(self, term: AcademicTerm) -> bool:
        """Update an existing academic term."""

        if term.id is None:
            raise ValueError(
                "Academic term ID is required for update."
            )

        query = """
            UPDATE academic_terms
            SET
                term_name = ?,
                academic_year = ?,
                start_date = ?,
                end_date = ?,
                is_current = ?
            WHERE term_id = ?
        """

        with self._connect() as connection:
            cursor = connection.execute(
                query,
                (
                    term.term_name,
                    term.academic_year,
                    term.start_date.isoformat(),
                    term.end_date.isoformat(),
                    int(term.is_current),
                    term.id,
                ),
            )

        return cursor.rowcount > 0

    def delete(self, term_id: int) -> bool:
        """Delete an academic term."""

        query = """
            DELETE FROM academic_terms
            WHERE term_id = ?
        """

        with self._connect() as connection:
            cursor = connection.execute(
                query,
                (term_id,),
            )

        return cursor.rowcount > 0

    def set_current(self, term_id: int) -> bool:
        """Set one academic term as current."""

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE academic_terms
                SET is_current = 0
                WHERE is_current = 1
                """
            )

            cursor = connection.execute(
                """
                UPDATE academic_terms
                SET is_current = 1
                WHERE term_id = ?
                """,
                (term_id,),
            )

        return cursor.rowcount > 0

    def get_current(self) -> Optional[AcademicTerm]:
        """Return the currently active academic term."""

        query = """
            SELECT
                term_id,
                term_name,
                academic_year,
                start_date,
                end_date,
                is_current
            FROM academic_terms
            WHERE is_current = 1
            LIMIT 1
        """

        with self._connect() as connection:
            row = connection.execute(query).fetchone()

        if row is None:
            return None

        return self._row_to_term(row)

    def exists_by_name_and_year(
        self,
        term_name: str,
        academic_year: int,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check whether a term name/year combination already exists."""

        if exclude_id is None:
            query = """
                SELECT 1
                FROM academic_terms
                WHERE term_name = ?
                  AND academic_year = ?
                LIMIT 1
            """

            parameters = (
                term_name.strip(),
                academic_year,
            )
        else:
            query = """
                SELECT 1
                FROM academic_terms
                WHERE term_name = ?
                  AND academic_year = ?
                  AND term_id != ?
                LIMIT 1
            """

            parameters = (
                term_name.strip(),
                academic_year,
                exclude_id,
            )

        with self._connect() as connection:
            row = connection.execute(
                query,
                parameters,
            ).fetchone()

        return row is not None

    @staticmethod
    def _row_to_term(
        row: sqlite3.Row,
    ) -> AcademicTerm:
        """Convert a database row into an AcademicTerm."""

        return AcademicTerm(
            id=row["term_id"],
            term_name=row["term_name"],
            academic_year=row["academic_year"],
            start_date=date.fromisoformat(row["start_date"]),
            end_date=date.fromisoformat(row["end_date"]),
            is_current=bool(row["is_current"]),
        )
