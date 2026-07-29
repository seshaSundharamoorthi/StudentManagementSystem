"""
app.py

Main entry point for the Flask Web Application. Configures application settings,
registers blueprints, handles routing initialization, and starts the local server on an
available port.
"""

import socket
from flask import Flask, redirect, url_for
from routes.student_routes import student_bp


def find_free_port(start_port: int = 5000) -> int:
    """
    Finds the first available TCP port starting from start_port.
    Ensures that we do not crash if port 5000 is occupied.

    Args:
        start_port (int): The port number to start checking. Defaults to 5000.

    Returns:
        int: The first available port.
    """
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                # Set SO_REUSEADDR so that socket can be bound immediately after close
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    return start_port


def create_app(db_filename: str = "students.json") -> Flask:
    """
    Flask Application Factory pattern implementation.

    Args:
        db_filename (str): Target filename for persistence storage.

    Returns:
        Flask: Instantiated app object.
    """
    app = Flask(__name__)

    # Set secret key for flash session signature
    app.secret_key = "kinetrexa_secret_key_student_management"

    # Configure database file path
    app.config["DATABASE_FILE"] = db_filename

    # Register routes blueprints
    app.register_blueprint(student_bp)

    @app.route("/")
    def index():
        """Redirects root page to the dashboard."""
        return redirect(url_for("students.dashboard"))

    return app


# Instantiated Flask app at the module scope for WSGI runners (e.g., Gunicorn/Vercel)
app = create_app()

if __name__ == "__main__":
    # Determine free port
    target_port = find_free_port(5000)

    print("\n" + "=" * 50)
    print("      STARTING STUDENT MANAGEMENT SYSTEM WEB APP")
    print("=" * 50)
    print(f"Local Server URL: http://127.0.0.1:{target_port}")
    print(f"Database File: {app.config['DATABASE_FILE']}")
    print("Press Ctrl+C to terminate.")
    print("=" * 50 + "\n")

    # Run Flask development server
    app.run(host="127.0.0.1", port=target_port, debug=False)
