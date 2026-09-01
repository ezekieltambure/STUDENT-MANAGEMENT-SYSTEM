from datetime import date

from src.controllers.student_controller import StudentController
from src.models.student import Student


class FakeStudentService:
    """Fake service used to test StudentController."""

    def __init__(self):
        self.students = {}
        self.next_id = 1

    def create_student(self, student):
        student.id = self.next_id
        self.students[self.next_id] = student
        self.next_id += 1
        return student

    def find_by_id(self, student_id):
        return self.students.get(student_id)

    def find_by_student_number(self, student_number):
        for student in self.students.values():
            if student.student_number == student_number:
                return student
        return None

    def exists_by_student_number(self, student_number):
        return any(
            student.student_number == student_number
            for student in self.students.values()
        )

    def update_student(self, student):
        self.students[student.id] = student
        return student

    def delete_student(self, student_id):
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


def test_controller_can_create_student():
    service = FakeStudentService()
    controller = StudentController(service)

    student = controller.create_student(make_student())

    assert student.id == 1
    assert student.student_number == "STU001"


def test_controller_can_find_student_by_id():
    service = FakeStudentService()
    controller = StudentController(service)

    created = controller.create_student(make_student())

    found = controller.find_by_id(created.id)

    assert found is not None
    assert found.student_number == "STU001"


def test_controller_can_find_student_by_number():
    service = FakeStudentService()
    controller = StudentController(service)

    controller.create_student(make_student())

    found = controller.find_by_student_number("STU001")

    assert found is not None
    assert found.first_name == "John"


def test_controller_can_check_student_number_exists():
    service = FakeStudentService()
    controller = StudentController(service)

    controller.create_student(make_student())

    assert controller.exists_by_student_number("STU001") is True
    assert controller.exists_by_student_number("STU999") is False


def test_controller_can_update_student():
    service = FakeStudentService()
    controller = StudentController(service)

    student = controller.create_student(make_student())
    student.first_name = "Peter"

    updated = controller.update_student(student)

    assert updated.first_name == "Peter"


def test_controller_can_delete_student():
    service = FakeStudentService()
    controller = StudentController(service)

    student = controller.create_student(make_student())

    assert controller.delete_student(student.id) is True
    assert controller.find_by_id(student.id) is None


def test_controller_returns_false_for_nonexistent_delete():
    service = FakeStudentService()
    controller = StudentController(service)

    assert controller.delete_student(999) is False
