"""
ai_routes.py - Interactive AIML endpoints showcasing Resume Keyword Analysis and Profile AI Assistant
"""

import re
from flask import Blueprint, jsonify, request
from backend.models import ProfileModel, SkillModel, ProjectModel

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

ROLE_SKILL_MAP = {
    "aiml engineer": ["python", "machine learning", "dsa", "nlp", "algorithms", "scikit-learn", "pandas"],
    "software engineer": ["java", "c++", "dsa", "oop", "algorithms", "git", "python"],
    "frontend developer": ["html", "css", "javascript", "frontend", "ui", "responsive design"],
    "full stack developer": ["java", "python", "javascript", "html", "css", "sqlite", "rest api"],
    "data scientist": ["python", "machine learning", "pandas", "algorithms", "statistics", "matplotlib"]
}


@ai_bp.route("/resume-match", methods=["POST"])
def analyze_resume_match():
    """Analyze Siddharth's skills against a provided job description or role requirements."""
    payload = request.get_json() or {}
    job_text = payload.get("job_text", "").strip()
    target_role = payload.get("target_role", "").strip().lower()

    if not job_text and not target_role:
        return jsonify({
            "success": False,
            "error": "Please provide either a target role or a job description snippet."
        }), 400

    skills = SkillModel.get_all()
    candidate_skills = [s["name"].lower() for s in skills]
    candidate_skills += ["python", "java", "c++", "dsa", "nlp", "ml", "machine learning", "sqlite", "oop", "git"]
    candidate_skills_set = set(candidate_skills)

    # Extract keywords from input
    text_to_analyze = f"{target_role} {job_text}".lower()
    words = re.findall(r"\b[a-zA-Z\+\#]{2,}\b", text_to_analyze)

    # Role specific required keywords
    required_keywords = set()
    for role, role_skills in ROLE_SKILL_MAP.items():
        if role in target_role:
            required_keywords.update(role_skills)

    if not required_keywords:
        # Generic engineering keywords from text
        tech_vocab = {
            "python", "java", "c++", "dsa", "algorithms", "data structures", "machine learning",
            "ml", "nlp", "oop", "object-oriented", "javascript", "html", "css", "git", "github",
            "sql", "sqlite", "database", "pandas", "scikit-learn", "rest api", "backend", "frontend"
        }
        for w in words:
            if w in tech_vocab:
                required_keywords.add(w)

    if not required_keywords:
        required_keywords = {"python", "java", "dsa", "oop", "machine learning"}

    # Calculate matches
    matched = []
    missing = []
    for req in required_keywords:
        if any(req in s or s in req for s in candidate_skills_set):
            matched.append(req.upper())
        else:
            missing.append(req.upper())

    match_percentage = int((len(matched) / len(required_keywords)) * 100) if required_keywords else 85
    match_percentage = min(98, max(40, match_percentage))

    verdict = (
        "Strong Candidate Fit! Siddharth possesses solid foundational and applied competencies matching these requirements."
        if match_percentage >= 75 else
        "Promising Profile: Key algorithmic and development capabilities align well."
    )

    return jsonify({
        "success": True,
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "verdict": verdict,
        "profile_summary": "AIML student at Global College with 500+ DSA problems solved and hands-on ML/software projects."
    })


@ai_bp.route("/chat", methods=["POST"])
def assistant_chat():
    """Smart knowledge assistant answering questions about Siddharth's portfolio and background."""
    payload = request.get_json() or {}
    query = payload.get("message", "").strip().lower()

    if not query:
        return jsonify({"success": False, "error": "Query message cannot be empty."}), 400

    profile = ProfileModel.get()
    skills = SkillModel.get_all()
    projects = ProjectModel.get_all()

    # Intelligent intent matching - check specific concepts first
    if any(w in query for w in ["project", "build", "portfolio", "created"]):
        project_titles = ", ".join([p["title"] for p in projects[:3]])
        reply = (
            f"Siddharth has built several impressive projects including {project_titles}. "
            "His flagship projects include an AI Resume Analyzer utilizing NLP, a robust Java Student Management System, "
            "and an ML Prediction pipeline."
        )
    elif any(w in query for w in ["skill", "stack", "language", "tech", "python", "java", "c++"]):
        top_skills = ", ".join([s["name"] for s in skills[:5]])
        reply = (
            f"Siddharth's core technical toolkit includes: {top_skills}, Object-Oriented Programming (OOP), "
            "Data Structures & Algorithms, Machine Learning, and Modern Web Development."
        )
    elif any(w in query for w in ["dsa", "leetcode", "problem", "solve", "algorithm"]):
        reply = (
            f"Siddharth is an avid problem solver with over {profile['dsa_solved']}+ DSA problems solved across LeetCode "
            "and HackerRank, emphasizing Trees, Graphs, Dynamic Programming, and Search/Sort algorithms."
        )
    elif any(w in query for w in ["contact", "hire", "email", "reach", "linkedin", "github"]):
        reply = (
            f"You can reach Siddharth directly at {profile['email']}, visit his GitHub at {profile['github']}, "
            f"or connect with him on LinkedIn ({profile['linkedin']})."
        )
    elif any(w in query for w in ["college", "education", "degree", "study", "university"]):
        reply = (
            f"Siddharth is currently pursuing his {profile['degree']} specializing in {profile['specialization']} "
            f"at {profile['college']} (2023 - Present)."
        )
    elif any(w in query for w in ["who", "about", "bio", "siddharth", "introduce"]):
        reply = (
            f"{profile['name']} is an {profile['title']} pursuing {profile['degree']} at {profile['college']}. "
            f"He specializes in {profile['specialization']} and is passionate about building intelligent ML systems "
            f"and solving complex algorithms."
        )
    else:
        reply = (
            f"Thanks for asking! Siddharth is an {profile['title']} at {profile['college']}. "
            "Feel free to ask about his Projects, DSA achievements, AI/ML skills, or how to get in touch!"
        )

    return jsonify({"success": True, "reply": reply})
