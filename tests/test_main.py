from src.main import main


def test_main_starts_login_view(monkeypatch, capsys):
    """Verify that the main application starts the login process."""

    class FakeUser:
        full_name = "Test User"
        role = "staff"

    class FakeLoginView:
        def display_login(self):
            return FakeUser()

    monkeypatch.setattr(
        "src.main.LoginView",
        FakeLoginView,
    )

    main()

    captured = capsys.readouterr()

    assert "Login session started." in captured.out
    assert "Welcome, Test User!" in captured.out


def test_main_stops_when_login_fails(monkeypatch, capsys):
    """Verify that the application stops when authentication fails."""

    class FakeLoginView:
        def display_login(self):
            return None

    monkeypatch.setattr(
        "src.main.LoginView",
        FakeLoginView,
    )

    main()

    captured = capsys.readouterr()

    assert "Login session started." not in captured.out