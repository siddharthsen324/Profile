"""
models.py - Data access layer for Profile, Projects, Skills, Messages, and Analytics
"""

from datetime import datetime, timezone
from backend.database import get_db_connection



class ProfileModel:
    @staticmethod
    def get():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM profile ORDER BY id ASC LIMIT 1;")
            return cursor.fetchone()

    @staticmethod
    def update(data):
        allowed_fields = [
            "name", "title", "tagline", "college", "specialization", "degree",
            "year", "bio_intro", "bio_detail", "interests", "dsa_solved",
            "projects_count", "email", "github", "linkedin", "location",
            "avatar_url", "status"
        ]
        updates = {k: v for k, v in data.items() if k in allowed_fields}
        if not updates:
            return ProfileModel.get()

        set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
        updates["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = f"UPDATE profile SET {set_clause}, updated_at = :updated_at WHERE id = (SELECT id FROM profile ORDER BY id ASC LIMIT 1);"
            cursor.execute(query, updates)
        return ProfileModel.get()


class ProjectModel:
    @staticmethod
    def get_all(category=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if category and category.lower() != "all":
                cursor.execute(
                    "SELECT * FROM projects WHERE LOWER(category) LIKE ? ORDER BY featured DESC, id DESC;",
                    (f"%{category.lower()}%",)
                )
            else:
                cursor.execute("SELECT * FROM projects ORDER BY featured DESC, id DESC;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(project_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?;", (project_id,))
            return cursor.fetchone()

    @staticmethod
    def create(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO projects (title, category, description, tags, github_url, live_url, featured, icon)
                VALUES (:title, :category, :description, :tags, :github_url, :live_url, :featured, :icon);
            """, {
                "title": data.get("title", "Untitled Project"),
                "category": data.get("category", "General"),
                "description": data.get("description", ""),
                "tags": data.get("tags", ""),
                "github_url": data.get("github_url", ""),
                "live_url": data.get("live_url", ""),
                "featured": int(data.get("featured", 1)),
                "icon": data.get("icon", "code")
            })
            new_id = cursor.lastrowid
        return ProjectModel.get_by_id(new_id)

    @staticmethod
    def update(project_id, data):
        allowed = ["title", "category", "description", "tags", "github_url", "live_url", "featured", "icon"]
        updates = {k: v for k, v in data.items() if k in allowed}
        if not updates:
            return ProjectModel.get_by_id(project_id)

        set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
        updates["id"] = project_id

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE projects SET {set_clause} WHERE id = :id;", updates)
        return ProjectModel.get_by_id(project_id)

    @staticmethod
    def delete(project_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?;", (project_id,))
            return cursor.rowcount > 0


class SkillModel:
    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skills ORDER BY category ASC, proficiency DESC;")
            return cursor.fetchall()

    @staticmethod
    def get_grouped():
        skills = SkillModel.get_all()
        grouped = {}
        for skill in skills:
            cat = skill["category"]
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(skill)
        return grouped

    @staticmethod
    def get_by_id(skill_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skills WHERE id = ?;", (skill_id,))
            return cursor.fetchone()

    @staticmethod
    def create(data):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO skills (name, category, proficiency, icon, description)
                VALUES (:name, :category, :proficiency, :icon, :description);
            """, {
                "name": data.get("name", "New Skill"),
                "category": data.get("category", "General"),
                "proficiency": min(100, max(0, int(data.get("proficiency", 80)))),
                "icon": data.get("icon", "code"),
                "description": data.get("description", "")
            })
            new_id = cursor.lastrowid
        return SkillModel.get_by_id(new_id)

    @staticmethod
    def update(skill_id, data):
        allowed = ["name", "category", "proficiency", "icon", "description"]
        updates = {k: v for k, v in data.items() if k in allowed}
        if "proficiency" in updates:
            updates["proficiency"] = min(100, max(0, int(updates["proficiency"])))
        if not updates:
            return SkillModel.get_by_id(skill_id)

        set_clause = ", ".join([f"{k} = :{k}" for k in updates.keys()])
        updates["id"] = skill_id

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE skills SET {set_clause} WHERE id = :id;", updates)
        return SkillModel.get_by_id(skill_id)

    @staticmethod
    def delete(skill_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM skills WHERE id = ?;", (skill_id,))
            return cursor.rowcount > 0


class MessageModel:
    @staticmethod
    def create(name, email, subject, message):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO messages (name, email, subject, message, is_read)
                VALUES (?, ?, ?, ?, 0);
            """, (name.strip(), email.strip(), subject.strip(), message.strip()))
            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM messages WHERE id = ?;", (new_id,))
            return cursor.fetchone()

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages ORDER BY id DESC;")
            return cursor.fetchall()

    @staticmethod
    def mark_as_read(message_id, is_read=1):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE messages SET is_read = ? WHERE id = ?;", (int(is_read), message_id))
            cursor.execute("SELECT * FROM messages WHERE id = ?;", (message_id,))
            return cursor.fetchone()

    @staticmethod
    def delete(message_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE id = ?;", (message_id,))
            return cursor.rowcount > 0

    @staticmethod
    def get_unread_count():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM messages WHERE is_read = 0;")
            row = cursor.fetchone()
            return row["count"] if row else 0


class AnalyticsModel:
    @staticmethod
    def log_visit(page, visitor_ip=None, user_agent=None):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analytics (page, visitor_ip, user_agent)
                VALUES (?, ?, ?);
            """, (page, visitor_ip, user_agent))

    @staticmethod
    def get_summary():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total_visits FROM analytics;")
            total_visits = cursor.fetchone()["total_visits"]

            cursor.execute("SELECT COUNT(DISTINCT visitor_ip) as unique_visitors FROM analytics;")
            unique_visitors = cursor.fetchone()["unique_visitors"]

            cursor.execute("SELECT COUNT(*) as total_messages FROM messages;")
            total_messages = cursor.fetchone()["total_messages"]

            cursor.execute("SELECT COUNT(*) as unread_messages FROM messages WHERE is_read = 0;")
            unread_messages = cursor.fetchone()["unread_messages"]

            cursor.execute("SELECT COUNT(*) as total_projects FROM projects;")
            total_projects = cursor.fetchone()["total_projects"]

            cursor.execute("SELECT COUNT(*) as total_skills FROM skills;")
            total_skills = cursor.fetchone()["total_skills"]

            cursor.execute("SELECT page, COUNT(*) as hits FROM analytics GROUP BY page ORDER BY hits DESC LIMIT 5;")
            top_pages = cursor.fetchall()

            return {
                "total_visits": total_visits,
                "unique_visitors": unique_visitors,
                "total_messages": total_messages,
                "unread_messages": unread_messages,
                "total_projects": total_projects,
                "total_skills": total_skills,
                "top_pages": top_pages
            }
