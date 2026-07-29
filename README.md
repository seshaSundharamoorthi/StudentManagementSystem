# Student Management System

A robust, production-quality, modular CLI-based **Student Management System** developed in Python 3. It utilizes Object-Oriented Programming (OOP) design and local file handling for data storage. This application is created as part of the Kinetrexa Software Python Development Internship task assignment.

---

## Project Overview

The **Student Management System** is a lightweight, local database manager for student records. It allows educational coordinators and administrators to manage student records efficiently directly from a terminal-based interface. The records are persistently stored in a local JSON file (`students.json`), which is automatically read at launch and updated after every addition, update, or deletion.

---

## Features

- **Student CRUD Operations**:
  - **Create**: Add student records with auto-generated incremental IDs (e.g., `STU1001`, `STU1002`).
  - **Read**: View all student records presented in a neat, dynamically-sizing ASCII table.
  - **Update**: Modify existing student attributes individually with option to leave fields unchanged.
  - **Delete**: Remove a student record after a mandatory confirmation screen.
- **Search Capabilities**: Find students by Student ID, Name, Department, or Email (supports partial, case-insensitive matches).
- **Filtering Capabilities**: Filter student records by Department, Year, Gender, or Age Range (Min/Max).
- **Input Validation**: Robust validation of inputs (e.g., Name must contain only alphabetic characters; Age must be between 15 and 100; Phone number must be exactly 10 digits; Email must match standard patterns).
- **Persistent JSON Storage**: Automatic loading and saving of records. Re-initializes empty database if storage file is missing or corrupted.
- **Error Handling**: Graceful exception catching preventing raw code crashes (e.g., handling KeyboardInterrupt Ctrl+C gracefully).

---

## Folder Structure

```text
StudentManagementSystem/
│
├── main.py                 # Application entry point & CLI Menu Loop
├── student.py              # Student model class representing a student
├── student_manager.py      # Business logic (CRUD, Searching, Filtering)
├── file_handler.py         # File read/write logic for students.json
├── utils.py                # Reusable validation and input prompt functions
├── students.json           # Local JSON file database
├── requirements.txt        # Package dependencies (uses standard library only)
├── .gitignore              # Git ignore file for python caches and IDE files
└── report/
    └── report.md           # Detailed Project internship report
```

---

## Technologies Used

- **Language**: Python 3.x
- **Standard Library Modules**:
  - `json` (for reading and writing persistent state)
  - `os` (for file checking and screen clearing)
  - `re` (for email pattern matching regex)
  - `sys` (for graceful application exits)
  - `typing` (for standard PEP 484 static type hints)

---

## Installation

1. **Prerequisites**: Ensure you have Python 3.6 or later installed on your system.
2. **Clone / Download**: Clone this repository or download the source folder to your local machine.
   ```bash
   git clone https://github.com/yourusername/StudentManagementSystem.git
   cd StudentManagementSystem
   ```
3. **Setup Dependencies**: This project uses only Python's built-in standard libraries. There is no need to install external packages.
   ```bash
   # Optional: verification of python installation
   python --version
   ```

---

## How to Run

Execute the main file using python from your terminal:

```bash
python main.py
```

---

## Sample CLI Output

### Main Menu Interface
```text
=====================================
      STUDENT MANAGEMENT SYSTEM
=====================================
1. Add Student
2. View All Students
3. Update Student
4. Delete Student
5. Search Student
6. Filter Students
7. Exit
=====================================
Enter your choice (1-7): 2
```

### Tabular Display Layout
```text
+------------+---------------+-----+--------+------------------+------+---------------------------+------------+
| Student ID | Name          | Age | Gender | Department       | Year | Email                     | Phone      |
+------------+---------------+-----+--------+------------------+------+---------------------------+------------+
| STU1001    | Alice Johnson | 20  | Female | Computer Science | 2    | alice.johnson@example.com | 9876543210 |
| STU1002    | Bob Smith     | 21  | Male   | Information Tech | 3    | bob.smith@example.com     | 8765432109 |
+------------+---------------+-----+--------+------------------+------+---------------------------+------------+
Total Student Records: 2
```

---

## Screenshots Placeholder

