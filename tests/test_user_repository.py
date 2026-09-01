import pytest

from src.models.user import User
from src.repositories.user_repository import UserRepository


@pytest.fixture
def repository() -> UserRepository:
    return UserRepository()


@pytest.fixture
def user() -> User:
    return User(
        username="repository_test_user",
        password_hash="hashed_password",
        role="staff",
        full_name="Repository Test User",
        email="repository@example.com",
        is_active=True,
    )


@pytest.fixture(autouse=True)
def clean_test_user():
    """Remove the test user before and after every test."""

    repository = UserRepository()

    existing_user = repository.find_by_username("repository_test_user")

    if existing_user is not None:
        repository.delete(existing_user.id)

    yield

    existing_user = repository.find_by_username("repository_test_user")

    if existing_user is not None:
        repository.delete(existing_user.id)


def test_create_user(
    repository: UserRepository,
    user: User,
) -> None:
    created_user = repository.create(user)

    assert created_user.id is not None
    assert created_user.username == "repository_test_user"


def test_find_user_by_id(
    repository: UserRepository,
    user: User,
) -> None:
    created_user = repository.create(user)

    found_user = repository.find_by_id(created_user.id)

    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == created_user.username


def test_find_user_by_username(
    repository: UserRepository,
    user: User,
) -> None:
    repository.create(user)

    found_user = repository.find_by_username("repository_test_user")

    assert found_user is not None
    assert found_user.username == "repository_test_user"


def test_find_nonexistent_user(
    repository: UserRepository,
) -> None:
    found_user = repository.find_by_username("does_not_exist")

    assert found_user is None


def test_exists_by_username(
    repository: UserRepository,
    user: User,
) -> None:
    assert repository.exists_by_username("repository_test_user") is False

    repository.create(user)

    assert repository.exists_by_username("repository_test_user") is True


def test_update_user(
    repository: UserRepository,
    user: User,
) -> None:
    created_user = repository.create(user)

    created_user.full_name = "Updated Test User"
    created_user.email = "updated@example.com"

    updated_user = repository.update(created_user)

    assert updated_user.full_name == "Updated Test User"
    assert updated_user.email == "updated@example.com"

    found_user = repository.find_by_id(created_user.id)

    assert found_user is not None
    assert found_user.full_name == "Updated Test User"
    assert found_user.email == "updated@example.com"


def test_update_user_without_id(
    repository: UserRepository,
    user: User,
) -> None:
    with pytest.raises(ValueError):
        repository.update(user)


def test_delete_user(
    repository: UserRepository,
    user: User,
) -> None:
    created_user = repository.create(user)

    deleted = repository.delete(created_user.id)

    assert deleted is True
    assert repository.find_by_id(created_user.id) is None


def test_delete_nonexistent_user(
    repository: UserRepository,
) -> None:
    deleted = repository.delete(999999)

    assert deleted is False

