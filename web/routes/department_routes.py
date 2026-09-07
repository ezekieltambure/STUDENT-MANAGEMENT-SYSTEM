from flask import Blueprint, redirect, render_template, request, session, url_for

from src.controllers.department_controller import DepartmentController
from src.models.department import Department


department_bp = Blueprint(
    "departments",
    __name__,
    url_prefix="/departments",
)

department_controller = DepartmentController()


def _require_login():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return None


@department_bp.route("/")
def list_departments():
    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    departments = department_controller.get_all_departments()

    query = request.args.get("q", "").strip().lower()

    if query:
        departments = [
            department
            for department in departments
            if (
                query in department.department_code.lower()
                or query in department.department_name.lower()
                or query in department.description.lower()
            )
        ]

    return render_template(
        "departments/list.html",
        departments=departments,
        query=request.args.get("q", "").strip(),
    )


@department_bp.route("/new", methods=["GET", "POST"])
def create_department():
    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    error = None

    if request.method == "POST":
        code = request.form.get("department_code", "").strip()
        name = request.form.get("department_name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            department_controller.create_department(
                department_code=code,
                department_name=name,
                description=description,
            )

            return redirect(url_for("departments.list_departments"))

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "departments/form.html",
        department=None,
        error=error,
    )


@department_bp.route("/<int:department_id>")
def view_department(department_id: int):
    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    department = department_controller.get_department(department_id)

    if department is None:
        return redirect(url_for("departments.list_departments"))

    return render_template(
        "departments/detail.html",
        department=department,
    )


@department_bp.route("/<int:department_id>/edit", methods=["GET", "POST"])
def edit_department(department_id: int):
    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    department = department_controller.get_department(department_id)

    if department is None:
        return redirect(url_for("departments.list_departments"))

    error = None

    if request.method == "POST":
        code = request.form.get("department_code", "").strip()
        name = request.form.get("department_name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            department.department_code = code.upper()
            department.department_name = name
            department.description = description

            department_controller.update_department(department)

            return redirect(
                url_for(
                    "departments.view_department",
                    department_id=department.id,
                )
            )

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "departments/form.html",
        department=department,
        error=error,
    )


@department_bp.route("/<int:department_id>/delete", methods=["POST"])
def delete_department(department_id: int):
    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    department = department_controller.get_department(department_id)

    if department is None:
        return redirect(url_for("departments.list_departments"))

    try:
        department_controller.delete_department(department_id)
    except Exception:
        pass

    return redirect(url_for("departments.list_departments"))
