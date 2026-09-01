from datetime import date

from src.models.student import Student
from src.views.student_view import StudentView


class FakeStudentController:
    """Fake controller used to test StudentView."""

    def __init__(self):
        self.students = {}
        self.next_id = 1

    def create_student(self, student):
        student.id = self.next_id
        self.students[self.next_id] = student
        self.next_id += 1
        return student

    def find_by_student_number(self, student_number):
        for student in self.students.values():
            if student.student_number == student_number:
                return student
        return None

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


def test_student_view_can_display_menu(capsys):
    view = StudentView(FakeStudentController())

    view.display_menu()

    output = capsys.readouterr().out

    assert "STUDENT MANAGEMENT" in output
    assert "1. Add Student" in output
    assert "2. Search Student" in output
    assert "3. Update Student" in output
    assert "4. Delete Student" in output
    assert "5. Exit" in output


def test_student_view_can_display_student(capsys):
    student = make_student()

    StudentView.display_student(student)

    output = capsys.readouterr().out

    assert "STUDENT DETAILS" in output
    assert "STU001" in output
    assert "John Doe" in output
    assert "Bachelor of Information Technology" in output
    assert "john.doe@example.com" in output
    assert "Active" in output


def test_student_view_can_add_student(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    inputs = iter([
        "STU001",
        "John",
        "Doe",
        "2000-01-01",
        "Male",
        "Bachelor of Information Technology",
        "john.doe@example.com",
        "70000000",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    student = view.add_student()

    assert student is not None
    assert student.id == 1
    assert student.student_number == "STU001"

    output = capsys.readouterr().out

    assert "Student created successfully." in output


def test_student_view_rejects_invalid_date(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    inputs = iter([
        "STU001",
        "John",
        "Doe",
        "invalid-date",
        "Male",
        "Bachelor of Information Technology",
        "john.doe@example.com",
        "70000000",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    student = view.add_student()

    assert student is None

    output = capsys.readouterr().out

    assert "Unable to create student" in output


def test_student_view_can_search_student(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    controller.create_student(make_student())

    monkeypatch.setattr("builtins.input", lambda _: "STU001")

    student = view.search_student()

    assert student is not None
    assert student.student_number == "STU001"

    output = capsys.readouterr().out

    assert "STUDENT DETAILS" in output
    assert "John Doe" in output


def test_student_view_reports_student_not_found(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    monkeypatch.setattr("builtins.input", lambda _: "STU999")

    student = view.search_student()

    assert student is None

    output = capsys.readouterr().out

    assert "Student not found." in output


def test_student_view_can_delete_student(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    student = controller.create_student(make_student())

    monkeypatch.setattr("builtins.input", lambda _: str(student.id))

    deleted = view.delete_student()

    assert deleted is True
    assert controller.find_by_student_number("STU001") is None

    output = capsys.readouterr().out

    assert "Student deleted successfully." in output


def test_student_view_rejects_invalid_student_id(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    monkeypatch.setattr("builtins.input", lambda _: "invalid")

    deleted = view.delete_student()

    assert deleted is False

    output = capsys.readouterr().out

    assert "Invalid student ID." in output


def test_student_view_reports_missing_student_on_delete(monkeypatch, capsys):
    controller = FakeStudentController()
    view = StudentView(controller)

    monkeypatch.setattr("builtins.input", lambda _: "999")

    deleted = view.delete_student()

    assert deleted is False

    output = capsys.readouterr().out

    assert "Student not found." in output
