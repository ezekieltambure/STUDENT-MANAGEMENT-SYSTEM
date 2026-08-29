"""
SQLite database connection management.

This module provides a reusable database connection for the
IBS Student Management System.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from src.config import DATABASE_PATH


class DatabaseConnection:
    """Manage SQLite database connections."""

    def __init__(self, database_path: Path | None = None) -> None:
        """Initialize the database connection manager."""
        self.database_path = database_path or DATABASE_PATH
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """
        Create and return a SQLite database connection.

        Foreign-key enforcement is enabled for every connection.
        """
        if self._connection is None:
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._connection = sqlite3.connect(
                self.database_path
            )

            self._connection.row_factory = sqlite3.Row

            self._connection.execute(
                "PRAGMA foreign_keys = ON"
            )

        return self._connection

    def close(self) -> None:
        """Close the active database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> sqlite3.Connection:
        """Open the connection when entering a context manager."""
        return self.connect()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """Close the connection when leaving a context manager."""
        self.close()