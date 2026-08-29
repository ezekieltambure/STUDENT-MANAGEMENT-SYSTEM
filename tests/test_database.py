"""
Database structure tests.
"""

from __future__ import annotations

import sqlite3

from src.config import DATABASE_PATH
from src.database.connection import DatabaseConnection


def test_database_exists() -> None:
    """Verify that the SQLite database file exists."""
    assert DATABASE_PATH.exists()


def test_required_tables_exist() -> None:
    """Verify that all required database tables exist."""

    expected_tables = {
        "users",
        "departments",
        "academic_terms",
        "students",
        "courses",
        "enrollments",
        "grades",
    }

    with DatabaseConnection() as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    actual_tables = {
        row["name"]
        for row in rows
    }

    assert expected_tables.issubset(actual_tables)


def test_foreign_keys_are_enabled() -> None:
    """Verify foreign-key enforcement is enabled by our connection."""

    database = DatabaseConnection()

    try:
        connection = database.connect()

        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

        assert result is not None
        assert result[0] == 1

    finally:
        database.close()