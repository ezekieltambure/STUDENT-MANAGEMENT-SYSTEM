from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class AcademicTerm:
    """Represents an academic term."""

    term_name: str
    academic_year: int
    start_date: date
    end_date: date
    is_current: bool = False
    id: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate and normalize academic term data."""

        self.term_name = self.term_name.strip()

        if not self.term_name:
            raise ValueError("Term name cannot be empty.")

        if not isinstance(self.academic_year, int):
            raise TypeError("Academic year must be a whole number.")

        if self.academic_year < 2000:
            raise ValueError(
                "Academic year must be 2000 or later."
            )

        if isinstance(self.start_date, str):
            self.start_date = date.fromisoformat(self.start_date)

        if isinstance(self.end_date, str):
            self.end_date = date.fromisoformat(self.end_date)

        if not isinstance(self.start_date, date):
            raise TypeError("Start date must be a valid date.")

        if not isinstance(self.end_date, date):
            raise TypeError("End date must be a valid date.")

        if self.start_date >= self.end_date:
            raise ValueError(
                "Start date must be before end date."
            )

        if not isinstance(self.is_current, bool):
            raise TypeError("Current status must be True or False.")

    def __str__(self) -> str:
        """Return a readable academic term representation."""

        current_label = " (Current)" if self.is_current else ""

        return (
            f"{self.term_name} {self.academic_year}"
            f"{current_label}"
        )
