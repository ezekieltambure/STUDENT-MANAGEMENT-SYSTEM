from typing import Optional

from src.controllers.report_controller import ReportController
from src.models.report import Report


class ReportView:
    """Terminal-based view for system reports."""

    def __init__(
        self,
        report_controller: Optional[ReportController] = None,
    ) -> None:
        """Initialize the report view."""

        self.report_controller = (
            report_controller or ReportController()
        )

    def display_menu(self) -> None:
        """Display the reports menu."""

        print()
        print("=" * 60)
        print("                 SYSTEM REPORTS")
        print("=" * 60)
        print("1. System Overview")
        print("2. Student Summary")
        print("3. Students by Department")
        print("4. Course Summary")
        print("5. Enrollment Summary")
        print("6. Enrollment by Academic Term")
        print("7. Grade Summary")
        print("8. Student Academic Performance")
        print("9. Exit")
        print("=" * 60)

    def run(self) -> None:
        """Run the interactive reports menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.display_report(
                    self.report_controller.get_system_overview()
                )

            elif choice == "2":
                self.display_report(
                    self.report_controller.get_student_summary()
                )

            elif choice == "3":
                self.display_report(
                    self.report_controller.get_students_by_department()
                )

            elif choice == "4":
                self.display_report(
                    self.report_controller.get_course_summary()
                )

            elif choice == "5":
                self.display_report(
                    self.report_controller.get_enrollment_summary()
                )

            elif choice == "6":
                self.display_report(
                    self.report_controller.get_enrollment_by_term()
                )

            elif choice == "7":
                self.display_report(
                    self.report_controller.get_grade_summary()
                )

            elif choice == "8":
                self.display_report(
                    self.report_controller.get_student_performance()
                )

            elif choice == "9":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    @staticmethod
    def display_report(report: Report) -> None:
        """Display a generated report."""

        print()
        print("=" * 60)
        print(f"                  {report.title.upper()}")
        print("=" * 60)

        if report.generated_at:
            print(f"Generated: {report.generated_at}")

        print(f"Records: {report.row_count}")
        print("-" * 60)

        if report.is_empty():
            print("No data available for this report.")
            print("=" * 60)
            return

        for index, row in enumerate(report.data, start=1):
            print(f"\nRecord {index}")

            for key, value in row.items():
                label = key.replace("_", " ").title()
                print(f"{label}: {value}")

        print()
        print("=" * 60)