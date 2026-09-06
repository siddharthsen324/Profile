"""
auth.py - Authentication helper utilities, token management, and admin decorator
"""

from functools import wraps
from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.security import check_password_hash
from backend.config import SECRET_KEY, TOKEN_MAX_AGE
from backend.database import get_db_connection

serializer = URLSafeTimedSerializer(SECRET_KEY, salt="admin-auth")


def generate_token(username: str) -> str:
    """Generate a cryptographically signed timed token for the user."""
    return serializer.dumps({"username": username})


def verify_token(token: str, max_age: int = TOKEN_MAX_AGE):
    """Verify signed token signature and expiration. Returns payload dict or None."""
    if not token:
        return None
    try:
        data = serializer.loads(token, max_age=max_age)
        return data
    except (SignatureExpired, BadTimeSignature):
        return None


def get_token_from_request():
    """Extract authentication token from request headers."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()

    # Fallback to custom header or query param
    return request.headers.get("X-Admin-Token") or request.args.get("token")


def verify_user_credentials(username, password):
    """Check username and password against SQLite users table."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username.strip(),))
        user = cursor.fetchone()
        if user and check_password_hash(user["password_hash"], password):
            return user
    return None


def admin_required(f):
    """Decorator for route endpoints requiring admin authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_request()
        payload = verify_token(token)
        if not payload or not payload.get("username"):
            return jsonify({
                "success": False,
                "error": "Unauthorized. Admin authentication required."
            }), 401
        return f(*args, **kwargs)
    return decorated_function
