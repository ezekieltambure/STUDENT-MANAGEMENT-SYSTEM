import pytest

from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthenticationService
from src.utils.password import hash_password


@pytest.fixture
def repository() -> UserRepository:
    return UserRepository()


@pytest.fixture
def service(repository: UserRepository) -> AuthenticationService:
    return AuthenticationService(repository)


@pytest.fixture
def test_user() -> User:
    return User(
        username="auth_test_user",
        password_hash=hash_password("SecurePassword123"),
        role="staff",
        full_name="Authentication Test User",
        email="auth@example.com",
        is_active=True,
    )


@pytest.fixture(autouse=True)
def clean_test_user():
    """Remove the authentication test user before and after every test."""

    repository = UserRepository()

    existing_user = repository.find_by_username("auth_test_user")

    if existing_user is not None:
        repository.delete(existing_user.id)

    yield

    existing_user = repository.find_by_username("auth_test_user")

    if existing_user is not None:
        repository.delete(existing_user.id)


def test_valid_credentials_authenticate_user(
    repository: UserRepository,
    service: AuthenticationService,
    test_user: User,
) -> None:
    repository.create(test_user)

    authenticated_user = service.authenticate(
        "auth_test_user",
        "SecurePassword123",
    )

    assert authenticated_user is not None
    assert authenticated_user.username == "auth_test_user"


def test_wrong_password_is_rejected(
    repository: UserRepository,
    service: AuthenticationService,
    test_user: User,
) -> None:
    repository.create(test_user)

    authenticated_user = service.authenticate(
        "auth_test_user",
        "WrongPassword123",
    )

    assert authenticated_user is None


def test_nonexistent_user_is_rejected(
    service: AuthenticationService,
) -> None:
    authenticated_user = service.authenticate(
        "does_not_exist",
        "SecurePassword123",
    )

    assert authenticated_user is None


def test_inactive_user_is_rejected(
    repository: UserRepository,
    service: AuthenticationService,
    test_user: User,
) -> None:
    test_user.is_active = False
    repository.create(test_user)

    authenticated_user = service.authenticate(
        "auth_test_user",
        "SecurePassword123",
    )

    assert authenticated_user is None


def test_empty_username_is_rejected(
    service: AuthenticationService,
) -> None:
    authenticated_user = service.authenticate(
        "",
        "SecurePassword123",
    )

    assert authenticated_user is None


def test_empty_password_is_rejected(
    repository: UserRepository,
    service: AuthenticationService,
    test_user: User,
) -> None:
    repository.create(test_user)

    authenticated_user = service.authenticate(
        "auth_test_user",
        "",
    )

    assert authenticated_user is None