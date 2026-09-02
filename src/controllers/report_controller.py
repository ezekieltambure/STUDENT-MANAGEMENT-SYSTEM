from src.models.report import Report
from src.services.report_service import ReportService


class ReportController:
    """Controller for report generation operations."""

    def __init__(
        self,
        report_service: ReportService | None = None,
    ) -> None:
        """Initialize the report controller."""

        self.report_service = (
            report_service or ReportService()
        )

    def get_student_summary(self) -> Report:
        """Generate the student summary report."""

        return self.report_service.get_student_summary()

    def get_students_by_department(self) -> Report:
        """Generate the students-by-department report."""

        return self.report_service.get_students_by_department()

    def get_course_summary(self) -> Report:
        """Generate the course summary report."""

        return self.report_service.get_course_summary()

    def get_enrollment_summary(self) -> Report:
        """Generate the enrollment summary report."""

        return self.report_service.get_enrollment_summary()

    def get_enrollment_by_term(self) -> Report:
        """Generate the enrollment-by-term report."""

        return self.report_service.get_enrollment_by_term()

    def get_grade_summary(self) -> Report:
        """Generate the grade summary report."""

        return self.report_service.get_grade_summary()

    def get_student_performance(self) -> Report:
        """Generate the student performance report."""

        return self.report_service.get_student_performance()

    def get_system_overview(self) -> Report:
        """Generate the system overview report."""

        return self.report_service.get_system_overview()