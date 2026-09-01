from src.models.user import User
from src.views.dashboard_view import DashboardView


def test_admin_dashboard_is_displayed(capsys) -> None:
    """Verify that the admin dashboard is displayed."""

    user = User(
        username="admin_test",
        password_hash="hashed_password",
        role="admin",
        full_name="Admin Test",
        email="admin@example.com",
        is_active=True,
    )

    view = DashboardView()
    view.display(user)

    captured = capsys.readouterr()

    assert "ADMIN DASHBOARD" in captured.out
    assert "User Management" in captured.out
    assert "Student Management" in captured.out
    assert "Grade Management" in captured.out
    assert "Reports" in captured.out


def test_staff_dashboard_is_displayed(capsys) -> None:
    """Verify that the staff dashboard is displayed."""

    user = User(
        username="staff_test",
        password_hash="hashed_password",
        role="staff",
        full_name="Staff Test",
        email="staff@example.com",
        is_active=True,
    )

    view = DashboardView()
    view.display(user)

    captured = capsys.readouterr()

    assert "STAFF DASHBOARD" in captured.out
    assert "Student Management" in captured.out
    assert "Course Management" in captured.out
    assert "Enrollment Management" in captured.out
    assert "Grade Management" in captured.out
    assert "Reports" in captured.out


def test_dashboard_displays_user_name(capsys) -> None:
    """Verify that the authenticated user's name is displayed."""

    user = User(
        username="staff_test",
        password_hash="hashed_password",
        role="staff",
        full_name="Joseph Test User",
        email="joseph@example.com",
        is_active=True,
    )

    view = DashboardView()
    view.display(user)

    captured = capsys.readouterr()

    assert "Welcome, Joseph Test User!" in captured.out