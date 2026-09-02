from typing import Optional

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.password import hash_password


class UserService:
    """Handles business logic for system users."""

    def __init__(
        self,
        user_repository: Optional[UserRepository] = None,
    ) -> None:
        """Initialize the user service."""

        self.user_repository = user_repository or UserRepository()

    def create_user(
        self,
        username: str,
        password: str,
        role: str,
        full_name: str,
        email: str,
    ) -> User:
        """Create a new system user."""

        username = username.strip()
        full_name = full_name.strip()
        email = email.strip()

        if self.user_repository.exists_by_username(username):
            raise ValueError("Username already exists.")

        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role,
            full_name=full_name,
            email=email,
        )

        return self.user_repository.create(user)

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""

        return self.user_repository.find_by_id(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""

        return self.user_repository.find_by_username(username)

    def update_user(
        self,
        user: User,
        password: Optional[str] = None,
    ) -> User:
        """Update a user's details.

        If a new password is provided, it is securely hashed before storage.
        """

        if password:
            user.password_hash = hash_password(password)

        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""

        return self.user_repository.delete(user_id)

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user account."""

        user = self.user_repository.find_by_id(user_id)

        if user is None:
            return False

        user.deactivate()
        self.user_repository.update(user)

        return True

    def activate_user(self, user_id: int) -> bool:
        """Activate a user account."""

        user = self.user_repository.find_by_id(user_id)

        if user is None:
            return False

        user.activate()
        self.user_repository.update(user)

        return True
