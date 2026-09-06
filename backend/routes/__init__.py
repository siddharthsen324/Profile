"""
Routes package initializer
"""
from backend.routes.profile_routes import profile_bp
from backend.routes.project_routes import project_bp
from backend.routes.skill_routes import skill_bp
from backend.routes.contact_routes import contact_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.ai_routes import ai_bp
from backend.routes.auth_routes import auth_bp

__all__ = [
    "profile_bp",
    "project_bp",
    "skill_bp",
    "contact_bp",
    "analytics_bp",
    "ai_bp",
    "auth_bp"
]
