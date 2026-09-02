from typing import List, Optional

from src.models.department import Department
from src.repositories.department_repository import DepartmentRepository


class DepartmentService:
    """Handles business logic for academic departments."""

    def __init__(
        self,
        department_repository: Optional[DepartmentRepository] = None,
    ) -> None:
        """Initialize the department service."""

        self.department_repository = (
            department_repository or DepartmentRepository()
        )

    def create_department(
        self,
        department_code: str,
        department_name: str,
        description: str = "",
    ) -> Department:
        """Create a new department."""

        department_code = department_code.strip().upper()
        department_name = department_name.strip()
        description = description.strip()

        if self.department_repository.exists_by_code(
            department_code
        ):
            raise ValueError(
                "Department code already exists."
            )

        if self.department_repository.exists_by_name(
            department_name
        ):
            raise ValueError(
                "Department name already exists."
            )

        department = Department(
            department_code=department_code,
            department_name=department_name,
            description=description,
        )

        return self.department_repository.create(department)

    def get_department(
        self,
        department_id: int,
    ) -> Optional[Department]:
        """Retrieve a department by ID."""

        return self.department_repository.find_by_id(
            department_id
        )

    def get_department_by_code(
        self,
        department_code: str,
    ) -> Optional[Department]:
        """Retrieve a department by code."""

        return self.department_repository.find_by_code(
            department_code.strip().upper()
        )

    def get_department_by_name(
        self,
        department_name: str,
    ) -> Optional[Department]:
        """Retrieve a department by name."""

        return self.department_repository.find_by_name(
            department_name.strip()
        )

    def get_all_departments(self) -> List[Department]:
        """Retrieve all departments."""

        return self.department_repository.list_all()

    def update_department(
        self,
        department: Department,
    ) -> Department:
        """Update an existing department."""

        existing_by_code = (
            self.department_repository.find_by_code(
                department.department_code
            )
        )

        if (
            existing_by_code is not None
            and existing_by_code.id != department.id
        ):
            raise ValueError(
                "Department code already exists."
            )

        existing_by_name = (
            self.department_repository.find_by_name(
                department.department_name
            )
        )

        if (
            existing_by_name is not None
            and existing_by_name.id != department.id
        ):
            raise ValueError(
                "Department name already exists."
            )

        return self.department_repository.update(
            department
        )

    def delete_department(
        self,
        department_id: int,
    ) -> bool:
        """Delete a department by ID."""

        return self.department_repository.delete(
            department_id
        )
