"""
contact_routes.py - Endpoints for contact form submissions and message management
"""

import re
from flask import Blueprint, jsonify, request
from backend.models import MessageModel
from backend.auth import admin_required

contact_bp = Blueprint("contact", __name__, url_prefix="/api")

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


@contact_bp.route("/contact", methods=["POST"])
def submit_contact():
    """Submit a contact message from the public portfolio (Public)."""
    payload = request.get_json()
    if not payload:
        return jsonify({"success": False, "error": "No data provided"}), 400

    name = payload.get("name", "").strip()
    email = payload.get("email", "").strip()
    subject = payload.get("subject", "").strip()
    message = payload.get("message", "").strip()

    errors = []
    if not name or len(name) < 2:
        errors.append("Name must be at least 2 characters")
    if not email or not re.match(EMAIL_REGEX, email):
        errors.append("A valid email address is required")
    if not subject or len(subject) < 3:
        errors.append("Subject must be at least 3 characters")
    if not message or len(message) < 5:
        errors.append("Message must be at least 5 characters")

    if errors:
        return jsonify({"success": False, "errors": errors}), 422

    new_message = MessageModel.create(name=name, email=email, subject=subject, message=message)
    return jsonify({
        "success": True,
        "message": f"Thank you {name}! Your message has been received and saved.",
        "data": new_message
    }), 201


@contact_bp.route("/messages", methods=["GET"])
@admin_required
def list_messages():
    """Retrieve all received messages (Admin Protected)."""
    messages = MessageModel.get_all()
    unread_count = MessageModel.get_unread_count()
    return jsonify({
        "success": True,
        "count": len(messages),
        "unread_count": unread_count,
        "data": messages
    })


@contact_bp.route("/messages/<int:message_id>/read", methods=["PATCH"])
@admin_required
def toggle_message_read(message_id):
    """Mark a message as read or unread (Admin Protected)."""
    payload = request.get_json() or {}
    is_read = payload.get("is_read", 1)
    updated = MessageModel.mark_as_read(message_id, is_read=is_read)
    if not updated:
        return jsonify({"success": False, "error": "Message not found"}), 404
    return jsonify({"success": True, "data": updated})


@contact_bp.route("/messages/<int:message_id>", methods=["DELETE"])
@admin_required
def delete_message(message_id):
    """Delete a message (Admin Protected)."""
    deleted = MessageModel.delete(message_id)
    if not deleted:
        return jsonify({"success": False, "error": "Message not found"}), 404
    return jsonify({"success": True, "message": "Message deleted successfully"})
