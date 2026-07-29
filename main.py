"""
main.py

This is the main entry point for the Student Management System. It implements
the menu-driven command line interface (CLI) and handles high-level user navigation.
"""

import sys
import os
from student_manager import StudentManager


def clear_screen() -> None:
    """
    Clears the terminal screen. Works on both Windows (cls) and Unix-based (clear) systems.
    """
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    """
    The main menu loop of the application. Renders the selection choices,
    routes calls to the StudentManager, and handles KeyboardInterrupts gracefully.
    """
    # Initialize the student manager (loads student records automatically)
    manager = StudentManager("students.json")

    while True:
        try:
            print("\n=====================================")
            print("      STUDENT MANAGEMENT SYSTEM")
            print("=====================================")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Search Student")
            print("6. Filter Students")
            print("7. Exit")
            print("=====================================")

            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                manager.add_student()
            elif choice == "2":
                manager.view_all_students()
            elif choice == "3":
                manager.update_student()
            elif choice == "4":
                manager.delete_student()
            elif choice == "5":
                manager.search_students()
            elif choice == "6":
                manager.filter_students()
            elif choice == "7":
                confirm = input("\nAre you sure you want to exit? (Y/N): ").strip().upper()
                if confirm in {"Y", "YES"}:
                    print("\nThank you for using Student Management System.")
                    print("Goodbye!\n")
                    sys.exit(0)
            else:
                print("\n[Error] Invalid option. Please select a valid number from 1 to 7.")

            # Pause before showing menu again (if not exiting)
            if choice != "7":
                input("\nPress [Enter] to return to the Main Menu...")
                # Optional: clear_screen() can be called here if a fresh console is desired
                # clear_screen()

        except KeyboardInterrupt:
            # Catch Ctrl+C and exit cleanly
            print("\n\n[Info] Keyboard Interrupt detected.")
            print("Saving data and shutting down Student Management System.")
            print("Goodbye!\n")
            sys.exit(0)
        except Exception as e:
            # Fail-safe catch-all to prevent raw system crashes
            print(f"\n[Critical Error] An unexpected error occurred: {e}")
            input("\nPress [Enter] to resume and return to the Main Menu...")


if __name__ == "__main__":
    main()
