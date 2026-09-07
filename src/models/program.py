from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Program:
    """Represents an academic program."""

    program_code: str
    program_name: str
    qualification: str
    duration_years: int
    department_id: int
    description: str = ""
    status: str = "Active"
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate and normalize program data."""

        self.program_code = self.program_code.strip().upper()
        self.program_name = self.program_name.strip()
        self.qualification = self.qualification.strip()
        self.description = self.description.strip()
        self.status = self.status.strip().title()

        if not self.program_code:
            raise ValueError("Program code cannot be empty.")

        if not self.program_name:
            raise ValueError("Program name cannot be empty.")

        if not self.qualification:
            raise ValueError("Qualification cannot be empty.")

        if not isinstance(self.duration_years, int):
            raise TypeError("Duration must be a whole number of years.")

        if self.duration_years <= 0:
            raise ValueError("Duration must be greater than zero.")

        if not isinstance(self.department_id, int):
            raise TypeError("Department ID must be an integer.")

        if self.department_id <= 0:
            raise ValueError("Department ID must be greater than zero.")

        if self.status not in {"Active", "Inactive"}:
            raise ValueError("Status must be either Active or Inactive.")

    def __str__(self) -> str:
        return f"{self.program_code} - {self.program_name}"
