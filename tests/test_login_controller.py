import pytest

from src.controllers.login_controller import LoginController
from src.models.user import User


class FakeAuthenticationService:
    """Test double for the authentication service."""

    def __init__(self, authenticated_user=None):
        self.authenticated_user = authenticated_user
        self.received_username = None
        self.received_password = None

    def authenticate(self, username: str, password: str):
        self.received_username = username
        self.received_password = password
        return self.authenticated_user


@pytest.fixture
def user() -> User:
    return User(
        id=1,
        username="test_user",
        password_hash="hashed_password",
        role="staff",
        full_name="Test User",
        email="test@example.com",
        is_active=True,
    )


def test_login_returns_authenticated_user(user: User) -> None:
    service = FakeAuthenticationService(authenticated_user=user)
    controller = LoginController(service)

    result = controller.login("test_user", "password123")

    assert result is user


def test_login_returns_none_when_authentication_fails() -> None:
    service = FakeAuthenticationService(authenticated_user=None)
    controller = LoginController(service)

    result = controller.login("test_user", "wrong_password")

    assert result is None


def test_login_passes_credentials_to_authentication_service(
    user: User,
) -> None:
    service = FakeAuthenticationService(authenticated_user=user)
    controller = LoginController(service)

    controller.login("test_user", "password123")

    assert service.received_username == "test_user"
    assert service.received_password == "password123"


def test_controller_can_use_default_authentication_service() -> None:
    controller = LoginController()

    assert controller.authentication_service is not None