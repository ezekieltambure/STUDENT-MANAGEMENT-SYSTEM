from src.controllers.department_controller import DepartmentController
from src.models.department import Department


class DepartmentView:
    """Terminal-based department management interface."""

    def __init__(
        self,
        department_controller: DepartmentController | None = None,
    ) -> None:
        """Initialize the department management view."""

        self.department_controller = (
            department_controller or DepartmentController()
        )

    def display_menu(self) -> None:
        """Display the department management menu."""

        print()
        print("=" * 50)
        print("          DEPARTMENT MANAGEMENT")
        print("=" * 50)
        print("1. List Departments")
        print("2. Add Department")
        print("3. Search Department")
        print("4. Update Department")
        print("5. Delete Department")
        print("6. Exit")
        print("=" * 50)

    def run(self) -> None:
        """Run the interactive department management menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.list_departments()

            elif choice == "2":
                self.add_department()

            elif choice == "3":
                self.search_department()

            elif choice == "4":
                self.update_department()

            elif choice == "5":
                self.delete_department()

            elif choice == "6":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def list_departments(self) -> None:
        """Display all departments."""

        departments = (
            self.department_controller.get_all_departments()
        )

        print()
        print("=" * 70)
        print("                    DEPARTMENTS")
        print("=" * 70)

        if not departments:
            print("No departments found.")
            print("=" * 70)
            return

        print(
            f"{'ID':<6}"
            f"{'CODE':<12}"
            f"{'DEPARTMENT NAME':<40}"
        )
        print("-" * 70)

        for department in departments:
            print(
                f"{department.id:<6}"
                f"{department.department_code:<12}"
                f"{department.department_name:<40}"
            )

        print("=" * 70)

    def add_department(self) -> None:
        """Create a new department."""

        print()
        print("-" * 50)
        print("             ADD DEPARTMENT")
        print("-" * 50)

        code = input("Department Code: ").strip()
        name = input("Department Name: ").strip()
        description = input("Description: ").strip()

        try:
            department = (
                self.department_controller.create_department(
                    department_code=code,
                    department_name=name,
                    description=description,
                )
            )

            print()
            print("Department created successfully.")
            print(f"Department ID: {department.id}")
            print(f"Code: {department.department_code}")
            print(f"Name: {department.department_name}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def search_department(self) -> None:
        """Search for a department by code."""

        print()
        print("-" * 50)
        print("           SEARCH DEPARTMENT")
        print("-" * 50)

        code = input("Department Code: ").strip()

        department = (
            self.department_controller.get_department_by_code(
                code
            )
        )

        if department is None:
            print()
            print("Department not found.")
            return

        self._display_department(department)

    def update_department(self) -> None:
        """Update an existing department."""

        print()
        print("-" * 50)
        print("            UPDATE DEPARTMENT")
        print("-" * 50)

        code = input("Department Code: ").strip()

        department = (
            self.department_controller.get_department_by_code(
                code
            )
        )

        if department is None:
            print()
            print("Department not found.")
            return

        print()
        print("Press Enter to keep the current value.")

        new_code = input(
            f"Department Code [{department.department_code}]: "
        ).strip()

        new_name = input(
            f"Department Name [{department.department_name}]: "
        ).strip()

        new_description = input(
            f"Description [{department.description}]: "
        ).strip()

        if new_code:
            department.department_code = new_code.upper()

        if new_name:
            department.department_name = new_name

        if new_description:
            department.description = new_description

        try:
            updated = (
                self.department_controller.update_department(
                    department
                )
            )

            print()
            print("Department updated successfully.")
            print(f"Code: {updated.department_code}")
            print(f"Name: {updated.department_name}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def delete_department(self) -> None:
        """Delete a department."""

        print()
        print("-" * 50)
        print("            DELETE DEPARTMENT")
        print("-" * 50)

        code = input("Department Code: ").strip()

        department = (
            self.department_controller.get_department_by_code(
                code
            )
        )

        if department is None:
            print()
            print("Department not found.")
            return

        print()
        print(f"Department: {department.department_name}")

        confirmation = input(
            "Are you sure you want to delete this department? "
            "(yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print()
            print("Deletion cancelled.")
            return

        try:
            success = (
                self.department_controller.delete_department(
                    department.id
                )
            )

            print()

            if success:
                print("Department deleted successfully.")
            else:
                print("Unable to delete department.")

        except Exception as error:
            print()
            print(
                "Unable to delete department."
            )
            print(f"Reason: {error}")

    @staticmethod
    def _display_department(
        department: Department,
    ) -> None:
        """Display department information."""

        print()
        print("=" * 50)
        print("           DEPARTMENT DETAILS")
        print("=" * 50)
        print(f"Department ID:   {department.id}")
        print(f"Code:            {department.department_code}")
        print(f"Name:            {department.department_name}")
        print(f"Description:     {department.description}")
        print("=" * 50)
