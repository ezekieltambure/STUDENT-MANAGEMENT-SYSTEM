from datetime import date

from src.controllers.course_controller import CourseController
from src.controllers.enrollment_controller import EnrollmentController
from src.controllers.student_controller import StudentController
from src.models.enrollment import Enrollment


class EnrollmentView:
    """Terminal-based enrollment management interface."""

    def __init__(
        self,
        enrollment_controller: EnrollmentController | None = None,
        student_controller: StudentController | None = None,
        course_controller: CourseController | None = None,
    ) -> None:
        self.enrollment_controller = (
            enrollment_controller or EnrollmentController()
        )
        self.student_controller = (
            student_controller or StudentController()
        )
        self.course_controller = (
            course_controller or CourseController()
        )

    def display_menu(self) -> None:
        """Display the enrollment management menu."""

        print()
        print("=" * 80)
        print("                    ENROLLMENT MANAGEMENT")
        print("=" * 80)
        print("1. List Enrollments")
        print("2. Enroll Student")
        print("3. Search Enrollment")
        print("4. Update Enrollment")
        print("5. Delete Enrollment")
        print("6. Exit")
        print("=" * 80)

    def run(self) -> None:
        """Run the enrollment management menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.list_enrollments()

            elif choice == "2":
                self.enroll_student()

            elif choice == "3":
                self.search_enrollment()

            elif choice == "4":
                self.update_enrollment()

            elif choice == "5":
                self.delete_enrollment()

            elif choice == "6":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def list_enrollments(self) -> None:
        """Display all enrollments."""

        enrollments = (
            self.enrollment_controller.get_all_enrollments()
        )

        print()
        print("=" * 110)
        print("                           ENROLLMENTS")
        print("=" * 110)

        if not enrollments:
            print("No enrollments found.")
            print("=" * 110)
            return

        print(
            f"{'ID':<6}"
            f"{'STUDENT':<25}"
            f"{'COURSE':<30}"
            f"{'TERM ID':<10}"
            f"{'DATE':<14}"
            f"{'STATUS':<15}"
        )
        print("-" * 110)

        for enrollment in enrollments:
            student = self.student_controller.get_student(
                enrollment.student_id
            )
            course = self.course_controller.get_course(
                enrollment.course_id
            )

            student_name = (
                student.full_name
                if student
                else f"Student #{enrollment.student_id}"
            )

            course_name = (
                f"{course.course_code} - {course.course_name}"
                if course
                else f"Course #{enrollment.course_id}"
            )

            enrollment_date = (
                enrollment.enrollment_date.isoformat()
                if enrollment.enrollment_date
                else ""
            )

            print(
                f"{enrollment.id:<6}"
                f"{student_name:<25}"
                f"{course_name:<30}"
                f"{enrollment.term_id:<10}"
                f"{enrollment_date:<14}"
                f"{enrollment.status:<15}"
            )

        print("=" * 110)

    def enroll_student(self) -> None:
        """Create a new student enrollment."""

        print()
        print("-" * 70)
        print("                         ENROLL STUDENT")
        print("-" * 70)

        self._display_students()
        self._display_courses()

        try:
            student_id = int(
                input("Student ID: ").strip()
            )
            course_id = int(
                input("Course ID: ").strip()
            )
            term_id = int(
                input("Academic Term ID: ").strip()
            )

            status = input(
                "Status [Enrolled]: "
            ).strip()

            if not status:
                status = "Enrolled"

            enrollment = (
                self.enrollment_controller.create_enrollment(
                    student_id=student_id,
                    course_id=course_id,
                    term_id=term_id,
                    status=status,
                )
            )

            print()
            print("Enrollment created successfully.")
            print(f"Enrollment ID: {enrollment.id}")
            print(f"Student ID: {enrollment.student_id}")
            print(f"Course ID: {enrollment.course_id}")
            print(f"Term ID: {enrollment.term_id}")
            print(f"Status: {enrollment.status}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def search_enrollment(self) -> None:
        """Search for an enrollment by ID."""

        print()
        print("-" * 70)
        print("                       SEARCH ENROLLMENT")
        print("-" * 70)

        try:
            enrollment_id = int(
                input("Enrollment ID: ").strip()
            )
        except ValueError:
            print()
            print("Enrollment ID must be a valid integer.")
            return

        enrollment = (
            self.enrollment_controller.get_enrollment(
                enrollment_id
            )
        )

        if enrollment is None:
            print()
            print("Enrollment not found.")
            return

        self._display_enrollment(enrollment)

    def update_enrollment(self) -> None:
        """Update an existing enrollment."""

        print()
        print("-" * 70)
        print("                       UPDATE ENROLLMENT")
        print("-" * 70)

        try:
            enrollment_id = int(
                input("Enrollment ID: ").strip()
            )
        except ValueError:
            print()
            print("Enrollment ID must be a valid integer.")
            return

        enrollment = (
            self.enrollment_controller.get_enrollment(
                enrollment_id
            )
        )

        if enrollment is None:
            print()
            print("Enrollment not found.")
            return

        print()
        print("Press Enter to keep the current value.")
        print()

        print(f"Current Status: {enrollment.status}")

        new_status = input(
            "Status [current]: "
        ).strip()

        if new_status:
            enrollment.status = new_status

        try:
            updated = (
                self.enrollment_controller.update_enrollment(
                    enrollment
                )
            )

            print()
            print("Enrollment updated successfully.")
            print(f"Enrollment ID: {updated.id}")
            print(f"Status: {updated.status}")

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def delete_enrollment(self) -> None:
        """Delete an enrollment."""

        print()
        print("-" * 70)
        print("                       DELETE ENROLLMENT")
        print("-" * 70)

        try:
            enrollment_id = int(
                input("Enrollment ID: ").strip()
            )
        except ValueError:
            print()
            print("Enrollment ID must be a valid integer.")
            return

        enrollment = (
            self.enrollment_controller.get_enrollment(
                enrollment_id
            )
        )

        if enrollment is None:
            print()
            print("Enrollment not found.")
            return

        print()
        print(f"Enrollment ID: {enrollment.id}")
        print(f"Student ID: {enrollment.student_id}")
        print(f"Course ID: {enrollment.course_id}")
        print(f"Term ID: {enrollment.term_id}")
        print(f"Status: {enrollment.status}")

        confirmation = input(
            "Are you sure you want to delete this enrollment? "
            "(yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print()
            print("Deletion cancelled.")
            return

        try:
            success = (
                self.enrollment_controller.delete_enrollment(
                    enrollment.id
                )
            )

            print()

            if success:
                print("Enrollment deleted successfully.")
            else:
                print("Unable to delete enrollment.")

        except Exception as error:
            print()
            print("Unable to delete enrollment.")
            print(f"Reason: {error}")

    def _display_students(self) -> None:
        """Display available students."""

        students = self.student_controller.get_all_students()

        print()
        print("Available Students")
        print("-" * 70)

        if not students:
            print("No students available.")
            print("-" * 70)
            return

        print(
            f"{'ID':<6}"
            f"{'STUDENT NUMBER':<18}"
            f"{'NAME':<30}"
            f"{'PROGRAM':<20}"
        )
        print("-" * 70)

        for student in students:
            print(
                f"{student.id:<6}"
                f"{student.student_number:<18}"
                f"{student.full_name:<30}"
                f"{student.program:<20}"
            )

        print("-" * 70)

    def _display_courses(self) -> None:
        """Display available courses."""

        courses = self.course_controller.get_all_courses()

        print()
        print("Available Courses")
        print("-" * 80)

        if not courses:
            print("No courses available.")
            print("-" * 80)
            return

        print(
            f"{'ID':<6}"
            f"{'CODE':<14}"
            f"{'COURSE NAME':<35}"
            f"{'CREDITS':<10}"
            f"{'DEPT ID':<10}"
        )
        print("-" * 80)

        for course in courses:
            print(
                f"{course.id:<6}"
                f"{course.course_code:<14}"
                f"{course.course_name:<35}"
                f"{course.credit_hours:<10}"
                f"{course.department_id:<10}"
            )

        print("-" * 80)

    def _display_enrollment(
        self,
        enrollment: Enrollment,
    ) -> None:
        """Display enrollment details."""

        student = self.student_controller.get_student(
            enrollment.student_id
        )
        course = self.course_controller.get_course(
            enrollment.course_id
        )

        student_name = (
            student.full_name
            if student
            else f"Student #{enrollment.student_id}"
        )

        course_name = (
            f"{course.course_code} - {course.course_name}"
            if course
            else f"Course #{enrollment.course_id}"
        )

        enrollment_date = (
            enrollment.enrollment_date.isoformat()
            if enrollment.enrollment_date
            else "Not recorded"
        )

        print()
        print("=" * 70)
        print("                      ENROLLMENT DETAILS")
        print("=" * 70)
        print(f"Enrollment ID:    {enrollment.id}")
        print(f"Student:          {student_name}")
        print(f"Course:           {course_name}")
        print(f"Academic Term ID: {enrollment.term_id}")
        print(f"Enrollment Date:  {enrollment_date}")
        print(f"Status:           {enrollment.status}")
        print("=" * 70)
