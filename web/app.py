from flask import Flask, render_template, request, session, redirect, url_for

from src.controllers.login_controller import LoginController
from src.controllers.dashboard_controller import DashboardController
from src.models.user import User

from web.routes.student_routes import student_bp


def create_app() -> Flask:
    """Create and configure the IBS Student Management System web app."""

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"

    # Register application blueprints
    app.register_blueprint(student_bp)

    # Initialize application controllers
    login_controller = LoginController()
    dashboard_controller = DashboardController()

    @app.route("/", methods=["GET", "POST"])
    def home():
        """Display the login page and process authentication."""

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            user = login_controller.login(
                username=username,
                password=password,
            )

            if user is None:
                return render_template(
                    "login.html",
                    error="Invalid username or password.",
                )

            # Store authenticated user information in the session.
            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            session["role"] = user.role

            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        """Log the current user out of the system."""

        session.clear()

        return redirect(url_for("home"))

    @app.route("/dashboard")
    def dashboard():
        """Display the role-based dashboard."""

        if "user_id" not in session:
            return redirect(url_for("home"))

        user = User(
            id=session["user_id"],
            username=session["username"],
            full_name=session["full_name"],
            role=session["role"],
        )

        dashboard_type = dashboard_controller.get_dashboard(user)

        return render_template(
            "dashboard/dashboard.html",
            dashboard_type=dashboard_type,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )