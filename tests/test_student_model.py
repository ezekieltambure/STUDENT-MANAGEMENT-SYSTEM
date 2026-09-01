from datetime import date

import pytest

from src.models.student import Student


@pytest.fixture
def student() -> Student:
    return Student(
        student_number="ST250282",
        first_name="Joseph",
        last_name="Ezekiel",
        date_of_birth=date(2000, 1, 1),
        gender="Male",
        program="Bachelor of Information Technology",
        email="joseph@example.com",
        phone="70000000",
    )


def test_student_can_be_created(student: Student) -> None:
    assert student.student_number == "ST250282"
    assert student.first_name == "Joseph"
    assert student.last_name == "Ezekiel"
    assert student.program == "Bachelor of Information Technology"
    assert student.is_active is True


def test_student_full_name(student: Student) -> None:
    assert student.full_name == "Joseph Ezekiel"


def test_student_male_gender(student: Student) -> None:
    assert student.gender == "Male"


def test_student_female_gender() -> None:
    student = Student(
        student_number="ST250283",
        first_name="Mary",
        last_name="John",
        date_of_birth=date(2001, 2, 2),
        gender="Female",
        program="Bachelor of Information Technology",
        email="mary@example.com",
        phone="70000001",
    )

    assert student.gender == "Female"


def test_invalid_gender_is_rejected() -> None:
    with pytest.raises(ValueError):
        Student(
            student_number="ST250284",
            first_name="Test",
            last_name="Student",
            date_of_birth=date(2000, 1, 1),
            gender="Invalid",
            program="Bachelor of Information Technology",
            email="test@example.com",
            phone="70000002",
        )


def test_empty_student_number_is_rejected() -> None:
    with pytest.raises(ValueError):
        Student(
            student_number="",
            first_name="Test",
            last_name="Student",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            program="Bachelor of Information Technology",
            email="test@example.com",
            phone="70000003",
        )


def test_invalid_email_is_rejected() -> None:
    with pytest.raises(ValueError):
        Student(
            student_number="ST250285",
            first_name="Test",
            last_name="Student",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            program="Bachelor of Information Technology",
            email="invalid-email",
            phone="70000004",
        )


def test_student_can_be_deactivated(student: Student) -> None:
    student.deactivate()

    assert student.is_active is False


def test_student_can_be_activated(student: Student) -> None:
    student.deactivate()
    student.activate()

    assert student.is_active is True


def test_student_string_representation(student: Student) -> None:
    assert str(student) == "ST250282 - Joseph Ezekiel"