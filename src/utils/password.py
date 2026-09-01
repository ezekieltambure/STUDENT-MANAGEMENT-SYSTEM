import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not isinstance(password_hash, str):
        raise TypeError("Password hash must be a string.")

    if not password:
        return False

    if not password_hash:
        return False

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False