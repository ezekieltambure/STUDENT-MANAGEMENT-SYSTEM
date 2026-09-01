from unittest.mock import patch

from src.models.user import User
from src.views.login_view import LoginView


class FakeLoginController:
    """Test double for the login controller."""

    def __init__(self, authenticated_user=None):
        self.authenticated_user = authenticated_user
        self.received_username = None
        self.received_password = None

    def login(self, username: str, password: str):
        self.received_username = username
        self.received_password = password
        return self.authenticated_user


def test_login_view_returns_authenticated_user() -> None:
    user = User(
        id=1,
        username="test_user",
        password_hash="hashed_password",
        role="staff",
        full_name="Test User",
        email="test@example.com",
        is_active=True,
    )

    controller = FakeLoginController(authenticated_user=user)
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["test_user", "password123"],
    ):
        result = view.display_login()

    assert result is user


def test_login_view_returns_none_when_login_fails() -> None:
    controller = FakeLoginController(authenticated_user=None)
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["test_user", "wrong_password"],
    ):
        result = view.display_login()

    assert result is None


def test_login_view_passes_entered_credentials_to_controller() -> None:
    controller = FakeLoginController()
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["test_user", "password123"],
    ):
        view.display_login()

    assert controller.received_username == "test_user"
    assert controller.received_password == "password123"


def test_login_view_strips_username_whitespace() -> None:
    controller = FakeLoginController()
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["  test_user  ", "password123"],
    ):
        view.display_login()

    assert controller.received_username == "test_user"


def test_login_view_displays_success_message(capsys) -> None:
    user = User(
        id=1,
        username="test_user",
        password_hash="hashed_password",
        role="admin",
        full_name="Test Administrator",
        email="admin@example.com",
        is_active=True,
    )

    controller = FakeLoginController(authenticated_user=user)
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["test_user", "password123"],
    ):
        view.display_login()

    output = capsys.readouterr().out

    assert "Login successful" in output
    assert "Welcome, Test Administrator!" in output
    assert "Role: admin" in output


def test_login_view_displays_failure_message(capsys) -> None:
    controller = FakeLoginController(authenticated_user=None)
    view = LoginView(controller)

    with patch(
        "builtins.input",
        side_effect=["test_user", "wrong_password"],
    ):
        view.display_login()

    output = capsys.readouterr().out

    assert "Login failed" in output
    assert "Invalid username or password" in output