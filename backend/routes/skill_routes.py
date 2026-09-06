"""
skill_routes.py - Endpoints for technical skills CRUD operations
"""

from flask import Blueprint, jsonify, request
from backend.models import SkillModel
from backend.auth import admin_required

skill_bp = Blueprint("skills", __name__, url_prefix="/api/skills")


@skill_bp.route("", methods=["GET"])
def list_skills():
    """List all skills, optionally grouped by category (Public)."""
    grouped = request.args.get("grouped", "false").lower() in ("true", "1")
    if grouped:
        data = SkillModel.get_grouped()
    else:
        data = SkillModel.get_all()
    return jsonify({"success": True, "data": data})


@skill_bp.route("/<int:skill_id>", methods=["GET"])
def get_skill(skill_id):
    """Retrieve a single skill by ID (Public)."""
    skill = SkillModel.get_by_id(skill_id)
    if not skill:
        return jsonify({"success": False, "error": "Skill not found"}), 404
    return jsonify({"success": True, "data": skill})


@skill_bp.route("", methods=["POST"])
@admin_required
def create_skill():
    """Create a new skill (Admin Protected)."""
    payload = request.get_json()
    if not payload or not payload.get("name") or not payload.get("category"):
        return jsonify({"success": False, "error": "Name and category are required"}), 400

    new_skill = SkillModel.create(payload)
    return jsonify({"success": True, "message": "Skill created successfully", "data": new_skill}), 201


@skill_bp.route("/<int:skill_id>", methods=["PUT"])
@admin_required
def update_skill(skill_id):
    """Update an existing skill (Admin Protected)."""
    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No data provided"}), 400

    existing = SkillModel.get_by_id(skill_id)
    if not existing:
        return jsonify({"success": False, "error": "Skill not found"}), 404

    updated = SkillModel.update(skill_id, payload)
    return jsonify({"success": True, "message": "Skill updated successfully", "data": updated})


@skill_bp.route("/<int:skill_id>", methods=["DELETE"])
@admin_required
def delete_skill(skill_id):
    """Delete a skill (Admin Protected)."""
    existing = SkillModel.get_by_id(skill_id)
    if not existing:
        return jsonify({"success": False, "error": "Skill not found"}), 404

    SkillModel.delete(skill_id)
    return jsonify({"success": True, "message": "Skill deleted successfully"})
