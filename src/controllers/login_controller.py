from typing import Optional

from src.models.user import User
from src.services.auth_service import AuthenticationService


class LoginController:
    """Coordinates the login process between the view and authentication service."""

    def __init__(
        self,
        authentication_service: Optional[AuthenticationService] = None,
    ) -> None:
        """Initialize the login controller."""

        self.authentication_service = (
            authentication_service or AuthenticationService()
        )

    def login(
        self,
        username: str,
        password: str,
    ) -> Optional[User]:
        """Authenticate a user and return the authenticated user.

        Returns:
            User: When the credentials are valid.
            None: When authentication fails.
        """

        return self.authentication_service.authenticate(
            username=username,
            password=password,
        )