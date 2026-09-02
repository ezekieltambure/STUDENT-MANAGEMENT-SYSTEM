from src.controllers.course_controller import CourseController
from src.controllers.department_controller import DepartmentController
from src.models.course import Course


class CourseView:
    """Terminal-based course management interface."""

    def __init__(
        self,
        course_controller: CourseController | None = None,
        department_controller: DepartmentController | None = None,
    ) -> None:
        self.course_controller = (
            course_controller or CourseController()
        )
        self.department_controller = (
            department_controller or DepartmentController()
        )

    def display_menu(self) -> None:
        """Display the course management menu."""

        print()
        print("=" * 60)
        print("                 COURSE MANAGEMENT")
        print("=" * 60)
        print("1. List Courses")
        print("2. Add Course")
        print("3. Search Course")
        print("4. Update Course")
        print("5. Delete Course")
        print("6. Exit")
        print("=" * 60)

    def run(self) -> None:
        """Run the interactive course management menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.list_courses()

            elif choice == "2":
                self.add_course()

            elif choice == "3":
                self.search_course()

            elif choice == "4":
                self.update_course()

            elif choice == "5":
                self.delete_course()

            elif choice == "6":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def list_courses(self) -> None:
        """Display all courses."""

        courses = self.course_controller.get_all_courses()

        print()
        print("=" * 100)
        print("                              COURSES")
        print("=" * 100)

        if not courses:
            print("No courses found.")
            print("=" * 100)
            return

        print(
            f"{'ID':<6}"
            f"{'CODE':<14}"
            f"{'COURSE NAME':<35}"
            f"{'CREDITS':<10}"
            f"{'DEPARTMENT':<25}"
        )
        print("-" * 100)

        for course in courses:
            department = (
                self.department_controller.get_department(
                    course.department_id
                )
            )

            department_name = (
                department.department_name
                if department
                else "Unknown"
            )

            print(
                f"{course.id:<6}"
                f"{course.course_code:<14}"
                f"{course.course_name:<35}"
                f"{course.credit_hours:<10}"
                f"{department_name:<25}"
            )

        print("=" * 100)

    def add_course(self) -> None:
        """Create a new course."""

        print()
        print("-" * 60)
        print("                    ADD COURSE")
        print("-" * 60)

        self._display_departments()

        code = input("Course Code: ").strip()
        name = input("Course Name: ").strip()
        description = input("Description: ").strip()

        try:
            credit_hours = int(
                input("Credit Hours: ").strip()
            )
            department_id = int(
                input("Department ID: ").strip()
            )

            course = self.course_controller.create_course(
                course_code=code,
                course_name=name,
                credit_hours=credit_hours,
                department_id=department_id,
                description=description,
            )

            print()
            print("Course created successfully.")
            print(f"Course ID: {course.id}")
            print(f"Code: {course.course_code}")
            print(f"Name: {course.course_name}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def search_course(self) -> None:
        """Search for a course by course code."""

        print()
        print("-" * 60)
        print("                   SEARCH COURSE")
        print("-" * 60)

        code = input("Course Code: ").strip()

        course = self.course_controller.get_course_by_code(
            code
        )

        if course is None:
            print()
            print("Course not found.")
            return

        self._display_course(course)

    def update_course(self) -> None:
        """Update an existing course."""

        print()
        print("-" * 60)
        print("                    UPDATE COURSE")
        print("-" * 60)

        code = input("Course Code: ").strip()

        course = self.course_controller.get_course_by_code(
            code
        )

        if course is None:
            print()
            print("Course not found.")
            return

        department = self.department_controller.get_department(
            course.department_id
        )

        current_department = (
            department.department_name
            if department
            else "Unknown"
        )

        print()
        print("Press Enter to keep the current value.")
        print()

        new_code = input(
            f"Course Code [{course.course_code}]: "
        ).strip()

        new_name = input(
            f"Course Name [{course.course_name}]: "
        ).strip()

        new_description = input(
            f"Description [{course.description}]: "
        ).strip()

        new_credit_hours = input(
            f"Credit Hours [{course.credit_hours}]: "
        ).strip()

        print(
            f"Current Department: "
            f"{current_department}"
        )

        change_department = input(
            "Change Department? (yes/no): "
        ).strip().lower()

        if new_code:
            course.course_code = new_code.upper()

        if new_name:
            course.course_name = new_name

        if new_description:
            course.description = new_description

        if new_credit_hours:
            try:
                course.credit_hours = int(
                    new_credit_hours
                )
            except ValueError:
                print()
                print("Credit hours must be a valid integer.")
                return

        if change_department == "yes":
            self._display_departments()

            new_department_id = input(
                f"Department ID [{course.department_id}]: "
            ).strip()

            if new_department_id:
                try:
                    course.department_id = int(
                        new_department_id
                    )
                except ValueError:
                    print()
                    print("Department ID must be a valid integer.")
                    return

        try:
            updated = self.course_controller.update_course(
                course
            )

            print()
            print("Course updated successfully.")
            print(f"Code: {updated.course_code}")
            print(f"Name: {updated.course_name}")
            print(f"Credits: {updated.credit_hours}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def delete_course(self) -> None:
        """Delete a course."""

        print()
        print("-" * 60)
        print("                    DELETE COURSE")
        print("-" * 60)

        code = input("Course Code: ").strip()

        course = self.course_controller.get_course_by_code(
            code
        )

        if course is None:
            print()
            print("Course not found.")
            return

        print()
        print(f"Course: {course.course_code}")
        print(f"Name: {course.course_name}")

        confirmation = input(
            "Are you sure you want to delete this course? "
            "(yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print()
            print("Deletion cancelled.")
            return

        try:
            success = self.course_controller.delete_course(
                course.id
            )

            print()

            if success:
                print("Course deleted successfully.")
            else:
                print("Unable to delete course.")

        except Exception as error:
            print()
            print("Unable to delete course.")
            print(f"Reason: {error}")

    def _display_departments(self) -> None:
        """Display available departments."""

        departments = (
            self.department_controller.get_all_departments()
        )

        print()
        print("Available Departments")
        print("-" * 60)

        if not departments:
            print("No departments available.")
            print("-" * 60)
            return

        print(
            f"{'ID':<6}"
            f"{'CODE':<12}"
            f"{'DEPARTMENT NAME':<40}"
        )
        print("-" * 60)

        for department in departments:
            print(
                f"{department.id:<6}"
                f"{department.department_code:<12}"
                f"{department.department_name:<40}"
            )

        print("-" * 60)

    def _display_course(self, course: Course) -> None:
        """Display course information."""

        department = self.department_controller.get_department(
            course.department_id
        )

        department_name = (
            department.department_name
            if department
            else "Unknown"
        )

        print()
        print("=" * 60)
        print("                    COURSE DETAILS")
        print("=" * 60)
        print(f"Course ID:       {course.id}")
        print(f"Code:            {course.course_code}")
        print(f"Name:            {course.course_name}")
        print(f"Description:     {course.description}")
        print(f"Credit Hours:    {course.credit_hours}")
        print(f"Department:      {department_name}")
        print("=" * 60)
