import pytest

from src.controllers.dashboard_controller import DashboardController
from src.models.user import User


@pytest.fixture
def controller() -> DashboardController:
    return DashboardController()


@pytest.fixture
def admin_user() -> User:
    return User(
        username="admin_test",
        password_hash="hashed_password",
        role="admin",
        full_name="Admin Test",
        email="admin@example.com",
        is_active=True,
    )


@pytest.fixture
def staff_user() -> User:
    return User(
        username="staff_test",
        password_hash="hashed_password",
        role="staff",
        full_name="Staff Test",
        email="staff@example.com",
        is_active=True,
    )


def test_admin_user_gets_admin_dashboard(
    controller: DashboardController,
    admin_user: User,
) -> None:
    assert controller.get_dashboard(admin_user) == "admin"


def test_staff_user_gets_staff_dashboard(
    controller: DashboardController,
    staff_user: User,
) -> None:
    assert controller.get_dashboard(staff_user) == "staff"


def test_unsupported_role_is_rejected(
    controller: DashboardController,
) -> None:
    user = User(
        username="invalid_role_test",
        password_hash="hashed_password",
        role="staff",
        full_name="Invalid Role Test",
        email="invalid@example.com",
        is_active=True,
    )

    user.role = "manager"

    with pytest.raises(ValueError):
        controller.get_dashboard(user)