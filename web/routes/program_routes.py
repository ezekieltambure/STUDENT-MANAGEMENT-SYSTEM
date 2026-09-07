from flask import Blueprint, redirect, render_template, request, session, url_for

from src.controllers.program_controller import ProgramController
from src.repositories.department_repository import DepartmentRepository
from src.models.program import Program


program_bp = Blueprint(
    "programs",
    __name__,
    url_prefix="/programs",
)

program_controller = ProgramController()
department_repository = DepartmentRepository()


def _require_login():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return None


@program_bp.route("/")
def list_programs():
    """Display all academic programs with optional search."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    query = request.args.get("q", "").strip()

    programs = program_controller.search_programs(query)

    departments = department_repository.list_all()

    department_map = {
        department.id: department
        for department in departments
    }

    return render_template(
        "programs/list.html",
        programs=programs,
        departments=department_map,
        query=query,
    )


@program_bp.route("/new", methods=["GET", "POST"])
def create_program():
    """Create a new academic program."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    departments = department_repository.list_all()
    error = None

    if request.method == "POST":
        code = request.form.get("program_code", "").strip()
        name = request.form.get("program_name", "").strip()
        qualification = request.form.get("qualification", "").strip()
        duration_raw = request.form.get("duration_years", "").strip()
        department_raw = request.form.get("department_id", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Active").strip()

        try:
            if not duration_raw:
                raise ValueError("Duration is required.")

            if not department_raw:
                raise ValueError("Department is required.")

            duration_years = int(duration_raw)
            department_id = int(department_raw)

            program_controller.create_program(
                program_code=code,
                program_name=name,
                qualification=qualification,
                duration_years=duration_years,
                department_id=department_id,
                description=description,
                status=status,
            )

            return redirect(url_for("programs.list_programs"))

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "programs/form.html",
        program=None,
        departments=departments,
        error=error,
    )


@program_bp.route("/<int:program_id>")
def view_program(program_id: int):
    """Display details for a single academic program."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    program = program_controller.get_program(program_id)

    if program is None:
        return redirect(url_for("programs.list_programs"))

    department = department_repository.find_by_id(program.department_id)

    return render_template(
        "programs/detail.html",
        program=program,
        department=department,
    )


@program_bp.route("/<int:program_id>/edit", methods=["GET", "POST"])
def edit_program(program_id: int):
    """Edit an existing academic program."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    program = program_controller.get_program(program_id)

    if program is None:
        return redirect(url_for("programs.list_programs"))

    departments = department_repository.list_all()
    error = None

    if request.method == "POST":
        code = request.form.get("program_code", "").strip()
        name = request.form.get("program_name", "").strip()
        qualification = request.form.get("qualification", "").strip()
        duration_raw = request.form.get("duration_years", "").strip()
        department_raw = request.form.get("department_id", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Active").strip()

        try:
            if not duration_raw:
                raise ValueError("Duration is required.")

            if not department_raw:
                raise ValueError("Department is required.")

            duration_years = int(duration_raw)
            department_id = int(department_raw)

            updated_program = Program(
                id=program.id,
                program_code=code,
                program_name=name,
                qualification=qualification,
                duration_years=duration_years,
                department_id=department_id,
                description=description,
                status=status,
                created_at=program.created_at,
            )

            program_controller.update_program(updated_program)

            return redirect(
                url_for(
                    "programs.view_program",
                    program_id=program.id,
                )
            )

        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "programs/form.html",
        program=program,
        departments=departments,
        error=error,
    )


@program_bp.route("/<int:program_id>/toggle-status", methods=["POST"])
def toggle_program_status(program_id: int):
    """Activate or deactivate an academic program."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    program = program_controller.get_program(program_id)

    if program is None:
        return redirect(url_for("programs.list_programs"))

    program.status = (
        "Inactive"
        if program.status == "Active"
        else "Active"
    )

    try:
        program_controller.update_program(program)
    except (ValueError, TypeError):
        pass

    return redirect(
        url_for(
            "programs.list_programs",
            q=request.args.get("q", ""),
        )
    )


@program_bp.route("/<int:program_id>/delete", methods=["POST"])
def delete_program(program_id: int):
    """Delete an academic program."""

    login_redirect = _require_login()
    if login_redirect:
        return login_redirect

    program = program_controller.get_program(program_id)

    if program is None:
        return redirect(url_for("programs.list_programs"))

    try:
        program_controller.delete_program(program_id)
    except Exception:
        pass

    return redirect(url_for("programs.list_programs"))
