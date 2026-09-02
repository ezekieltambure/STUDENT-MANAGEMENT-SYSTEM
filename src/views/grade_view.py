from src.controllers.enrollment_controller import EnrollmentController
from src.controllers.grade_controller import GradeController
from src.controllers.student_controller import StudentController
from src.controllers.course_controller import CourseController
from src.models.grade import Grade


class GradeView:
    """Terminal-based grade management interface."""

    def __init__(
        self,
        grade_controller: GradeController | None = None,
        enrollment_controller: EnrollmentController | None = None,
        student_controller: StudentController | None = None,
        course_controller: CourseController | None = None,
    ) -> None:
        self.grade_controller = (
            grade_controller or GradeController()
        )
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
        """Display the grade management menu."""

        print()
        print("=" * 90)
        print("                         GRADE MANAGEMENT")
        print("=" * 90)
        print("1. List Grades")
        print("2. Record Grade")
        print("3. Search Grade")
        print("4. Update Grade")
        print("5. Delete Grade")
        print("6. Exit")
        print("=" * 90)

    def run(self) -> None:
        """Run the interactive grade management menu."""

        while True:
            self.display_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.list_grades()

            elif choice == "2":
                self.record_grade()

            elif choice == "3":
                self.search_grade()

            elif choice == "4":
                self.update_grade()

            elif choice == "5":
                self.delete_grade()

            elif choice == "6":
                print()
                print("Returning to dashboard...")
                break

            else:
                print()
                print("Invalid option. Please try again.")

    def list_grades(self) -> None:
        """Display all recorded grades."""

        grades = self.grade_controller.get_all_grades()

        print()
        print("=" * 120)
        print("                              GRADES")
        print("=" * 120)

        if not grades:
            print("No grades found.")
            print("=" * 120)
            return

        print(
            f"{'ID':<6}"
            f"{'STUDENT':<25}"
            f"{'COURSE':<28}"
            f"{'ASSESS':<10}"
            f"{'EXAM':<10}"
            f"{'FINAL':<10}"
            f"{'GRADE':<8}"
            f"{'POINT':<8}"
            f"{'REMARKS':<15}"
        )
        print("-" * 120)

        for grade in grades:
            student_name, course_name = (
                self._get_enrollment_details(
                    grade.enrollment_id
                )
            )

            print(
                f"{grade.id:<6}"
                f"{student_name:<25}"
                f"{course_name:<28}"
                f"{grade.assessment_score:<10.2f}"
                f"{grade.exam_score:<10.2f}"
                f"{grade.final_score:<10.2f}"
                f"{grade.grade_letter:<8}"
                f"{grade.grade_point:<8.1f}"
                f"{grade.remarks:<15}"
            )

        print("=" * 120)

    def record_grade(self) -> None:
        """Record a new grade."""

        print()
        print("-" * 80)
        print("                           RECORD GRADE")
        print("-" * 80)

        self._display_enrollments()

        try:
            enrollment_id = int(
                input("Enrollment ID: ").strip()
            )

            assessment_score = float(
                input("Assessment Score (0-100): ").strip()
            )

            exam_score = float(
                input("Exam Score (0-100): ").strip()
            )

            remarks = input(
                "Remarks (optional): "
            ).strip()

            grade = self.grade_controller.create_grade(
                enrollment_id=enrollment_id,
                assessment_score=assessment_score,
                exam_score=exam_score,
                remarks=remarks,
            )

            print()
            print("Grade recorded successfully.")
            self._display_grade(grade)

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def search_grade(self) -> None:
        """Search for a grade by ID."""

        print()
        print("-" * 80)
        print("                           SEARCH GRADE")
        print("-" * 80)

        try:
            grade_id = int(
                input("Grade ID: ").strip()
            )
        except ValueError:
            print()
            print("Grade ID must be a valid integer.")
            return

        grade = self.grade_controller.get_grade(grade_id)

        if grade is None:
            print()
            print("Grade not found.")
            return

        self._display_grade(grade)

    def update_grade(self) -> None:
        """Update an existing grade."""

        print()
        print("-" * 80)
        print("                           UPDATE GRADE")
        print("-" * 80)

        try:
            grade_id = int(
                input("Grade ID: ").strip()
            )
        except ValueError:
            print()
            print("Grade ID must be a valid integer.")
            return

        grade = self.grade_controller.get_grade(grade_id)

        if grade is None:
            print()
            print("Grade not found.")
            return

        print()
        print("Press Enter to keep the current value.")
        print()

        assessment_input = input(
            f"Assessment Score [{grade.assessment_score}]: "
        ).strip()

        exam_input = input(
            f"Exam Score [{grade.exam_score}]: "
        ).strip()

        remarks_input = input(
            f"Remarks [{grade.remarks}]: "
        ).strip()

        try:
            if assessment_input:
                grade.assessment_score = float(
                    assessment_input
                )

            if exam_input:
                grade.exam_score = float(exam_input)

            if remarks_input:
                grade.remarks = remarks_input

            updated = self.grade_controller.update_grade(
                grade
            )

            print()
            print("Grade updated successfully.")
            self._display_grade(updated)

        except (ValueError, TypeError) as error:
            print()
            print(f"Error: {error}")

    def delete_grade(self) -> None:
        """Delete a grade."""

        print()
        print("-" * 80)
        print("                           DELETE GRADE")
        print("-" * 80)

        try:
            grade_id = int(
                input("Grade ID: ").strip()
            )
        except ValueError:
            print()
            print("Grade ID must be a valid integer.")
            return

        grade = self.grade_controller.get_grade(grade_id)

        if grade is None:
            print()
            print("Grade not found.")
            return

        self._display_grade(grade)

        confirmation = input(
            "Are you sure you want to delete this grade? "
            "(yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print()
            print("Deletion cancelled.")
            return

        try:
            success = self.grade_controller.delete_grade(
                grade_id
            )

            print()

            if success:
                print("Grade deleted successfully.")
            else:
                print("Unable to delete grade.")

        except Exception as error:
            print()
            print("Unable to delete grade.")
            print(f"Reason: {error}")

    def _display_enrollments(self) -> None:
        """Display available enrollments."""

        enrollments = (
            self.enrollment_controller.get_all_enrollments()
        )

        print()
        print("Available Enrollments")
        print("-" * 100)

        if not enrollments:
            print("No enrollments available.")
            print("-" * 100)
            return

        print(
            f"{'ID':<6}"
            f"{'STUDENT':<25}"
            f"{'COURSE':<30}"
            f"{'TERM':<10}"
            f"{'STATUS':<15}"
        )
        print("-" * 100)

        for enrollment in enrollments:
            student_name, course_name = (
                self._get_enrollment_details(
                    enrollment.id
                )
            )

            print(
                f"{enrollment.id:<6}"
                f"{student_name:<25}"
                f"{course_name:<30}"
                f"{enrollment.term_id:<10}"
                f"{enrollment.status:<15}"
            )

        print("-" * 100)

    def _get_enrollment_details(
        self,
        enrollment_id: int | None,
    ) -> tuple[str, str]:
        """Return student and course names for an enrollment."""

        if enrollment_id is None:
            return "Unknown Student", "Unknown Course"

        enrollment = (
            self.enrollment_controller.get_enrollment(
                enrollment_id
            )
        )

        if enrollment is None:
            return "Unknown Student", "Unknown Course"

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

        return student_name, course_name

    def _display_grade(self, grade: Grade) -> None:
        """Display detailed grade information."""

        student_name, course_name = (
            self._get_enrollment_details(
                grade.enrollment_id
            )
        )

        print()
        print("=" * 80)
        print("                            GRADE DETAILS")
        print("=" * 80)
        print(f"Grade ID:          {grade.id}")
        print(f"Student:           {student_name}")
        print(f"Course:            {course_name}")
        print(f"Enrollment ID:     {grade.enrollment_id}")
        print(f"Assessment Score:  {grade.assessment_score:.2f}")
        print(f"Exam Score:        {grade.exam_score:.2f}")
        print(f"Final Score:       {grade.final_score:.2f}")
        print(f"Grade Letter:      {grade.grade_letter}")
        print(f"Grade Point:       {grade.grade_point:.1f}")
        print(f"Remarks:           {grade.remarks}")
        print("=" * 80)
