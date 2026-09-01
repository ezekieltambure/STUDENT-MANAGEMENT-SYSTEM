from src.views.login_view import LoginView


def main() -> None:
    """Start the IBS Student Management System."""

    login_view = LoginView()
    user = login_view.display_login()

    if user is None:
        return

    print()
    print("=" * 50)
    print("Login session started.")
    print(f"Welcome, {user.full_name}!")
    print("=" * 50)


if __name__ == "__main__":
    main()