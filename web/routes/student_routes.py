from datetime import date

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from src.controllers.student_controller import StudentController
from src.models.student import Student


student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students",
)

student_controller = StudentController()


def _require_login():
    """Redirect unauthenticated users to the login page."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    return None


@student_bp.route("/")
def list_students():
    """Display students with optional search and status filtering."""

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

    search_term = request.args.get(
        "q",
        "",
    ).strip()

    status = request.args.get(
        "status",
        "",
    ).strip()

    if status not in {
        "Active",
        "Inactive",
    }:
        status = ""

    students = student_controller.search_students(
        search_term=search_term,
        status=status or None,
    )

    return render_template(
        "students/list.html",
        students=students,
        search_term=search_term,
        status=status,
    )


@student_bp.route("/new", methods=["GET", "POST"])
def create_student():
    """Display and process the add student form."""

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

    if request.method == "POST":
        student_number = request.form.get(
            "student_number",
            "",
        ).strip()

        first_name = request.form.get(
            "first_name",
            "",
        ).strip()

        last_name = request.form.get(
            "last_name",
            "",
        ).strip()

        date_of_birth_value = request.form.get(
            "date_of_birth",
            "",
        ).strip()

        gender = request.form.get(
            "gender",
            "",
        ).strip()

        program = request.form.get(
            "program",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip()

        phone = request.form.get(
            "phone",
            "",
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

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

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


@student_bp.route(
    "/<int:student_id>/edit",
    methods=["GET", "POST"],
)
def edit_student(student_id: int):
    """Display and process the edit student form."""

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

    student = student_controller.find_by_id(student_id)

    if student is None:
        return render_template(
            "students/detail.html",
            student=None,
            error="Student not found.",
        ), 404

    if request.method == "POST":
        student_number = request.form.get(
            "student_number",
            "",
        ).strip()

        first_name = request.form.get(
            "first_name",
            "",
        ).strip()

        last_name = request.form.get(
            "last_name",
            "",
        ).strip()

        date_of_birth_value = request.form.get(
            "date_of_birth",
            "",
        ).strip()

        gender = request.form.get(
            "gender",
            "",
        ).strip()

        program = request.form.get(
            "program",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip()

        phone = request.form.get(
            "phone",
            "",
        ).strip()

        status = request.form.get(
            "status",
            "",
        ).strip()

        try:
            date_of_birth = date.fromisoformat(
                date_of_birth_value
            )

            updated_student = Student(
                id=student.id,
                student_number=student_number,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                program=program,
                email=email,
                phone=phone,
                is_active=status == "Active",
            )

            student_controller.update_student(
                updated_student
            )

            return redirect(
                url_for(
                    "students.view_student",
                    student_id=student.id,
                )
            )

        except (ValueError, TypeError) as error:
            return render_template(
                "students/edit.html",
                student=student,
                error=str(error),
            )

    return render_template(
        "students/edit.html",
        student=student,
    )


@student_bp.route(
    "/<int:student_id>/deactivate",
    methods=["POST"],
)
def deactivate_student(student_id: int):
    """Deactivate a student."""

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

    try:
        student_controller.deactivate_student(
            student_id
        )

        return redirect(
            url_for(
                "students.view_student",
                student_id=student_id,
            )
        )

    except ValueError as error:
        return render_template(
            "students/detail.html",
            student=None,
            error=str(error),
        ), 404


@student_bp.route(
    "/<int:student_id>/activate",
    methods=["POST"],
)
def activate_student(student_id: int):
    """Activate a student."""

    login_redirect = _require_login()

    if login_redirect:
        return login_redirect

    try:
        student_controller.activate_student(
            student_id
        )

        return redirect(
            url_for(
                "students.view_student",
                student_id=student_id,
            )
        )

    except ValueError as error:
        return render_template(
            "students/detail.html",
            student=None,
            error=str(error),
        ), 404