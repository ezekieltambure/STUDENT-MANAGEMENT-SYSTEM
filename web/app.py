from flask import Flask, redirect, render_template, request, session, url_for

from src.controllers.login_controller import LoginController
from src.controllers.student_controller import StudentController
from src.controllers.department_controller import DepartmentController
from src.controllers.program_controller import ProgramController
from src.controllers.course_controller import CourseController
from src.controllers.academic_term_controller import AcademicTermController

from web.routes.student_routes import student_bp
from web.routes.department_routes import department_bp
from web.routes.program_routes import program_bp
from web.routes.course_routes import course_bp
from web.routes.academic_term_routes import academic_term_bp


app = Flask(__name__)

app.secret_key = "ibs-sms-development-secret-key"


auth_controller = LoginController()


@app.route("/", methods=["GET", "POST"])
def home():
    """Display the login page and process user authentication."""

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get(
            "username",
            "",
        ).strip()

        password = request.form.get(
            "password",
            "",
        )

        try:
            user = auth_controller.login(
                username=username,
                password=password,
            )

            if user is None:
                return render_template(
                    "login.html",
                    error="Invalid username or password.",
                )

            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            session["role"] = user.role

            return redirect(url_for("dashboard"))

        except (ValueError, TypeError) as exc:
            return render_template(
                "login.html",
                error=str(exc),
            )

    return render_template(
        "login.html",
        error=None,
    )


@app.route("/dashboard")
def dashboard():
    """Display the authenticated user's dashboard."""

    if "user_id" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard/dashboard.html",
        full_name=session.get("full_name"),
        role=session.get("role"),
    )


@app.route("/logout")
def logout():
    """Log the current user out."""

    session.clear()

    return redirect(url_for("home"))


app.register_blueprint(student_bp)
app.register_blueprint(department_bp)
app.register_blueprint(program_bp)
app.register_blueprint(course_bp)
app.register_blueprint(academic_term_bp)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
