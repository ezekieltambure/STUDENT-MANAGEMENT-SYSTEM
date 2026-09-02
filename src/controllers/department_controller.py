from typing import List, Optional

from src.models.department import Department
from src.services.department_service import DepartmentService


class DepartmentController:
    """Coordinates department management operations."""

    def __init__(
        self,
        department_service: Optional[DepartmentService] = None,
    ) -> None:
        """Initialize the department controller."""

        self.department_service = (
            department_service or DepartmentService()
        )

    def create_department(
        self,
        department_code: str,
        department_name: str,
        description: str = "",
    ) -> Department:
        """Create a new department."""

        return self.department_service.create_department(
            department_code=department_code,
            department_name=department_name,
            description=description,
        )

    def get_department(
        self,
        department_id: int,
    ) -> Optional[Department]:
        """Retrieve a department by ID."""

        return self.department_service.get_department(
            department_id
        )

    def get_department_by_code(
        self,
        department_code: str,
    ) -> Optional[Department]:
        """Retrieve a department by code."""

        return self.department_service.get_department_by_code(
            department_code
        )

    def get_all_departments(self) -> List[Department]:
        """Retrieve all departments."""

        return self.department_service.get_all_departments()

    def update_department(
        self,
        department: Department,
    ) -> Department:
        """Update an existing department."""

        return self.department_service.update_department(
            department
        )

    def delete_department(
        self,
        department_id: int,
    ) -> bool:
        """Delete a department."""

        return self.department_service.delete_department(
            department_id
        )
