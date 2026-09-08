from flask import Blueprint, redirect, render_template, request, session, url_for

from src.controllers.course_controller import CourseController
from src.models.course import Course
from src.repositories.department_repository import DepartmentRepository


course_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/courses",
)

course_controller = CourseController()
department_repository = DepartmentRepository()


def _require_login():
    if "user_id" not in session:
        return redirect(url_for("home"))
    return None


@course_bp.route("/")
def list_courses():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    query = request.args.get("q", "").strip()

    if query:
        courses = course_controller.search_courses(query)
    else:
        courses = course_controller.get_all_courses()

    departments = department_repository.list_all()
    department_map = {
        department.id: department
        for department in departments
    }

    return render_template(
        "courses/list.html",
        courses=courses,
        departments=department_map,
        query=query,
    )


@course_bp.route("/new", methods=["GET", "POST"])
def create_course():
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    departments = department_repository.list_all()

    if request.method == "POST":
        course_code = request.form.get("course_code", "").strip()
        course_name = request.form.get("course_name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            credit_hours = int(
                request.form.get("credit_hours", "").strip()
            )
            department_id = int(
                request.form.get("department_id", "").strip()
            )

            course = course_controller.create_course(
                course_code=course_code,
                course_name=course_name,
                credit_hours=credit_hours,
                department_id=department_id,
                description=description,
            )

            return redirect(
                url_for(
                    "courses.view_course",
                    course_id=course.id,
                )
            )

        except (ValueError, TypeError) as exc:
            return render_template(
                "courses/form.html",
                course=None,
                departments=departments,
                error=str(exc),
            )

    return render_template(
        "courses/form.html",
        course=None,
        departments=departments,
        error=None,
    )


@course_bp.route("/<int:course_id>")
def view_course(course_id):
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    course = course_controller.get_course(course_id)

    if course is None:
        return "Course not found", 404

    department = department_repository.find_by_id(
        course.department_id
    )

    return render_template(
        "courses/detail.html",
        course=course,
        department=department,
    )


@course_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
def edit_course(course_id):
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    course = course_controller.get_course(course_id)

    if course is None:
        return "Course not found", 404

    departments = department_repository.list_all()

    if request.method == "POST":
        course_code = request.form.get("course_code", "").strip()
        course_name = request.form.get("course_name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            credit_hours = int(
                request.form.get("credit_hours", "").strip()
            )
            department_id = int(
                request.form.get("department_id", "").strip()
            )

            updated_course = Course(
                id=course.id,
                course_code=course_code,
                course_name=course_name,
                credit_hours=credit_hours,
                department_id=department_id,
                description=description,
            )

            course_controller.update_course(updated_course)

            return redirect(
                url_for(
                    "courses.view_course",
                    course_id=course.id,
                )
            )

        except (ValueError, TypeError) as exc:
            return render_template(
                "courses/form.html",
                course=course,
                departments=departments,
                error=str(exc),
            )

    return render_template(
        "courses/form.html",
        course=course,
        departments=departments,
        error=None,
    )


@course_bp.route("/<int:course_id>/delete", methods=["POST"])
def delete_course(course_id):
    redirect_response = _require_login()
    if redirect_response:
        return redirect_response

    try:
        course_controller.delete_course(course_id)
    except ValueError as exc:
        return str(exc), 400

    return redirect(url_for("courses.list_courses"))
