from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "database" / "student_management.db"


class DatabaseConnection:
    """Manage SQLite database connections."""

    def __init__(self, database_path: Path = DATABASE_PATH) -> None:
        self.database_path = database_path
        self.connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Open and configure the SQLite database connection."""

        if self.connection is None:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row

            # Enable foreign-key enforcement.
            self.connection.execute("PRAGMA foreign_keys = ON")

        return self.connection

    def close(self) -> None:
        """Close the database connection."""

        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def __enter__(self) -> sqlite3.Connection:
        """Open the connection when entering a with-statement."""

        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Commit/rollback and close the connection."""

        if self.connection is not None:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()

        self.close()


def get_connection() -> sqlite3.Connection:
    """Create and configure a SQLite database connection."""

    database = DatabaseConnection()
    return database.connect()