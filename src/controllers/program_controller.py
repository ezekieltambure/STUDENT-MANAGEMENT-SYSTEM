from typing import List, Optional

from src.models.program import Program
from src.services.program_service import ProgramService


class ProgramController:
    """Controller for academic program operations."""

    def __init__(
        self,
        program_service: Optional[ProgramService] = None,
    ) -> None:
        self.program_service = program_service or ProgramService()

    def create_program(
        self,
        program_code: str,
        program_name: str,
        qualification: str,
        duration_years: int,
        department_id: int,
        description: str = "",
        status: str = "Active",
    ) -> Program:
        """Create an academic program."""

        return self.program_service.create_program(
            program_code=program_code,
            program_name=program_name,
            qualification=qualification,
            duration_years=duration_years,
            department_id=department_id,
            description=description,
            status=status,
        )

    def get_program(self, program_id: int) -> Optional[Program]:
        """Get a program by ID."""

        return self.program_service.get_program(program_id)

    def get_program_by_code(
        self,
        program_code: str,
    ) -> Optional[Program]:
        """Get a program by code."""

        return self.program_service.get_program_by_code(program_code)

    def get_program_by_name(
        self,
        program_name: str,
    ) -> Optional[Program]:
        """Get a program by name."""

        return self.program_service.get_program_by_name(program_name)

    def get_all_programs(self) -> List[Program]:
        """Get all academic programs."""

        return self.program_service.get_all_programs()

    def search_programs(
        self,
        search_term: str = "",
    ) -> List[Program]:
        """Search academic programs."""

        return self.program_service.search_programs(search_term)

    def update_program(self, program: Program) -> bool:
        """Update an academic program."""

        return self.program_service.update_program(program)

    def delete_program(self, program_id: int) -> bool:
        """Delete an academic program."""

        return self.program_service.delete_program(program_id)
