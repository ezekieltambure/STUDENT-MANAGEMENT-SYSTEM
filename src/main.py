from src.views.dashboard_view import DashboardView
from src.views.login_view import LoginView


def main() -> None:
    """Start the IBS Student Management System."""

    login_view = LoginView()
    user = login_view.display_login()

    if user is None:
        return

    dashboard_view = DashboardView()
    dashboard_view.run(user)


if __name__ == "__main__":
    main()
