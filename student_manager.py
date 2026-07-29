"""
student_manager.py

This module contains the StudentManager class, which implements all core CRUD operations,
data searching, and filtering logic for managing students.
"""

from typing import List, Optional
from student import Student
from file_handler import FileHandler
import utils


class StudentManager:
    """
    Manages the collection of students, coordinates interactions with FileHandler
    for persistence, and encapsulates the business logic for additions, updates,
    deletions, searching, and filtering.
    """

    def __init__(self, filepath: str = "students.json") -> None:
        """
        Initializes the StudentManager and loads existing student records.

        Args:
            filepath (str): Path to the storage JSON file. Defaults to 'students.json'.
        """
        self.file_handler = FileHandler(filepath)
        self.students: List[Student] = []
        self.load_students_from_file()

    def load_students_from_file(self) -> None:
        """
        Loads student dictionaries from persistent JSON storage, converts them
        to Student objects, and caches them in memory.
        """
        try:
            raw_data = self.file_handler.load_data()
            self.students = [Student.from_dict(item) for item in raw_data]
        except Exception as e:
            print(f"Error loading student database: {e}")
            self.students = []

    def save_students_to_file(self) -> bool:
        """
        Serializes all Student objects in memory to dictionary format
        and saves them using the FileHandler.

        Returns:
            bool: True if save operation succeeded, False otherwise.
        """
        try:
            data = [stu.to_dict() for stu in self.students]
            return self.file_handler.save_data(data)
        except Exception as e:
            print(f"Error saving student database: {e}")
            return False

    def generate_next_id(self) -> str:
        """
        Generates the next sequential unique Student ID in the format STU1001, STU1002, etc.
        It parses existing IDs to find the maximum suffix number and increments it.

        Returns:
            str: The auto-generated Student ID.
        """
        base_id = 1001
        max_num = base_id - 1

        for stu in self.students:
            id_str = stu.student_id
            if id_str.startswith("STU") and id_str[3:].isdigit():
                try:
                    num = int(id_str[3:])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    continue

        return f"STU{max_num + 1}"

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        Retrieves a student record from memory matching the given student_id.

        Args:
            student_id (str): The ID to search for (case-insensitive).

        Returns:
            Optional[Student]: The Student object if found, otherwise None.
        """
        search_id = student_id.strip().upper()
        for stu in self.students:
            if stu.student_id.upper() == search_id:
                return stu
        return None

    def add_student(self) -> None:
        """
        Guides the CLI user to add a new student. Prompts for details using
        validated input wrappers from utils, auto-generates a unique ID,
        and saves the record.
        """
        print("\n--- Add New Student ---")
        
        # Collect validated fields
        name = utils.prompt_student_name()
        age = utils.prompt_student_age()
        gender = utils.prompt_student_gender()
        department = utils.prompt_student_department()
        year = utils.prompt_student_year()
        email = utils.prompt_student_email()
        phone = utils.prompt_student_phone()

        # Check for duplication of email/phone in existing database (Good practice)
        for stu in self.students:
            if stu.email.lower() == email.lower():
                print(f"\n[Error] A student with email '{email}' already exists.")
                return
            if stu.phone == phone:
                print(f"\n[Error] A student with phone number '{phone}' already exists.")
                return

        # Generate unique Student ID
        student_id = self.generate_next_id()

        # Instantiate student and save
        new_student = Student(
            student_id=student_id,
            name=name,
            age=age,
            gender=gender,
            department=department,
            year=year,
            email=email,
            phone=phone
        )

        self.students.append(new_student)
        if self.save_students_to_file():
            print(f"\n[Success] Student successfully added! Assigned ID: {student_id}")
        else:
            print("\n[Error] Failed to add student due to a storage write issue.")

    def view_all_students(self) -> None:
        """
        Renders all currently stored students in a formatted ASCII table.
        """
        print("\n--- All Student Records ---")
        self._print_table(self.students)

    def update_student(self) -> None:
        """
        Allows updating specific fields of a student. The user is prompted for
        the student's ID, and then for each field. Pressing 'Enter' leaves
        the current value unchanged.
        """
        print("\n--- Update Student Record ---")
        student_id = input("Enter Student ID to update (e.g., STU1001): ").strip()
        student = self.get_student_by_id(student_id)

        if not student:
            print(f"[Error] Student with ID '{student_id}' not found.")
            return

        print(f"\nUpdating details for {student.name} ({student.student_id}).")
        print("Press [Enter] to keep the current value unchanged.\n")

        # Collect validated fields with empty input allowed (retains existing)
        new_name = utils.prompt_student_name(allow_empty=True)
        new_age = utils.prompt_student_age(allow_empty=True)
        new_gender = utils.prompt_student_gender(allow_empty=True)
        new_department = utils.prompt_student_department(allow_empty=True)
        new_year = utils.prompt_student_year(allow_empty=True)
        new_email = utils.prompt_student_email(allow_empty=True)
        new_phone = utils.prompt_student_phone(allow_empty=True)

        # Apply updates if new inputs are provided
        updated = False
        if new_name:
            student.name = new_name
            updated = True
        if new_age:
            student.age = new_age
            updated = True
        if new_gender:
            student.gender = new_gender
            updated = True
        if new_department:
            student.department = new_department
            updated = True
        if new_year:
            student.year = new_year
            updated = True

        if new_email:
            # Check for email duplicates among other students
            email_dup = False
            for stu in self.students:
                if stu.student_id != student.student_id and stu.email.lower() == new_email.lower():
                    print(f"[Error] Another student with email '{new_email}' already exists. Skipping email update.")
                    email_dup = True
                    break
            if not email_dup:
                student.email = new_email
                updated = True

        if new_phone:
            # Check for phone duplicates among other students
            phone_dup = False
            for stu in self.students:
                if stu.student_id != student.student_id and stu.phone == new_phone:
                    print(f"[Error] Another student with phone '{new_phone}' already exists. Skipping phone update.")
                    phone_dup = True
                    break
            if not phone_dup:
                student.phone = new_phone
                updated = True

        if updated:
            if self.save_students_to_file():
                print(f"\n[Success] Student ID {student.student_id} successfully updated!")
            else:
                print("\n[Error] Failed to save updates to file storage.")
        else:
            print("\n[Info] No changes made.")

    def delete_student(self) -> None:
        """
        Deletes a student record by ID. Asks for user confirmation before deletion.
        """
        print("\n--- Delete Student Record ---")
        student_id = input("Enter Student ID to delete: ").strip()
        student = self.get_student_by_id(student_id)

        if not student:
            print(f"[Error] Student with ID '{student_id}' not found.")
            return

        print(f"\nAre you sure you want to delete the following record?")
        print(f"  ID: {student.student_id}")
        print(f"  Name: {student.name}")
        print(f"  Department: {student.department}")
        
        confirm = input("\nType 'Y' or 'YES' to confirm deletion: ").strip().upper()
        if confirm in {"Y", "YES"}:
            self.students.remove(student)
            if self.save_students_to_file():
                print(f"\n[Success] Student {student.student_id} has been deleted.")
            else:
                print("\n[Error] Failed to save changes to storage.")
        else:
            print("\n[Info] Deletion cancelled.")

    def search_students(self) -> None:
        """
        Displays a search menu and performs search queries on fields:
        Student ID, Name, Department, and Email.
        """
        while True:
            print("\n--- Search Students ---")
            print("1. Search by Student ID")
            print("2. Search by Name")
            print("3. Search by Department")
            print("4. Search by Email")
            print("5. Back to Main Menu")

            choice = input("Enter your search choice (1-5): ").strip()

            if choice == "5":
                break

            if choice not in {"1", "2", "3", "4"}:
                print("[Error] Invalid choice. Please enter a number between 1 and 5.")
                continue

            query = input("Enter search query: ").strip().lower()
            if not query:
                print("[Warning] Empty query. Showing all students.")
                self.view_all_students()
                continue

            matches: List[Student] = []

            for stu in self.students:
                if choice == "1":
                    if query in stu.student_id.lower():
                        matches.append(stu)
                elif choice == "2":
                    if query in stu.name.lower():
                        matches.append(stu)
                elif choice == "3":
                    if query in stu.department.lower():
                        matches.append(stu)
                elif choice == "4":
                    if query in stu.email.lower():
                        matches.append(stu)

            print(f"\n--- Search Results ({len(matches)} matches found) ---")
            self._print_table(matches)

    def filter_students(self) -> None:
        """
        Prompts user for filters (Department, Year, Gender, Age Range)
        and displays matched student records.
        """
        print("\n--- Filter Student Records ---")
        print("Leave fields blank to skip filtering by that criteria.\n")

        dept_filter = input("Enter Department to filter by (or press Enter to skip): ").strip().lower()
        
        year_input = input("Enter Year to filter by (1-5, or press Enter to skip): ").strip()
        year_filter = int(year_input) if year_input.isdigit() and 1 <= int(year_input) <= 5 else None

        gender_input = input("Enter Gender to filter by (Male/Female/Other, or press Enter to skip): ").strip().capitalize()
        gender_filter = gender_input if gender_input in {"Male", "Female", "Other"} else None

        min_age_input = input("Enter Minimum Age (or press Enter to skip): ").strip()
        min_age = int(min_age_input) if min_age_input.isdigit() else None

        max_age_input = input("Enter Maximum Age (or press Enter to skip): ").strip()
        max_age = int(max_age_input) if max_age_input.isdigit() else None

        filtered: List[Student] = []

        for stu in self.students:
            # Check department filter
            if dept_filter and dept_filter not in stu.department.lower():
                continue
            # Check year filter
            if year_filter is not None and stu.year != year_filter:
                continue
            # Check gender filter
            if gender_filter and stu.gender != gender_filter:
                continue
            # Check age range filters
            if min_age is not None and stu.age < min_age:
                continue
            # Check age range filters
            if max_age is not None and stu.age > max_age:
                continue

            filtered.append(stu)

        print(f"\n--- Filter Results ({len(filtered)} matches found) ---")
        self._print_table(filtered)

    def _print_table(self, students: List[Student]) -> None:
        """
        Private helper to print student records in a clean tabular ASCII format.

        Args:
            students (List[Student]): List of students to display.
        """
        if not students:
            print("No student records found.")
            return

        # Define column headers
        headers = ["Student ID", "Name", "Age", "Gender", "Department", "Year", "Email", "Phone"]
        
        # Calculate dynamic column widths to accommodate all text lengths
        widths = [len(h) for h in headers]
        for stu in students:
            widths[0] = max(widths[0], len(stu.student_id))
            widths[1] = max(widths[1], len(stu.name))
            widths[2] = max(widths[2], len(str(stu.age)))
            widths[3] = max(widths[3], len(stu.gender))
            widths[4] = max(widths[4], len(stu.department))
            widths[5] = max(widths[5], len(str(stu.year)))
            widths[6] = max(widths[6], len(stu.email))
            widths[7] = max(widths[7], len(stu.phone))
            
        # Format the top/bottom/middle boundary lines
        separator = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        
        # Print table header
        print(separator)
        header_row = "|" + "|".join(f" {headers[i].ljust(widths[i])} " for i in range(len(headers))) + "|"
        print(header_row)
        print(separator)
        
        # Print each row of student data
        for stu in students:
            row = [
                stu.student_id,
                stu.name,
                str(stu.age),
                stu.gender,
                stu.department,
                str(stu.year),
                stu.email,
                stu.phone
            ]
            data_row = "|" + "|".join(f" {row[i].ljust(widths[i])} " for i in range(len(row))) + "|"
            print(data_row)
            
        print(separator)
        print(f"Total Student Records: {len(students)}\n")

    def add_student_record(
        self,
        name: str,
        age: int,
        gender: str,
        department: str,
        year: int,
        email: str,
        phone: str
    ) -> Student:
        """
        Programmatic API to add a student record. Validates all inputs and checks for duplicates.

        Args:
            name (str): Student name
            age (int): Student age
            gender (str): Student gender
            department (str): Student department
            year (int): Academic year
            email (str): Student email
            phone (str): Student phone number

        Returns:
            Student: The newly created student instance.

        Raises:
            ValueError: If validation fails or duplicate entries are found.
        """
        if not utils.validate_name(name):
            raise ValueError("Name must contain only letters and spaces, and cannot be empty.")
        if not utils.validate_age(str(age)):
            raise ValueError("Age must be a valid integer between 15 and 100.")
        if not utils.validate_gender(gender):
            raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
        if not department.strip():
            raise ValueError("Department cannot be empty.")
        if not utils.validate_year(str(year)):
            raise ValueError("Year must be a valid integer between 1 and 5.")
        if not utils.validate_email(email):
            raise ValueError("Please enter a valid email address.")
        if not utils.validate_phone(phone):
            raise ValueError("Phone number must be exactly 10 digits.")

        # Check for duplication of email/phone
        for stu in self.students:
            if stu.email.lower() == email.lower():
                raise ValueError(f"A student with email '{email}' already exists.")
            if stu.phone == phone:
                raise ValueError(f"A student with phone '{phone}' already exists.")

        student_id = self.generate_next_id()
        new_student = Student(
            student_id=student_id,
            name=name.strip(),
            age=int(age),
            gender=gender.strip().capitalize(),
            department=department.strip(),
            year=int(year),
            email=email.strip(),
            phone=phone.strip()
        )
        self.students.append(new_student)
        if not self.save_students_to_file():
            raise IOError("Failed to save student record to JSON file database.")
        return new_student

    def update_student_record(
        self,
        student_id: str,
        name: str = "",
        age: Optional[int] = None,
        gender: str = "",
        department: str = "",
        year: Optional[int] = None,
        email: str = "",
        phone: str = ""
    ) -> bool:
        """
        Programmatic API to update a student record. Validates all non-empty inputs.

        Returns:
            bool: True if updated, False if no changes made.

        Raises:
            ValueError: If validation fails or duplicate entries are found.
        """
        student_obj = self.get_student_by_id(student_id)
        if not student_obj:
            raise ValueError(f"Student with ID '{student_id}' not found.")

        updated = False

        if name:
            if not utils.validate_name(name):
                raise ValueError("Name must contain only letters and spaces.")
            student_obj.name = name.strip()
            updated = True

        if age is not None:
            if not utils.validate_age(str(age)):
                raise ValueError("Age must be an integer between 15 and 100.")
            student_obj.age = int(age)
            updated = True

        if gender:
            if not utils.validate_gender(gender):
                raise ValueError("Gender must be 'Male', 'Female', or 'Other'.")
            student_obj.gender = gender.strip().capitalize()
            updated = True

        if department:
            if not department.strip():
                raise ValueError("Department cannot be empty.")
            student_obj.department = department.strip()
            updated = True

        if year is not None:
            if not utils.validate_year(str(year)):
                raise ValueError("Year must be an integer between 1 and 5.")
            student_obj.year = int(year)
            updated = True

        if email:
            if not utils.validate_email(email):
                raise ValueError("Please enter a valid email address.")
            for stu in self.students:
                if stu.student_id != student_obj.student_id and stu.email.lower() == email.lower():
                    raise ValueError(f"Another student with email '{email}' already exists.")
            student_obj.email = email.strip()
            updated = True

        if phone:
            if not utils.validate_phone(phone):
                raise ValueError("Phone number must be exactly 10 digits.")
            for stu in self.students:
                if stu.student_id != student_obj.student_id and stu.phone == phone:
                    raise ValueError(f"Another student with phone '{phone}' already exists.")
            student_obj.phone = phone.strip()
            updated = True

        if updated:
            if not self.save_students_to_file():
                raise IOError("Failed to save updates to file storage.")
        return updated

    def delete_student_record(self, student_id: str) -> bool:
        """
        Programmatic API to delete a student record by ID.

        Returns:
            bool: True if deleted.

        Raises:
            ValueError: If student not found.
        """
        student_obj = self.get_student_by_id(student_id)
        if not student_obj:
            raise ValueError(f"Student with ID '{student_id}' not found.")

        self.students.remove(student_obj)
        if not self.save_students_to_file():
            raise IOError("Failed to save changes to storage.")
        return True

