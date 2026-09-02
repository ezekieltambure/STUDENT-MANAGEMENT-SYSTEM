from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Report:
    """Represents a generated system report."""

    report_type: str
    title: str
    data: list[dict[str, Any]]
    generated_at: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate report information."""

        if not self.report_type.strip():
            raise ValueError("Report type cannot be empty.")

        if not self.title.strip():
            raise ValueError("Report title cannot be empty.")

        if not isinstance(self.data, list):
            raise TypeError("Report data must be a list.")

        if self.generated_at is not None and not isinstance(
            self.generated_at, str
        ):
            raise TypeError("Generated time must be a string.")

    @property
    def row_count(self) -> int:
        """Return the number of rows in the report."""

        return len(self.data)

    def is_empty(self) -> bool:
        """Return True when the report contains no data."""

        return not self.data

    def __str__(self) -> str:
        """Return a readable report description."""

        return f"{self.title} ({self.row_count} records)"