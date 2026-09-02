from src.controllers.dashboard_controller import DashboardController
from src.models.user import User
from src.views.student_view import StudentView
from src.views.user_view import UserView
from src.views.department_view import DepartmentView
from src.views.course_view import CourseView
from src.views.enrollment_view import EnrollmentView
from src.views.grade_view import GradeView


class DashboardView:
    """Terminal-based role-specific dashboard."""

    def __init__(
        self,
        dashboard_controller: DashboardController | None = None,
        student_view: StudentView | None = None,
        user_view: UserView | None = None,
        department_view: DepartmentView | None = None,
        course_view: CourseView | None = None,
        enrollment_view: EnrollmentView | None = None,
        grade_view: GradeView | None = None,
    ) -> None:
        """Initialize the dashboard view."""

        self.dashboard_controller = (
            dashboard_controller or DashboardController()
        )
        self.student_view = student_view or StudentView()
        self.user_view = user_view or UserView()
        self.department_view = department_view or DepartmentView()
        self.course_view = course_view or CourseView()
        self.enrollment_view = enrollment_view or EnrollmentView()
        self.grade_view = grade_view or GradeView()

    def display(self, user: User) -> None:
        """Display the dashboard without requesting user input."""

        dashboard = self.dashboard_controller.get_dashboard(user)

        print()
        print("=" * 50)

        if dashboard == "admin":
            self._display_admin_dashboard(user)
        elif dashboard == "staff":
            self._display_staff_dashboard(user)

        print("=" * 50)

    def run(self, user: User) -> None:
        """Run the interactive dashboard menu."""

        dashboard = self.dashboard_controller.get_dashboard(user)

        while True:
            self.display(user)

            choice = input("Select an option: ").strip()

            if choice == "0":
                print()
                print("Logging out...")
                break

            if dashboard == "admin" and choice == "1":
                self.user_view.run()
                continue

            if dashboard == "admin" and choice == "2":
                self.student_view_loop()
                continue

            if dashboard == "admin" and choice == "3":
                self.department_view.run()
                continue

            if dashboard == "admin" and choice == "4":
                self.course_view.run()
                continue

            if dashboard == "admin" and choice == "5":
                self.enrollment_view.run()
                continue

            if dashboard == "admin" and choice == "6":
                self.grade_view.run()
                continue

            if dashboard == "staff" and choice == "1":
                self.student_view_loop()
                continue

            if dashboard == "staff" and choice == "2":
                self.course_view.run()
                continue

            if dashboard == "staff" and choice == "3":
                self.enrollment_view.run()
                continue

            if dashboard == "staff" and choice == "4":
                self.grade_view.run()
                continue

            print()
            print("Invalid option. Please try again.")

    def student_view_loop(self) -> None:
        """Run the student management menu."""

        while True:
            self.student_view.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.student_view.add_student()

            elif choice == "2":
                self.student_view.search_student()

            elif choice == "3":
                self.student_view.update_student()

            elif choice == "4":
                self.student_view.delete_student()

            elif choice == "5":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def _display_admin_dashboard(self, user: User) -> None:
        """Display the administrator dashboard."""

        print("       IBS STUDENT MANAGEMENT SYSTEM")
        print("             ADMIN DASHBOARD")
        print("=" * 50)
        print(f"Welcome, {user.full_name}!")
        print()
        print("1. User Management")
        print("2. Student Management")
        print("3. Department Management")
        print("4. Course Management")
        print("5. Enrollment Management")
        print("6. Grade Management")
        print("7. Reports")
        print("0. Logout")

    def _display_staff_dashboard(self, user: User) -> None:
        """Display the staff dashboard."""

        print("       IBS STUDENT MANAGEMENT SYSTEM")
        print("             STAFF DASHBOARD")
        print("=" * 50)
        print(f"Welcome, {user.full_name}!")
        print()
        print("1. Student Management")
        print("2. Course Management")
        print("3. Enrollment Management")
        print("4. Grade Management")
        print("5. Reports")
        print("0. Logout")
