from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, session

from src.controllers.student_controller import StudentController
from src.models.student import Student


student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students",
)

student_controller = StudentController()


@student_bp.route("/")
def list_students():
    """Display all students."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    students = student_controller.find_all()

    return render_template(
        "students/list.html",
        students=students,
    )


@student_bp.route("/new", methods=["GET", "POST"])
def create_student():
    """Display and process the add student form."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        student_number = request.form.get(
            "student_number", ""
        ).strip()

        first_name = request.form.get(
            "first_name", ""
        ).strip()

        last_name = request.form.get(
            "last_name", ""
        ).strip()

        date_of_birth_value = request.form.get(
            "date_of_birth", ""
        ).strip()

        gender = request.form.get(
            "gender", ""
        ).strip()

        program = request.form.get(
            "program", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip()

        phone = request.form.get(
            "phone", ""
        ).strip()

        try:
            date_of_birth = date.fromisoformat(
                date_of_birth_value
            )

            student = Student(
                student_number=student_number,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                program=program,
                email=email,
                phone=phone,
            )

            student_controller.create_student(student)

            return redirect(
                url_for("students.list_students")
            )

        except (ValueError, TypeError) as error:
            return render_template(
                "students/form.html",
                error=str(error),
            )

    return render_template(
        "students/form.html"
    )


@student_bp.route("/<int:student_id>")
def view_student(student_id: int):
    """Display detailed information about a student."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    student = student_controller.find_by_id(student_id)

    if student is None:
        return render_template(
            "students/detail.html",
            student=None,
            error="Student not found.",
        ), 404

    return render_template(
        "students/detail.html",
        student=student,
    )