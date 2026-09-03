from flask import Flask, render_template, request

from src.controllers.login_controller import LoginController


def create_app() -> Flask:
    """Create and configure the IBS Student Management System web app."""

    app = Flask(__name__)
    login_controller = LoginController()

    @app.route("/", methods=["GET", "POST"])
    def home():
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

            return (
                f"Login successful. Welcome, {user.full_name}! "
                f"Role: {user.role}"
            )

        return render_template("login.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
