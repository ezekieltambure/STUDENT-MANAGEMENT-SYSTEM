import pytest

from src.utils.password import hash_password, verify_password


def test_password_can_be_hashed() -> None:
    password_hash = hash_password("SecurePassword123")

    assert password_hash != "SecurePassword123"
    assert password_hash.startswith("$2")


def test_correct_password_is_verified() -> None:
    password_hash = hash_password("SecurePassword123")

    assert verify_password("SecurePassword123", password_hash) is True


def test_incorrect_password_is_rejected() -> None:
    password_hash = hash_password("SecurePassword123")

    assert verify_password("WrongPassword123", password_hash) is False


def test_same_password_generates_different_hashes() -> None:
    first_hash = hash_password("SecurePassword123")
    second_hash = hash_password("SecurePassword123")

    assert first_hash != second_hash


def test_empty_password_is_rejected_when_hashing() -> None:
    with pytest.raises(ValueError):
        hash_password("")


def test_non_string_password_is_rejected_when_hashing() -> None:
    with pytest.raises(TypeError):
        hash_password(123)  # type: ignore[arg-type]


def test_empty_password_fails_verification() -> None:
    password_hash = hash_password("SecurePassword123")

    assert verify_password("", password_hash) is False