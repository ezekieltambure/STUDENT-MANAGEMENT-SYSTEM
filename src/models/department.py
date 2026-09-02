from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Department:
    """Represents an academic department."""

    department_code: str
    department_name: str
    description: str = ""
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate department data."""

        self.department_code = self.department_code.strip()
        self.department_name = self.department_name.strip()
        self.description = self.description.strip()

        if not self.department_code:
            raise ValueError("Department code cannot be empty.")

        if not self.department_name:
            raise ValueError("Department name cannot be empty.")

    def __str__(self) -> str:
        """Return a readable department representation."""

        return (
            f"{self.department_code} - "
            f"{self.department_name}"
        )
