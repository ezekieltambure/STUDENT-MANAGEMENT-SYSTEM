from typing import Optional

from src.controllers.login_controller import LoginController
from src.models.user import User


class LoginView:
    """Terminal-based view for user login."""

    def __init__(
        self,
        login_controller: Optional[LoginController] = None,
    ) -> None:
        """Initialize the login view."""

        self.login_controller = login_controller or LoginController()

    def display_login(self) -> Optional[User]:
        """Display the login form and process the user's credentials."""

        print()
        print("=" * 50)
        print("       IBS STUDENT MANAGEMENT SYSTEM")
        print("                  LOGIN")
        print("=" * 50)

        username = input("Username: ").strip()
        password = input("Password: ")

        user = self.login_controller.login(
            username=username,
            password=password,
        )

        if user is None:
            print()
            print("Login failed: Invalid username or password.")
            return None

        print()
        print(f"Login successful. Welcome, {user.full_name}!")
        print(f"Role: {user.role}")

        return user