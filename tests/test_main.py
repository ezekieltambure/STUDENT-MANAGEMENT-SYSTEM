from src.main import main


def test_main_starts_login_view(monkeypatch, capsys):
    """Verify that the main application starts login and dashboard."""

    class FakeUser:
        full_name = "Test User"
        role = "staff"

    class FakeLoginView:
        def display_login(self):
            return FakeUser()

    class FakeDashboardView:
        def run(self, user):
            print(f"Dashboard started for {user.full_name}")

    monkeypatch.setattr(
        "src.main.LoginView",
        FakeLoginView,
    )

    monkeypatch.setattr(
        "src.main.DashboardView",
        FakeDashboardView,
    )

    main()

    captured = capsys.readouterr()

    assert "Dashboard started for Test User" in captured.out


def test_main_stops_when_login_fails(monkeypatch, capsys):
    """Verify that the application stops when login fails."""

    class FakeLoginView:
        def display_login(self):
            return None

    class FakeDashboardView:
        def run(self, user):
            print("Dashboard should not start")

    monkeypatch.setattr(
        "src.main.LoginView",
        FakeLoginView,
    )

    monkeypatch.setattr(
        "src.main.DashboardView",
        FakeDashboardView,
    )

    main()

    captured = capsys.readouterr()

    assert "Dashboard should not start" not in captured.out
