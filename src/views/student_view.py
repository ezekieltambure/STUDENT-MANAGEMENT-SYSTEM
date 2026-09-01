from datetime import date
from typing import Optional

from src.controllers.student_controller import StudentController
from src.models.student import Student


class StudentView:
    """Terminal-based view for student management."""

    def __init__(
        self,
        student_controller: Optional[StudentController] = None,
    ) -> None:
        """Initialize the student view."""

        self.student_controller = (
            student_controller or StudentController()
        )

    def display_menu(self) -> None:
        """Display the student management menu."""

        print()
        print("=" * 50)
        print("          STUDENT MANAGEMENT")
        print("=" * 50)
        print("1. Add Student")
        print("2. Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        print("=" * 50)

    def add_student(self) -> Optional[Student]:
        """Collect student information and create a student."""

        print()
        print("-" * 50)
        print("             ADD STUDENT")
        print("-" * 50)

        student_number = input("Student Number: ").strip()
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        date_of_birth_text = input("Date of Birth (YYYY-MM-DD): ").strip()
        gender = input("Gender (Male/Female/Other): ").strip()
        program = input("Program: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()

        try:
            date_of_birth = date.fromisoformat(date_of_birth_text)

            student = Student(
                student_number=student_number,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                program=program,
                email=email,
                phone=phone,
            )

            created_student = self.student_controller.create_student(student)

            print()
            print("Student created successfully.")
            print(f"Student ID: {created_student.id}")
            print(f"Student Number: {created_student.student_number}")
            print(f"Name: {created_student.full_name}")

            return created_student

        except ValueError as error:
            print()
            print(f"Unable to create student: {error}")
            return None

    def search_student(self) -> Optional[Student]:
        """Search for a student by student number."""

        print()
        print("-" * 50)
        print("            SEARCH STUDENT")
        print("-" * 50)

        student_number = input("Student Number: ").strip()

        student = self.student_controller.find_by_student_number(
            student_number
        )

        if student is None:
            print()
            print("Student not found.")
            return None

        self.display_student(student)
        return student

    def update_student(self) -> Optional[Student]:
        """Update an existing student's information."""

        print()
        print("-" * 50)
        print("            UPDATE STUDENT")
        print("-" * 50)

        student_id_text = input("Student ID: ").strip()

        try:
            student_id = int(student_id_text)
        except ValueError:
            print()
            print("Invalid student ID.")
            return None

        student = self.student_controller.find_by_id(student_id)

        if student is None:
            print()
            print("Student not found.")
            return None

        print()
        print("Enter the new student information.")

        student_number = input(
            f"Student Number [{student.student_number}]: "
        ).strip()
        first_name = input(
            f"First Name [{student.first_name}]: "
        ).strip()
        last_name = input(
            f"Last Name [{student.last_name}]: "
        ).strip()
        date_of_birth_text = input(
            f"Date of Birth [{student.date_of_birth}]: "
        ).strip()
        gender = input(
            f"Gender [{student.gender}]: "
        ).strip()
        program = input(
            f"Program [{student.program}]: "
        ).strip()
        email = input(
            f"Email [{student.email}]: "
        ).strip()
        phone = input(
            f"Phone [{student.phone}]: "
        ).strip()

        try:
            if student_number:
                student.student_number = student_number

            if first_name:
                student.first_name = first_name

            if last_name:
                student.last_name = last_name

            if date_of_birth_text:
                student.date_of_birth = date.fromisoformat(
                    date_of_birth_text
                )

            if gender:
                student.gender = gender

            if program:
                student.program = program

            if email:
                student.email = email

            if phone:
                student.phone = phone

            updated_student = self.student_controller.update_student(
                student
            )

            print()
            print("Student updated successfully.")
            print(f"Student ID: {updated_student.id}")
            print(f"Student Number: {updated_student.student_number}")
            print(f"Name: {updated_student.full_name}")

            return updated_student

        except ValueError as error:
            print()
            print(f"Unable to update student: {error}")
            return None

    @staticmethod
    def display_student(student: Student) -> None:
        """Display student information."""

        print()
        print("=" * 50)
        print("             STUDENT DETAILS")
        print("=" * 50)
        print(f"Student ID:     {student.id}")
        print(f"Student Number: {student.student_number}")
        print(f"Name:            {student.full_name}")
        print(f"Date of Birth:   {student.date_of_birth}")
        print(f"Gender:          {student.gender}")
        print(f"Program:         {student.program}")
        print(f"Email:           {student.email}")
        print(f"Phone:           {student.phone}")
        print(f"Status:          {'Active' if student.is_active else 'Inactive'}")
        print("=" * 50)

    def delete_student(self) -> bool:
        """Delete a student by ID."""

        print()
        print("-" * 50)
        print("            DELETE STUDENT")
        print("-" * 50)

        student_id_text = input("Student ID: ").strip()

        try:
            student_id = int(student_id_text)
        except ValueError:
            print()
            print("Invalid student ID.")
            return False

        deleted = self.student_controller.delete_student(student_id)

        if deleted:
            print()
            print("Student deleted successfully.")
        else:
            print()
            print("Student not found.")

        return deleted
