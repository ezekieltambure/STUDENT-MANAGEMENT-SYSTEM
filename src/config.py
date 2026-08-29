"""
Application configuration for the IBS Student Management System.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

# src/config.py
# .parent = src
# .parent.parent = STUDENT MANAGEMENT SYSTEM PROJECT
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATA_DIR = BASE_DIR / "data"
IMPORT_DIR = DATA_DIR / "imports"
EXPORT_DIR = DATA_DIR / "exports"
LOG_DIR = BASE_DIR / "logs"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"

DATABASE_PATH = DATABASE_DIR / "student_management.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "IBS Student Management System",
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development",
)

DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() in {"true", "1", "yes", "on"}


# ============================================================
# SECURITY SETTINGS
# ============================================================

BCRYPT_ROUNDS = int(
    os.getenv(
        "BCRYPT_ROUNDS",
        "12",
    )
)


# ============================================================
# DATABASE SETTINGS
# ============================================================

DATABASE_TIMEOUT = int(
    os.getenv(
        "DATABASE_TIMEOUT",
        "10",
    )
)


# ============================================================
# PAGINATION
# ============================================================

DEFAULT_PAGE_SIZE = int(
    os.getenv(
        "DEFAULT_PAGE_SIZE",
        "10",
    )
)

MAX_PAGE_SIZE = int(
    os.getenv(
        "MAX_PAGE_SIZE",
        "100",
    )
)


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

for directory in (
    DATABASE_DIR,
    DATA_DIR,
    IMPORT_DIR,
    EXPORT_DIR,
    LOG_DIR,
    DOCS_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )