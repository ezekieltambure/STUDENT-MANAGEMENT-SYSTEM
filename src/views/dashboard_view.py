from src.controllers.dashboard_controller import DashboardController
from src.models.user import User


class DashboardView:
    """Terminal-based role-specific dashboard."""

    def __init__(
        self,
        dashboard_controller: DashboardController | None = None,
    ) -> None:
        """Initialize the dashboard view."""

        self.dashboard_controller = (
            dashboard_controller or DashboardController()
        )

    def display(self, user: User) -> None:
        """Display the dashboard available to the user's role."""

        dashboard = self.dashboard_controller.get_dashboard(user)

        print()
        print("=" * 50)

        if dashboard == "admin":
            self._display_admin_dashboard(user)
        elif dashboard == "staff":
            self._display_staff_dashboard(user)

        print("=" * 50)

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