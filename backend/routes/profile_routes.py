"""
profile_routes.py - Endpoints for managing profile data
"""

from flask import Blueprint, jsonify, request
from backend.models import ProfileModel
from backend.seed_data import DEFAULT_ACHIEVEMENTS
from backend.auth import admin_required

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("", methods=["GET"])
def get_profile():
    """Retrieve the developer profile (Public)."""
    profile = ProfileModel.get()
    if not profile:
        return jsonify({"success": False, "error": "Profile not found"}), 404

    # Format interests as a list for convenience
    interests_list = [i.strip() for i in profile["interests"].split(",")] if profile.get("interests") else []
    data = dict(profile)
    data["interests_list"] = interests_list
    data["achievements"] = DEFAULT_ACHIEVEMENTS

    return jsonify({"success": True, "data": data})


@profile_bp.route("", methods=["PUT"])
@admin_required
def update_profile():
    """Update profile information (Admin Protected)."""
    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No data provided"}), 400

    updated = ProfileModel.update(payload)
    return jsonify({"success": True, "message": "Profile updated successfully", "data": updated})
