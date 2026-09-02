from datetime import datetime
from typing import Optional

from src.database.connection import get_connection
from src.models.grade import Grade


class GradeRepository:
    """Repository for Grade database operations."""

    def create(self, grade: Grade) -> Grade:
        """Create a new grade record."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO grades (
                    enrollment_id,
                    assessment_score,
                    exam_score,
                    final_score,
                    grade_letter,
                    grade_point,
                    remarks
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    grade.enrollment_id,
                    grade.assessment_score,
                    grade.exam_score,
                    grade.final_score,
                    grade.grade_letter,
                    grade.grade_point,
                    grade.remarks,
                ),
            )

            connection.commit()

            grade.id = cursor.lastrowid

            return grade

        finally:
            connection.close()

    def find_by_id(self, grade_id: int) -> Optional[Grade]:
        """Find a grade by its ID."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    grade_id,
                    enrollment_id,
                    assessment_score,
                    exam_score,
                    final_score,
                    grade_letter,
                    grade_point,
                    remarks,
                    graded_at
                FROM grades
                WHERE grade_id = ?
                """,
                (grade_id,),
            ).fetchone()

            return self._row_to_grade(row)

        finally:
            connection.close()

    def find_by_enrollment(
        self,
        enrollment_id: int,
    ) -> Optional[Grade]:
        """Find the grade for an enrollment."""

        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    grade_id,
                    enrollment_id,
                    assessment_score,
                    exam_score,
                    final_score,
                    grade_letter,
                    grade_point,
                    remarks,
                    graded_at
                FROM grades
                WHERE enrollment_id = ?
                """,
                (enrollment_id,),
            ).fetchone()

            return self._row_to_grade(row)

        finally:
            connection.close()

    def list_all(self) -> list[Grade]:
        """Return all grades."""

        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    grade_id,
                    enrollment_id,
                    assessment_score,
                    exam_score,
                    final_score,
                    grade_letter,
                    grade_point,
                    remarks,
                    graded_at
                FROM grades
                ORDER BY grade_id
                """
            ).fetchall()

            return [
                self._row_to_grade(row)
                for row in rows
            ]

        finally:
            connection.close()

    def update(self, grade: Grade) -> Grade:
        """Update an existing grade."""

        if grade.id is None:
            raise ValueError("Grade ID is required for update.")

        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE grades
                SET
                    enrollment_id = ?,
                    assessment_score = ?,
                    exam_score = ?,
                    final_score = ?,
                    grade_letter = ?,
                    grade_point = ?,
                    remarks = ?
                WHERE grade_id = ?
                """,
                (
                    grade.enrollment_id,
                    grade.assessment_score,
                    grade.exam_score,
                    grade.final_score,
                    grade.grade_letter,
                    grade.grade_point,
                    grade.remarks,
                    grade.id,
                ),
            )

            connection.commit()

            return grade

        finally:
            connection.close()

    def delete(self, grade_id: int) -> bool:
        """Delete a grade by ID."""

        connection = get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM grades
                WHERE grade_id = ?
                """,
                (grade_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()

    def exists_for_enrollment(
        self,
        enrollment_id: int,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """Check whether a grade already exists for an enrollment."""

        connection = get_connection()

        try:
            if exclude_id is None:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM grades
                    WHERE enrollment_id = ?
                    LIMIT 1
                    """,
                    (enrollment_id,),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT 1
                    FROM grades
                    WHERE enrollment_id = ?
                      AND grade_id != ?
                    LIMIT 1
                    """,
                    (enrollment_id, exclude_id),
                ).fetchone()

            return row is not None

        finally:
            connection.close()

    @staticmethod
    def _row_to_grade(row) -> Optional[Grade]:
        """Convert a database row into a Grade object."""

        if row is None:
            return None

        graded_at = None

        if row["graded_at"]:
            try:
                graded_at = datetime.fromisoformat(
                    row["graded_at"]
                )
            except ValueError:
                graded_at = None

        return Grade(
            id=row["grade_id"],
            enrollment_id=row["enrollment_id"],
            assessment_score=row["assessment_score"],
            exam_score=row["exam_score"],
            final_score=row["final_score"],
            grade_letter=row["grade_letter"] or "",
            grade_point=row["grade_point"],
            remarks=row["remarks"] or "",
            graded_at=graded_at,
        )
