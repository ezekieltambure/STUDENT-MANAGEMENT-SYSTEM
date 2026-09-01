from src.models.user import User


class DashboardController:
    """Controls role-based access to system dashboards."""

    def get_dashboard(self, user: User) -> str:
        """Return the dashboard name available to the user's role."""

        if user.role == "admin":
            return "admin"

        if user.role == "staff":
            return "staff"

        raise ValueError(f"Unsupported user role: {user.role}")