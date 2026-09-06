"""
auth_routes.py - Endpoints for admin authentication (login, token verification, logout)
"""

from flask import Blueprint, jsonify, request
from backend.auth import verify_user_credentials, generate_token, verify_token, get_token_from_request

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate administrator credentials and return an authorization token."""
    payload = request.get_json() or {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "error": "Username and password are required"}), 400

    user = verify_user_credentials(username, password)
    if not user:
        return jsonify({"success": False, "error": "Invalid username or password"}), 401

    token = generate_token(username)
    return jsonify({
        "success": True,
        "message": "Authentication successful",
        "token": token,
        "user": {
            "username": user["username"]
        }
    })


@auth_bp.route("/verify", methods=["GET"])
def verify():
    """Verify if current admin token is valid."""
    token = get_token_from_request()
    payload = verify_token(token)
    if not payload or not payload.get("username"):
        return jsonify({"success": False, "authenticated": False, "error": "Invalid or expired token"}), 401

    return jsonify({
        "success": True,
        "authenticated": True,
        "user": {
            "username": payload["username"]
        }
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout endpoint."""
    return jsonify({"success": True, "message": "Logged out successfully"})
