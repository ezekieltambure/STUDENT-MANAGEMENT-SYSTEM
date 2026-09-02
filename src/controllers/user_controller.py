from typing import Optional

from src.models.user import User
from src.services.user_service import UserService


class UserController:
    """Coordinates user management operations."""

    def __init__(
        self,
        user_service: Optional[UserService] = None,
    ) -> None:
        """Initialize the user controller."""

        self.user_service = user_service or UserService()

    def create_user(
        self,
        username: str,
        password: str,
        role: str,
        full_name: str,
        email: str,
    ) -> User:
        """Create a new system user."""

        return self.user_service.create_user(
            username=username,
            password=password,
            role=role,
            full_name=full_name,
            email=email,
        )

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""

        return self.user_service.get_user(user_id)

    def get_user_by_username(
        self,
        username: str,
    ) -> Optional[User]:
        """Retrieve a user by username."""

        return self.user_service.get_user_by_username(username)

    def update_user(
        self,
        user: User,
        password: Optional[str] = None,
    ) -> User:
        """Update an existing user."""

        return self.user_service.update_user(
            user=user,
            password=password,
        )

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""

        return self.user_service.delete_user(user_id)

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account."""

        return self.user_service.deactivate_user(user_id)

    def activate_user(self, user_id: int) -> bool:
        """Activate a user account."""

        return self.user_service.activate_user(user_id)
