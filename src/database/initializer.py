"""
SQLite database initialization.

Creates the Student Management System database from schema.sql.
"""

from __future__ import annotations

import sqlite3

from src.config import DATABASE_PATH, SCHEMA_PATH


def initialize_database() -> None:
    """Create the SQLite database using the SQL schema."""

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Database schema not found: {SCHEMA_PATH}"
        )

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    schema = SCHEMA_PATH.read_text(
        encoding="utf-8"
    )

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")

        connection.executescript(schema)

        connection.commit()


if __name__ == "__main__":
    initialize_database()

    print(
        f"Database initialized successfully:\n"
        f"{DATABASE_PATH}"
    )