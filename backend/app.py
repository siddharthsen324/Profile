"""
app.py - Main Flask application factory and server
Serves the REST API under /api/* and the static frontend UI.
"""

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.config import FRONTEND_DIR, SECRET_KEY, CORS_ORIGINS
from backend.database import init_database
from backend.routes import (
    profile_bp,
    project_bp,
    skill_bp,
    contact_bp,
    analytics_bp,
    ai_bp,
    auth_bp
)


def create_app():
    """Application factory for the Developer Profile application."""
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path=""
    )

    app.config["SECRET_KEY"] = SECRET_KEY
    CORS(app, resources={r"/api/*": {
        "origins": CORS_ORIGINS,
        "allow_headers": ["Content-Type", "Authorization", "X-Admin-Token"]
    }})

    # Initialize SQLite database and seed defaults
    with app.app_context():
        init_database()

    # Register API Blueprints
    app.register_blueprint(profile_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(auth_bp)

    # Serve Frontend Pages
    @app.route("/")
    def index():
        return send_from_directory(str(FRONTEND_DIR), "index.html")

    @app.route("/login")
    @app.route("/login.html")
    def login_page():
        return send_from_directory(str(FRONTEND_DIR), "login.html")

    @app.route("/admin")
    @app.route("/admin.html")
    def admin_page():
        return send_from_directory(str(FRONTEND_DIR), "admin.html")

    @app.route("/<path:path>")
    def static_proxy(path):
        return send_from_directory(str(FRONTEND_DIR), path)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    from backend.config import HOST, PORT, DEBUG
    print(f"==================================================")
    print(f" Siddharth Sen - Developer Profile & Platform")
    print(f" Server running at: http://{HOST}:{PORT}")
    print(f" Admin Login at:     http://{HOST}:{PORT}/login.html")
    print(f" Admin Dashboard at: http://{HOST}:{PORT}/admin.html")
    print(f"==================================================")
    app.run(host=HOST, port=PORT, debug=DEBUG)
