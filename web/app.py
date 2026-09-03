from flask import Flask, render_template, request, session, redirect, url_for

from src.controllers.login_controller import LoginController


def create_app() -> Flask:
    """Create and configure the IBS Student Management System web app."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
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

            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.full_name
            session['role'] = user.role

            return redirect(url_for('dashboard'))

        return render_template("login.html")

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('home'))

        return (
            f"<h1>IBS Student Management System</h1>"
            f"<h2>Welcome, {session['full_name']}!</h2>"
            f"<p>Role: {session['role']}</p>"
            f"<a href=\"{url_for('logout')}\">Logout</a>"
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