Here are placeholders for visual walk-throughs of the application when executing tasks:

- **Main Menu Preview**
  <!-- [Screenshot Placeholder: Main Menu screen showing options 1 to 7] -->
- **Add Student with Validation Error**
  <!-- [Screenshot Placeholder: Demonstration of validation warning when typing invalid email or phone number] -->
- **Tabular View of All Students**
  <!-- [Screenshot Placeholder: Full ASCII Table showing the sample database] -->
- **Filtering Students Interface**
  <!-- [Screenshot Placeholder: Filtered list showing students corresponding only to 'Computer Science'] -->

---

## Future Enhancements

1. **SQLite Database Integration**: Migrate from local JSON file storage to a relational database for enhanced concurrent writing capabilities.
2. **Graphical User Interface (GUI)**: Create a Tkinter or PySide/PyQt graphical user interface for a cleaner desktop window experience.
3. **Export Reports**: Allow exporting the student tables into CSV, Excel, or PDF report formats.
4. **Course & Grade Tracking**: Extend the schema to add courses enrollment and GPA tracking per student.

---

## Cloud Deployment & Git Upload Guide

This project is fully structured and prepared for continuous integration deployment on cloud services like **Render** and **Vercel**.

### Environment Variables Config

Admin authentication values are loaded dynamically from environment variables on the cloud server. Make sure to configure the following variables in your cloud dashboards:

- `ADMIN_USERNAME`: Custom admin username (Defaults to `admin` if not configured)
- `ADMIN_PASSWORD`: Custom admin password (Defaults to `admin123` if not configured)

---

### 1. GitHub Upload Steps

To push the project codebase to your public GitHub repository:

1. **Initialize Git Repository**:
   ```bash
   git init
   ```
2. **Stage Project Files**:
   ```bash
   git add .
   ```
3. **Commit Code Changes**:
   ```bash
   git commit -m "feat: migrate Student Management System to Flask Web App with Session Auth"
   ```
4. **Create Branch**:
   ```bash
   git branch -M main
   ```
5. **Add Remote Endpoint & Push**:
   ```bash
   git remote add origin https://github.com/your-username/StudentManagementSystem.git
   git push -u origin main
   ```

---

### 2. Render Deployment (Recommended)

Render runs web containers which allow disk persistence modifications to stay alive during the container session lifespan (though they will reset upon container rebuilding unless paired with a Render Persistent Disk volume).

1. Sign up or log into **Render** (`https://render.com`).
2. Go to **Dashboard** and select **New +** -> **Web Service**.
3. Link your GitHub account and select your `StudentManagementSystem` repository.
4. Set the following settings:
   - **Name**: `student-management-system`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Under **Environment Variables**, add:
   - `ADMIN_USERNAME` = `admin`
   - `ADMIN_PASSWORD` = `admin123`
6. Click **Deploy Web Service**.
7. **Live URL Format**: `https://student-management-system.onrender.com`

---

### 3. Vercel Deployment

> [!WARNING]
> Vercel runs on serverless architecture where the local directory is read-only and ephemeral. The application will start successfully, but any additions, modifications, or deletions in the directory (`students.json`) will not persist across serverless invocation restarts. Vercel deployment is recommended for previewing routes, logins, and CLI views, but Render should be preferred for state persistence testing.

1. Install the Vercel CLI locally (or link Vercel to your GitHub repository from the Vercel Dashboard):
   ```bash
   npm install -g vercel
   ```
2. Run the deployment setup from your project directory:
   ```bash
   vercel
   ```
3. Link to your project and select Vercel defaults. The configuration in `vercel.json` will automatically map Flask routing.
4. Configure environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) on the Vercel Project Dashboard under **Settings -> Environment Variables**.
5. Deploy to production:
   ```bash
   vercel --prod
   ```
6. **Live URL Format**: `https://student-management-system.vercel.app`

---

## Author

- **Name**: SESHA S
- **Application ID**: KTS020260716704
- **Internship Domain**: Python Development Internship
- **Organization**: Kinetrexa Software Private Limited
- **Duration**: 20 July 2026 – 19 August 2026
#   S t u d e n t M a n a g e m e n t S y s t e m  
 