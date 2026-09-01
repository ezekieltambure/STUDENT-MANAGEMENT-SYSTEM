from typing import Optional

from src.database.connection import get_connection
from src.models.user import User


class UserRepository:
    """Handles database operations for User records."""

    def create(self, user: User) -> User:
        """Create a new user and return it with its database ID."""

        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (
                    username,
                    password_hash,
                    role,
                    full_name,
                    email,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user.username,
                    user.password_hash,
                    user.role,
                    user.full_name,
                    user.email,
                    int(user.is_active),
                ),
            )

            user.id = cursor.lastrowid
            connection.commit()

        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their database ID."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    user_id,
                    username,
                    password_hash,
                    role,
                    full_name,
                    email,
                    is_active,
                    created_at,
                    updated_at
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_user(row)

    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    user_id,
                    username,
                    password_hash,
                    role,
                    full_name,
                    email,
                    is_active,
                    created_at,
                    updated_at
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_user(row)

    def update(self, user: User) -> User:
        """Update an existing user."""

        if user.id is None:
            raise ValueError("Cannot update a user without an ID.")

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE users
                SET
                    username = ?,
                    password_hash = ?,
                    role = ?,
                    full_name = ?,
                    email = ?,
                    is_active = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
                """,
                (
                    user.username,
                    user.password_hash,
                    user.role,
                    user.full_name,
                    user.email,
                    int(user.is_active),
                    user.id,
                ),
            )

            connection.commit()

        return user

    def delete(self, user_id: int) -> bool:
        """Delete a user by ID.

        Returns True if a record was deleted, otherwise False.
        """

        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            )

            connection.commit()

        return cursor.rowcount > 0

    def exists_by_username(self, username: str) -> bool:
        """Check whether a username already exists."""

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM users
                WHERE username = ?
                LIMIT 1
                """,
                (username,),
            ).fetchone()

        return row is not None

    @staticmethod
    def _row_to_user(row) -> User:
        """Convert a SQLite row into a User object."""

        return User(
            id=row["user_id"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"],
            full_name=row["full_name"],
            email=row["email"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

