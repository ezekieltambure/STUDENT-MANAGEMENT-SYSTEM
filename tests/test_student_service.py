from copy import deepcopy
from datetime import date

import pytest

from src.models.student import Student
from src.services.student_service import StudentService


class FakeStudentRepository:
    """Fake repository used to test StudentService."""

    def __init__(self):
        self.students = {}
        self.next_id = 1

    def create(self, student):
        student.id = self.next_id
        self.students[self.next_id] = deepcopy(student)
        self.next_id += 1
        return deepcopy(student)

    def find_by_id(self, student_id):
        student = self.students.get(student_id)

        if student is None:
            return None

        return deepcopy(student)

    def find_by_student_number(self, student_number):
        for student in self.students.values():
            if student.student_number == student_number:
                return deepcopy(student)

        return None

    def exists_by_student_number(self, student_number):
        return self.find_by_student_number(student_number) is not None

    def update(self, student):
        self.students[student.id] = deepcopy(student)
        return deepcopy(student)

    def delete(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            return True

        return False


def make_student(student_number="STU001"):
    return Student(
        student_number=student_number,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(2000, 1, 1),
        gender="Male",
        program="Bachelor of Information Technology",
        email="john.doe@example.com",
        phone="70000000",
    )


def test_service_can_create_student():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student = make_student()

    created = service.create_student(student)

    assert created.id == 1
    assert created.student_number == "STU001"


def test_service_rejects_duplicate_student_number():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    service.create_student(make_student())

    with pytest.raises(ValueError, match="Student number already exists"):
        service.create_student(make_student())


def test_service_can_find_student_by_id():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student = service.create_student(make_student())

    found = service.find_by_id(student.id)

    assert found is not None
    assert found.student_number == "STU001"


def test_service_can_find_student_by_number():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    service.create_student(make_student())

    found = service.find_by_student_number("STU001")

    assert found is not None
    assert found.first_name == "John"


def test_service_returns_none_for_empty_student_number():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    assert service.find_by_student_number("   ") is None


def test_service_checks_student_number_exists():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    service.create_student(make_student())

    assert service.exists_by_student_number("STU001") is True
    assert service.exists_by_student_number("STU999") is False


def test_service_can_update_student():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student = service.create_student(make_student())

    student.first_name = "Peter"

    updated = service.update_student(student)

    assert updated.first_name == "Peter"


def test_service_rejects_update_without_id():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student = make_student()

    with pytest.raises(ValueError, match="Student ID is required"):
        service.update_student(student)


def test_service_rejects_duplicate_number_during_update():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student_one = service.create_student(make_student("STU001"))
    service.create_student(make_student("STU002"))

    student_one.student_number = "STU002"

    with pytest.raises(ValueError, match="Student number already exists"):
        service.update_student(student_one)


def test_service_can_delete_student():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    student = service.create_student(make_student())

    assert service.delete_student(student.id) is True
    assert service.find_by_id(student.id) is None


def test_service_returns_false_when_deleting_nonexistent_student():
    repository = FakeStudentRepository()
    service = StudentService(repository)

    assert service.delete_student(999) is False
