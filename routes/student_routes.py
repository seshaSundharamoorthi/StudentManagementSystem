"""
routes/student_routes.py

This module defines the Flask Blueprint containing all web routing controllers 
for CRUD, searching, and filtering operations.
"""

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from student_manager import StudentManager

student_bp = Blueprint("students", __name__)


def get_manager() -> StudentManager:
    """
    Retrieves or initializes the global StudentManager cache instance 
    stored in the Flask application extensions.
    """
    if "student_manager" not in current_app.extensions:
        # Load database path from Flask config
        db_path = current_app.config.get("DATABASE_FILE", "students.json")
        current_app.extensions["student_manager"] = StudentManager(db_path)
    return current_app.extensions["student_manager"]


@student_bp.before_app_request
def require_login():
    """
    Forces all users to be logged in before viewing any page except
    the login page itself and static assets.
    """
    if not session.get("logged_in"):
        # Allow static files and the login page
        # Check endpoints safely (some requests might not match endpoints, e.g. 404s)
        if request.endpoint != "students.login" and not request.path.startswith("/static"):
            return redirect(url_for("students.login"))


@student_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles admin login authentication, verifying against env variables.
    """
    if session.get("logged_in"):
        return redirect(url_for("students.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        env_username = os.environ.get("ADMIN_USERNAME", "admin")
        env_password = os.environ.get("ADMIN_PASSWORD", "admin123")

        if username == env_username and password == env_password:
            session["logged_in"] = True
            flash("Welcome back, Admin!", "success")
            return redirect(url_for("students.dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")


@student_bp.route("/logout", methods=["POST"])
def logout():
    """
    Clears the session log and returns to the login page.
    """
    session.clear()
    flash("Successfully logged out.", "success")
    return redirect(url_for("students.login"))


@student_bp.route("/search")
def search():
    """
    Dedicated search route returning student profiles matching attributes.
    """
    manager = get_manager()
    search_by = request.args.get("search_by", "").strip().lower()
    query = request.args.get("query", "").strip().lower()
    matches = []

    if query:
        for stu in manager.students:
            if search_by == "id" and query in stu.student_id.lower():
                matches.append(stu)
            elif search_by == "name" and query in stu.name.lower():
                matches.append(stu)
            elif search_by == "department" and query in stu.department.lower():
                matches.append(stu)
            elif search_by == "email" and query in stu.email.lower():
                matches.append(stu)

    return render_template("search.html", search_by=search_by, query=query, matches=matches)



@student_bp.route("/dashboard")
def dashboard():
    """
    Renders the web dashboard demonstrating data analytics summary counters,
    department statistics, and year breakdowns.
    """
    manager = get_manager()
    students = manager.students

    total_count = len(students)

    # Department breakdown
    dept_counts = {}
    for s in students:
        dept = s.department.strip()
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

    # Year breakdown
    year_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for s in students:
        if s.year in year_counts:
            year_counts[s.year] += 1

    # Gender distribution
    gender_counts = {"Male": 0, "Female": 0, "Other": 0}
    for s in students:
        gender = s.gender.capitalize()
        if gender in gender_counts:
            gender_counts[gender] += 1

    return render_template(
        "dashboard.html",
        total_count=total_count,
        dept_counts=dept_counts,
        year_counts=year_counts,
        gender_counts=gender_counts
    )


@student_bp.route("/students")
def view_students():
    """
    Renders a list of all students. Integrates search and multi-filtering parameters
    using request args.
    """
    manager = get_manager()
    students_list = manager.students[:]  # Work with a copy of the list

    # Extract dynamic departments for filter dropdown
    all_departments = sorted(list(set(s.department for s in manager.students if s.department)))

    # Get search parameters
    search_by = request.args.get("search_by", "").strip().lower()
    query = request.args.get("query", "").strip().lower()

    if query:
        if search_by == "id":
            students_list = [s for s in students_list if query in s.student_id.lower()]
        elif search_by == "name":
            students_list = [s for s in students_list if query in s.name.lower()]
        elif search_by == "department":
            students_list = [s for s in students_list if query in s.department.lower()]
        elif search_by == "email":
            students_list = [s for s in students_list if query in s.email.lower()]

    # Get filter parameters
    dept_filter = request.args.get("department", "").strip()
    if dept_filter:
        students_list = [s for s in students_list if s.department.lower() == dept_filter.lower()]

    year_filter = request.args.get("year", "").strip()
    if year_filter.isdigit():
        students_list = [s for s in students_list if s.year == int(year_filter)]

    gender_filter = request.args.get("gender", "").strip().capitalize()
    if gender_filter in {"Male", "Female", "Other"}:
        students_list = [s for s in students_list if s.gender == gender_filter]

    min_age_str = request.args.get("min_age", "").strip()
    if min_age_str.isdigit():
        students_list = [s for s in students_list if s.age >= int(min_age_str)]

    max_age_str = request.args.get("max_age", "").strip()
    if max_age_str.isdigit():
        students_list = [s for s in students_list if s.age <= int(max_age_str)]

    return render_template(
        "students.html",
        students=students_list,
        departments=all_departments,
        search_by=search_by,
        query=query,
        dept_filter=dept_filter,
        year_filter=year_filter,
        gender_filter=gender_filter,
        min_age=min_age_str,
        max_age=max_age_str
    )


@student_bp.route("/students/add", methods=["GET", "POST"])
def add_student():
    """
    Renders the add student form page and accepts post submissions for inserting records.
    """
    form_data = {}
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        department = request.form.get("department", "").strip()
        year_str = request.form.get("year", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        # Save values for form reloading on validation error
        form_data = {
            "name": name,
            "age": age_str,
            "gender": gender,
            "department": department,
            "year": year_str,
            "email": email,
            "phone": phone
        }

        try:
            # Type conversions before record invocation
            age = int(age_str) if age_str.isdigit() else 0
            year = int(year_str) if year_str.isdigit() else 0

            manager = get_manager()
            manager.add_student_record(
                name=name,
                age=age,
                gender=gender,
                department=department,
                year=year,
                email=email,
                phone=phone
            )
            flash("Student added successfully!", "success")
            return redirect(url_for("students.view_students"))

        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "danger")

    return render_template("add_student.html", form_data=form_data)


@student_bp.route("/students/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id: str):
    """
    Renders the update form and accepts post actions for modifying student attributes.
    """
    manager = get_manager()
    student_obj = manager.get_student_by_id(student_id)

    if not student_obj:
        flash(f"Student with ID '{student_id}' not found.", "danger")
        return redirect(url_for("students.view_students"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        department = request.form.get("department", "").strip()
        year_str = request.form.get("year", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        try:
            # Type conversions
            age = int(age_str) if age_str.isdigit() else None
            year = int(year_str) if year_str.isdigit() else None

            # Attempt updates
            manager.update_student_record(
                student_id=student_id,
                name=name,
                age=age,
                gender=gender,
                department=department,
                year=year,
                email=email,
                phone=phone
            )
            flash(f"Student {student_id} updated successfully!", "success")
            return redirect(url_for("students.view_students"))

        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "danger")

    return render_template("edit_student.html", student=student_obj)


@student_bp.route("/students/delete/<student_id>", methods=["POST"])
def delete_student(student_id: str):
    """
    Deletes the target student record. Requires confirmation (handled on HTML client-side).
    """
    try:
        manager = get_manager()
        manager.delete_student_record(student_id)
        flash(f"Student {student_id} has been deleted successfully.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Failed to delete student: {e}", "danger")

    return redirect(url_for("students.view_students"))
