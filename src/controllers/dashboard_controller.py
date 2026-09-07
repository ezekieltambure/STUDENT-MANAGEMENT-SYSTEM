from typing import Optional

from src.models.student import Student
from src.models.user import User
from src.services.dashboard_service import DashboardService


class DashboardController:
    """Coordinates dashboard access and dashboard data."""

    def __init__(
        self,
        dashboard_service: Optional[DashboardService] = None,
    ) -> None:
        """Initialize the dashboard controller."""

        self.dashboard_service = (
            dashboard_service or DashboardService()
        )

    def get_dashboard(self, user: User) -> str:
        """Return the dashboard name available to the user's role."""

        if user.role == "admin":
            return "admin"

        if user.role == "staff":
            return "staff"

        raise ValueError(f"Unsupported user role: {user.role}")

    def get_dashboard_data(self) -> dict:
        """Return statistics and recent students for the dashboard."""

        return {
            "total_students": self.dashboard_service.get_total_students(),
            "active_students": self.dashboard_service.get_active_students(),
            "inactive_students": self.dashboard_service.get_inactive_students(),
            "program_count": self.dashboard_service.get_program_count(),
            "recent_students": self.dashboard_service.get_recent_students(),
        }
