"""
project_routes.py - Endpoints for project CRUD operations
"""

from flask import Blueprint, jsonify, request
from backend.models import ProjectModel
from backend.auth import admin_required

project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@project_bp.route("", methods=["GET"])
def list_projects():
    """List all projects with optional category filter (Public)."""
    category = request.args.get("category")
    projects = ProjectModel.get_all(category=category)

    # Parse tags into list for each project
    formatted = []
    for p in projects:
        item = dict(p)
        item["tag_list"] = [t.strip() for t in p["tags"].split(",") if t.strip()] if p.get("tags") else []
        formatted.append(item)

    return jsonify({"success": True, "count": len(formatted), "data": formatted})


@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Retrieve a single project by ID (Public)."""
    project = ProjectModel.get_by_id(project_id)
    if not project:
        return jsonify({"success": False, "error": "Project not found"}), 404

    item = dict(project)
    item["tag_list"] = [t.strip() for t in project["tags"].split(",") if t.strip()] if project.get("tags") else []
    return jsonify({"success": True, "data": item})


@project_bp.route("", methods=["POST"])
@admin_required
def create_project():
    """Create a new project (Admin Protected)."""
    payload = request.get_json()
    if not payload or not payload.get("title") or not payload.get("description"):
        return jsonify({"success": False, "error": "Title and description are required"}), 400

    new_project = ProjectModel.create(payload)
    return jsonify({"success": True, "message": "Project created successfully", "data": new_project}), 201


@project_bp.route("/<int:project_id>", methods=["PUT"])
@admin_required
def update_project(project_id):
    """Update an existing project (Admin Protected)."""
    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No data provided"}), 400

    existing = ProjectModel.get_by_id(project_id)
    if not existing:
        return jsonify({"success": False, "error": "Project not found"}), 404

    updated = ProjectModel.update(project_id, payload)
    return jsonify({"success": True, "message": "Project updated successfully", "data": updated})


@project_bp.route("/<int:project_id>", methods=["DELETE"])
@admin_required
def delete_project(project_id):
    """Delete a project (Admin Protected)."""
    existing = ProjectModel.get_by_id(project_id)
    if not existing:
        return jsonify({"success": False, "error": "Project not found"}), 404

    ProjectModel.delete(project_id)
    return jsonify({"success": True, "message": "Project deleted successfully"})
