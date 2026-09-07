from typing import List, Optional

from src.models.program import Program
from src.repositories.department_repository import DepartmentRepository
from src.repositories.program_repository import ProgramRepository


class ProgramService:
    """Business logic for academic programs."""

    def __init__(
        self,
        program_repository: Optional[ProgramRepository] = None,
        department_repository: Optional[DepartmentRepository] = None,
    ) -> None:
        self.program_repository = program_repository or ProgramRepository()
        self.department_repository = (
            department_repository or DepartmentRepository()
        )

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
        """Create a new academic program."""

        if self.program_repository.exists_by_code(program_code):
            raise ValueError(
                f"Program code '{program_code.strip().upper()}' already exists."
            )

        if self.program_repository.exists_by_name(program_name):
            raise ValueError(
                f"Program name '{program_name.strip()}' already exists."
            )

        department = self.department_repository.find_by_id(department_id)

        if department is None:
            raise ValueError(
                f"Department with ID {department_id} does not exist."
            )

        program = Program(
            program_code=program_code,
            program_name=program_name,
            qualification=qualification,
            duration_years=duration_years,
            department_id=department_id,
            description=description,
            status=status,
        )

        return self.program_repository.create(program)

    def get_program(self, program_id: int) -> Optional[Program]:
        """Get a program by ID."""

        return self.program_repository.find_by_id(program_id)

    def get_program_by_code(self, program_code: str) -> Optional[Program]:
        """Get a program by code."""

        return self.program_repository.find_by_code(program_code)

    def get_program_by_name(self, program_name: str) -> Optional[Program]:
        """Get a program by name."""

        return self.program_repository.find_by_name(program_name)

    def get_all_programs(self) -> List[Program]:
        """Get all academic programs."""

        return self.program_repository.list_all()

    def search_programs(self, search_term: str = "") -> List[Program]:
        """Search academic programs."""

        return self.program_repository.search(search_term)

    def update_program(self, program: Program) -> bool:
        """Update an existing academic program."""

        if program.id is None:
            raise ValueError("Program ID is required for update.")

        department = self.department_repository.find_by_id(
            program.department_id
        )

        if department is None:
            raise ValueError(
                f"Department with ID {program.department_id} does not exist."
            )

        existing_code = self.program_repository.find_by_code(
            program.program_code
        )

        if existing_code is not None and existing_code.id != program.id:
            raise ValueError(
                f"Program code '{program.program_code}' already exists."
            )

        existing_name = self.program_repository.find_by_name(
            program.program_name
        )

        if existing_name is not None and existing_name.id != program.id:
            raise ValueError(
                f"Program name '{program.program_name}' already exists."
            )

        return self.program_repository.update(program)

    def delete_program(self, program_id: int) -> bool:
        """Delete an academic program."""

        existing_program = self.program_repository.find_by_id(program_id)

        if existing_program is None:
            raise ValueError(
                f"Program with ID {program_id} does not exist."
            )

        return self.program_repository.delete(program_id)
