from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Grade:
    """Represents a student's grade for an enrollment."""

    enrollment_id: int
    assessment_score: float
    exam_score: float
    final_score: Optional[float] = None
    grade_letter: str = ""
    grade_point: Optional[float] = None
    remarks: str = ""
    id: Optional[int] = None
    graded_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not isinstance(self.enrollment_id, int):
            raise TypeError("Enrollment ID must be an integer.")

        if self.enrollment_id <= 0:
            raise ValueError("Enrollment ID must be greater than zero.")

        self.assessment_score = float(self.assessment_score)
        self.exam_score = float(self.exam_score)

        if not 0 <= self.assessment_score <= 100:
            raise ValueError(
                "Assessment score must be between 0 and 100."
            )

        if not 0 <= self.exam_score <= 100:
            raise ValueError(
                "Exam score must be between 0 and 100."
            )

        if self.final_score is not None:
            self.final_score = float(self.final_score)

            if not 0 <= self.final_score <= 100:
                raise ValueError(
                    "Final score must be between 0 and 100."
                )

        self.grade_letter = self.grade_letter.strip().upper()
        self.remarks = self.remarks.strip()

        if self.grade_point is not None:
            self.grade_point = float(self.grade_point)

    def calculate_final_score(self) -> float:
        """Calculate the final score from assessment and exam scores."""

        self.final_score = (
            self.assessment_score * 0.40
            + self.exam_score * 0.60
        )

        return round(self.final_score, 2)

    def calculate_grade(self) -> str:
        """Calculate the grade letter and grade point."""

        if self.final_score is None:
            self.calculate_final_score()

        if self.final_score >= 80:
            self.grade_letter = "A"
            self.grade_point = 4.0
        elif self.final_score >= 70:
            self.grade_letter = "B"
            self.grade_point = 3.0
        elif self.final_score >= 60:
            self.grade_letter = "C"
            self.grade_point = 2.0
        elif self.final_score >= 50:
            self.grade_letter = "D"
            self.grade_point = 1.0
        else:
            self.grade_letter = "F"
            self.grade_point = 0.0

        return self.grade_letter

    def __str__(self) -> str:
        return (
            f"Grade {self.id}: "
            f"{self.grade_letter} "
            f"({self.final_score})"
        )
