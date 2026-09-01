from typing import Optional

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.password import verify_password


class AuthenticationService:
    """Handles user authentication."""

    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        """Initialize the authentication service."""

        self.user_repository = user_repository or UserRepository()

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Optional[User]:
        """Authenticate a user using username and password.

        Returns the authenticated User when credentials are valid.
        Returns None when authentication fails.
        """

        if not username.strip():
            return None

        if not password:
            return None

        user = self.user_repository.find_by_username(username)

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user