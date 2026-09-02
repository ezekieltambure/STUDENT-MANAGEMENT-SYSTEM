from getpass import getpass

from src.controllers.user_controller import UserController


class UserView:
    """Terminal-based user management interface."""

    def __init__(
        self,
        user_controller: UserController | None = None,
    ) -> None:
        """Initialize the user management view."""

        self.user_controller = user_controller or UserController()

    def display_menu(self) -> None:
        """Display the user management menu."""

        print()
        print("=" * 50)
        print("             USER MANAGEMENT")
        print("=" * 50)
        print("1. Add User")
        print("2. Search User")
        print("3. Update User")
        print("4. Deactivate User")
        print("5. Activate User")
        print("6. Delete User")
        print("7. Exit")
        print("=" * 50)

    def run(self) -> None:
        """Run the interactive user management menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.add_user()

            elif choice == "2":
                self.search_user()

            elif choice == "3":
                self.update_user()

            elif choice == "4":
                self.deactivate_user()

            elif choice == "5":
                self.activate_user()

            elif choice == "6":
                self.delete_user()

            elif choice == "7":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def add_user(self) -> None:
        """Create a new system user."""

        print()
        print("-" * 50)
        print("               ADD USER")
        print("-" * 50)

        username = input("Username: ").strip()
        full_name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        role = input("Role (admin/staff): ").strip().lower()
        password = getpass("Password: ")
        confirm_password = getpass("Confirm Password: ")

        if password != confirm_password:
            print()
            print("Error: Passwords do not match.")
            return

        try:
            user = self.user_controller.create_user(
                username=username,
                password=password,
                role=role,
                full_name=full_name,
                email=email,
            )

            print()
            print("User created successfully.")
            print(f"User ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Role: {user.role}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def search_user(self) -> None:
        """Search for a user by username."""

        print()
        print("-" * 50)
        print("              SEARCH USER")
        print("-" * 50)

        username = input("Username: ").strip()

        user = self.user_controller.get_user_by_username(username)

        if user is None:
            print()
            print("User not found.")
            return

        self._display_user(user)

    def update_user(self) -> None:
        """Update an existing user."""

        print()
        print("-" * 50)
        print("              UPDATE USER")
        print("-" * 50)

        username = input("Username: ").strip()

        user = self.user_controller.get_user_by_username(username)

        if user is None:
            print()
            print("User not found.")
            return

        print()
        print("Press Enter to keep the current value.")

        full_name = input(
            f"Full Name [{user.full_name}]: "
        ).strip()

        email = input(
            f"Email [{user.email}]: "
        ).strip()

        role = input(
            f"Role [{user.role}]: "
        ).strip().lower()

        new_password = getpass(
            "New Password (leave blank to keep current): "
        )

        if full_name:
            user.full_name = full_name

        if email:
            user.email = email

        if role:
            user.role = role

        try:
            updated_user = self.user_controller.update_user(
                user=user,
                password=new_password or None,
            )

            print()
            print("User updated successfully.")
            print(f"Username: {updated_user.username}")
            print(f"Role: {updated_user.role}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def deactivate_user(self) -> None:
        """Deactivate a user account."""

        username = input("Username to deactivate: ").strip()

        user = self.user_controller.get_user_by_username(username)

        if user is None:
            print()
            print("User not found.")
            return

        if not user.is_active:
            print()
            print("User is already inactive.")
            return

        success = self.user_controller.deactivate_user(user.id)

        print()
        if success:
            print("User deactivated successfully.")
        else:
            print("Unable to deactivate user.")

    def activate_user(self) -> None:
        """Activate a user account."""

        username = input("Username to activate: ").strip()

        user = self.user_controller.get_user_by_username(username)

        if user is None:
            print()
            print("User not found.")
            return

        if user.is_active:
            print()
            print("User is already active.")
            return

        success = self.user_controller.activate_user(user.id)

        print()
        if success:
            print("User activated successfully.")
        else:
            print("Unable to activate user.")

    def delete_user(self) -> None:
        """Delete a user account."""

        username = input("Username to delete: ").strip()

        user = self.user_controller.get_user_by_username(username)

        if user is None:
            print()
            print("User not found.")
            return

        confirmation = input(
            f"Are you sure you want to delete '{username}'? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print()
            print("Deletion cancelled.")
            return

        success = self.user_controller.delete_user(user.id)

        print()
        if success:
            print("User deleted successfully.")
        else:
            print("Unable to delete user.")

    @staticmethod
    def _display_user(user) -> None:
        """Display user information."""

        print()
        print("=" * 50)
        print("               USER DETAILS")
        print("=" * 50)
        print(f"User ID:        {user.id}")
        print(f"Username:       {user.username}")
        print(f"Full Name:      {user.full_name}")
        print(f"Email:          {user.email}")
        print(f"Role:           {user.role}")
        print(
            f"Status:         "
            f"{'Active' if user.is_active else 'Inactive'}"
        )
        print("=" * 50)
