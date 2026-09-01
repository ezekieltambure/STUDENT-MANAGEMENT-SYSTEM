from datetime import date

import pytest

from src.models.student import Student
from src.repositories.student_repository import StudentRepository


@pytest.fixture
def repository() -> StudentRepository:
    return StudentRepository()


@pytest.fixture
def student() -> Student:
    return Student(
        student_number="STUDENT_REPOSITORY_TEST",
        first_name="Repository",
        last_name="Student",
        date_of_birth=date(2000, 1, 1),
        gender="Male",
        program="Bachelor of Information Technology",
        email="student.repository@example.com",
        phone="70000010",
        is_active=True,
    )


@pytest.fixture(autouse=True)
def clean_test_student() -> None:
    """Remove the test student before and after every test."""

    repository = StudentRepository()

    existing_student = repository.find_by_student_number(
        "STUDENT_REPOSITORY_TEST"
    )

    if existing_student is not None:
        repository.delete(existing_student.id)

    yield

    existing_student = repository.find_by_student_number(
        "STUDENT_REPOSITORY_TEST"
    )

    if existing_student is not None:
        repository.delete(existing_student.id)


def test_create_student(
    repository: StudentRepository,
    student: Student,
) -> None:
    created_student = repository.create(student)

    assert created_student.id is not None
    assert created_student.student_number == "STUDENT_REPOSITORY_TEST"


def test_find_student_by_id(
    repository: StudentRepository,
    student: Student,
) -> None:
    created_student = repository.create(student)

    found_student = repository.find_by_id(created_student.id)

    assert found_student is not None
    assert found_student.id == created_student.id
    assert found_student.student_number == created_student.student_number


def test_find_student_by_student_number(
    repository: StudentRepository,
    student: Student,
) -> None:
    repository.create(student)

    found_student = repository.find_by_student_number(
        "STUDENT_REPOSITORY_TEST"
    )

    assert found_student is not None
    assert found_student.student_number == "STUDENT_REPOSITORY_TEST"


def test_find_nonexistent_student(
    repository: StudentRepository,
) -> None:
    found_student = repository.find_by_student_number(
        "DOES_NOT_EXIST"
    )

    assert found_student is None


def test_exists_by_student_number(
    repository: StudentRepository,
    student: Student,
) -> None:
    assert repository.exists_by_student_number(
        "STUDENT_REPOSITORY_TEST"
    ) is False

    repository.create(student)

    assert repository.exists_by_student_number(
        "STUDENT_REPOSITORY_TEST"
    ) is True


def test_update_student(
    repository: StudentRepository,
    student: Student,
) -> None:
    created_student = repository.create(student)

    created_student.first_name = "Updated"
    created_student.email = "updated.student@example.com"

    updated_student = repository.update(created_student)

    assert updated_student.first_name == "Updated"
    assert updated_student.email == "updated.student@example.com"

    found_student = repository.find_by_id(created_student.id)

    assert found_student is not None
    assert found_student.first_name == "Updated"
    assert found_student.email == "updated.student@example.com"


def test_update_student_without_id(
    repository: StudentRepository,
    student: Student,
) -> None:
    with pytest.raises(ValueError):
        repository.update(student)


def test_delete_student(
    repository: StudentRepository,
    student: Student,
) -> None:
    created_student = repository.create(student)

    deleted = repository.delete(created_student.id)

    assert deleted is True
    assert repository.find_by_id(created_student.id) is None


def test_delete_nonexistent_student(
    repository: StudentRepository,
) -> None:
    deleted = repository.delete(999999)

    assert deleted is False