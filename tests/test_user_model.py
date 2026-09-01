import pytest

from src.models.user import User


def test_user_can_be_created() -> None:
    user = User(
        username="admin",
        password_hash="hashed_password",
        role="admin",
        full_name="System Administrator",
        email="admin@example.com",
    )

    assert user.username == "admin"
    assert user.role == "admin"
    assert user.full_name == "System Administrator"
    assert user.email == "admin@example.com"
    assert user.is_active is True


def test_admin_role() -> None:
    user = User(
        username="admin",
        password_hash="hashed_password",
        role="admin",
    )

    assert user.is_admin() is True
    assert user.is_staff() is False


def test_staff_role() -> None:
    user = User(
        username="staff01",
        password_hash="hashed_password",
        role="staff",
    )

    assert user.is_staff() is True
    assert user.is_admin() is False


def test_invalid_role_is_rejected() -> None:
    with pytest.raises(ValueError, match="Invalid role"):
        User(
            username="testuser",
            password_hash="hashed_password",
            role="student",
        )


def test_empty_username_is_rejected() -> None:
    with pytest.raises(ValueError, match="Username cannot be empty"):
        User(
            username="",
            password_hash="hashed_password",
            role="staff",
        )


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValueError, match="Invalid email address"):
        User(
            username="staff01",
            password_hash="hashed_password",
            role="staff",
            email="invalid-email",
        )


def test_user_can_be_deactivated() -> None:
    user = User(
        username="staff01",
        password_hash="hashed_password",
        role="staff",
    )

    user.deactivate()

    assert user.is_active is False


def test_user_can_be_activated() -> None:
    user = User(
        username="staff01",
        password_hash="hashed_password",
        role="staff",
        is_active=False,
    )

    user.activate()

    assert user.is_active is True


def test_user_string_representation() -> None:
    user = User(
        username="admin",
        password_hash="hashed_password",
        role="admin",
    )

    assert str(user) == "admin (admin)"