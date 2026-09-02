from datetime import datetime
from typing import Any, Callable

from src.models.report import Report
from src.repositories.report_repository import ReportRepository


class ReportService:
    """Service layer for generating system reports."""

    def __init__(
        self,
        report_repository: ReportRepository | None = None,
    ) -> None:
        """Initialize the report service."""

        self.report_repository = (
            report_repository or ReportRepository()
        )

    def _create_report(
        self,
        report_type: str,
        title: str,
        generator: Callable[[], list[dict[str, Any]]],
    ) -> Report:
        """Generate and return a Report object."""

        data = generator()

        return Report(
            report_type=report_type,
            title=title,
            data=data,
            generated_at=datetime.now().isoformat(
                timespec="seconds"
            ),
        )

    def get_student_summary(self) -> Report:
        """Generate the student summary report."""

        return self._create_report(
            "student_summary",
            "Student Summary Report",
            self.report_repository.student_summary,
        )

    def get_students_by_department(self) -> Report:
        """Generate the students-by-department report."""

        return self._create_report(
            "students_by_department",
            "Students by Department Report",
            self.report_repository.students_by_department,
        )

    def get_course_summary(self) -> Report:
        """Generate the course summary report."""

        return self._create_report(
            "course_summary",
            "Course Summary Report",
            self.report_repository.course_summary,
        )

    def get_enrollment_summary(self) -> Report:
        """Generate the enrollment summary report."""

        return self._create_report(
            "enrollment_summary",
            "Enrollment Summary Report",
            self.report_repository.enrollment_summary,
        )

    def get_enrollment_by_term(self) -> Report:
        """Generate the enrollment-by-term report."""

        return self._create_report(
            "enrollment_by_term",
            "Enrollment by Academic Term Report",
            self.report_repository.enrollment_by_term,
        )

    def get_grade_summary(self) -> Report:
        """Generate the grade summary report."""

        return self._create_report(
            "grade_summary",
            "Grade Summary Report",
            self.report_repository.grade_summary,
        )

    def get_student_performance(self) -> Report:
        """Generate the student performance report."""

        return self._create_report(
            "student_performance",
            "Student Academic Performance Report",
            self.report_repository.student_performance,
        )

    def get_system_overview(self) -> Report:
        """Generate the system overview report."""

        return self._create_report(
            "system_overview",
            "System Overview Report",
            self.report_repository.system_overview,
        )