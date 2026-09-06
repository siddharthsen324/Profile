"""
analytics_routes.py - Endpoints for visitor tracking and metrics summary
"""

from flask import Blueprint, jsonify, request
from backend.models import AnalyticsModel
from backend.auth import admin_required

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.route("/visit", methods=["POST"])
def log_visit():
    """Record a visitor page view (Public)."""
    payload = request.get_json() or {}
    page = payload.get("page", request.referrer or "home")
    visitor_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "Unknown")

    AnalyticsModel.log_visit(page=page, visitor_ip=visitor_ip, user_agent=user_agent)
    return jsonify({"success": True})


@analytics_bp.route("/summary", methods=["GET"])
@admin_required
def get_summary():
    """Retrieve visitor metrics and platform stats (Admin Protected)."""
    summary = AnalyticsModel.get_summary()
    return jsonify({"success": True, "data": summary})
