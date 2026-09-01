from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Represents a system user.

    A user can have one of the supported roles:
    - admin
    - staff
    """

    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = "staff"
    full_name: str = ""
    email: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    ALLOWED_ROLES = {"admin", "staff"}

    def __post_init__(self) -> None:
        """Validate the user after initialization."""

        if not self.username.strip():
            raise ValueError("Username cannot be empty.")

        if self.role not in self.ALLOWED_ROLES:
            raise ValueError(
                f"Invalid role '{self.role}'. "
                f"Allowed roles: {', '.join(sorted(self.ALLOWED_ROLES))}."
            )

        if self.email and "@" not in self.email:
            raise ValueError("Invalid email address.")

    def is_admin(self) -> bool:
        """Return True when the user has administrator privileges."""
        return self.role == "admin"

    def is_staff(self) -> bool:
        """Return True when the user has staff privileges."""
        return self.role == "staff"

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True

    def __str__(self) -> str:
        """Return a human-readable representation of the user."""
        return f"{self.username} ({self.role})"