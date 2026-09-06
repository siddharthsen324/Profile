"""
test_api.py - Comprehensive unit and integration test suite for profile backend & security
"""

import json
import unittest
from backend.app import create_app
from backend.config import ADMIN_USERNAME, ADMIN_PASSWORD


class TestProfileAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.auth_token = None

    def test_01_login_and_auth_verification(self):
        """Test admin login and token verification."""
        # Test invalid credentials
        res_invalid = self.client.post("/api/auth/login", json={
            "username": "wrong_user",
            "password": "wrong_password"
        })
        self.assertEqual(res_invalid.status_code, 401)

        # Test valid credentials
        res_valid = self.client.post("/api/auth/login", json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        })
        self.assertEqual(res_valid.status_code, 200)
        data = json.loads(res_valid.data)
        self.assertTrue(data["success"])
        self.assertIn("token", data)

        # Store token for subsequent protected tests
        TestProfileAPI.auth_token = data["token"]

        # Verify token validity
        res_verify = self.client.get("/api/auth/verify", headers={
            "Authorization": f"Bearer {TestProfileAPI.auth_token}"
        })
        self.assertEqual(res_verify.status_code, 200)
        verify_data = json.loads(res_verify.data)
        self.assertTrue(verify_data["authenticated"])

    def test_02_public_endpoints_accessible_without_token(self):
        """Verify public endpoints remain accessible without authentication."""
        # Profile GET
        res_prof = self.client.get("/api/profile")
        self.assertEqual(res_prof.status_code, 200)

        # Projects GET
        res_proj = self.client.get("/api/projects")
        self.assertEqual(res_proj.status_code, 200)

        # Skills GET
        res_skills = self.client.get("/api/skills")
        self.assertEqual(res_skills.status_code, 200)

        # AI Resume Match POST
        res_ai = self.client.post("/api/ai/resume-match", json={"target_role": "AI Engineer"})
        self.assertEqual(res_ai.status_code, 200)

    def test_03_protected_endpoints_reject_unauthenticated(self):
        """Verify protected endpoints return 401 Unauthorized when missing token."""
        # Protected PUT profile
        res_prof = self.client.put("/api/profile", json={"status": "Hacked"})
        self.assertEqual(res_prof.status_code, 401)

        # Protected POST project
        res_proj = self.client.post("/api/projects", json={"title": "Unauthorized", "description": "Test"})
        self.assertEqual(res_proj.status_code, 401)

        # Protected GET messages inbox
        res_msg = self.client.get("/api/messages")
        self.assertEqual(res_msg.status_code, 401)

        # Protected GET analytics summary
        res_analytics = self.client.get("/api/analytics/summary")
        self.assertEqual(res_analytics.status_code, 401)

    def test_04_update_profile_with_token(self):
        """Test updating profile information with valid Bearer token."""
        headers = {"Authorization": f"Bearer {TestProfileAPI.auth_token}"}
        update_payload = {"status": "Available for High-Impact Projects"}
        response = self.client.put("/api/profile", json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["status"], "Available for High-Impact Projects")

    def test_05_create_and_delete_project_with_token(self):
        """Test project CRUD operations with Bearer token."""
        headers = {"Authorization": f"Bearer {TestProfileAPI.auth_token}"}
        payload = {
            "title": "Automated Unit Test Project",
            "category": "Testing",
            "description": "A project created by automated tests.",
            "tags": "Python, Testing, CI/CD",
            "github_url": "https://github.com/siddharthsen324",
            "live_url": "#",
            "featured": 0
        }
        res_create = self.client.post("/api/projects", json=payload, headers=headers)
        self.assertEqual(res_create.status_code, 201)
        created_data = json.loads(res_create.data)
        project_id = created_data["data"]["id"]

        # Delete project with token
        res_delete = self.client.delete(f"/api/projects/{project_id}", headers=headers)
        self.assertEqual(res_delete.status_code, 200)

    def test_06_contact_submission_and_admin_inbox(self):
        """Test public contact submission and protected admin inbox reading."""
        # Public contact submission (no token needed)
        res_valid = self.client.post("/api/contact", json={
            "name": "Recruiter Test",
            "email": "recruiter@techcompany.com",
            "subject": "Exciting AI Opportunity",
            "message": "We would love to discuss an AI/ML developer role with you!"
        })
        self.assertEqual(res_valid.status_code, 201)
        msg_data = json.loads(res_valid.data)
        message_id = msg_data["data"]["id"]

        # Retrieve messages WITH token
        headers = {"Authorization": f"Bearer {TestProfileAPI.auth_token}"}
        res_messages = self.client.get("/api/messages", headers=headers)
        self.assertEqual(res_messages.status_code, 200)

        # Mark as read WITH token
        res_read = self.client.patch(f"/api/messages/{message_id}/read", json={"is_read": 1}, headers=headers)
        self.assertEqual(res_read.status_code, 200)

    def test_07_analytics_summary_with_token(self):
        """Test visit logging and protected summary retrieval."""
        res_log = self.client.post("/api/analytics/visit", json={"page": "home"})
        self.assertEqual(res_log.status_code, 200)

        headers = {"Authorization": f"Bearer {TestProfileAPI.auth_token}"}
        res_summary = self.client.get("/api/analytics/summary", headers=headers)
        self.assertEqual(res_summary.status_code, 200)
        summary = json.loads(res_summary.data)["data"]
        self.assertIn("total_visits", summary)

    def test_08_ai_resume_match(self):
        """Test AI resume matcher endpoint."""
        res_match = self.client.post("/api/ai/resume-match", json={
            "target_role": "AI Engineer",
            "job_text": "Looking for python and machine learning engineer with strong algorithms knowledge"
        })
        self.assertEqual(res_match.status_code, 200)
        match_data = json.loads(res_match.data)
        self.assertTrue(match_data["success"])
        self.assertGreaterEqual(match_data["match_percentage"], 50)

    def test_09_ai_chat(self):
        """Test AI knowledge assistant response."""
        res_chat = self.client.post("/api/ai/chat", json={"message": "What projects has Siddharth built?"})
        self.assertEqual(res_chat.status_code, 200)
        chat_data = json.loads(res_chat.data)
        self.assertTrue(chat_data["success"])
        self.assertIn("projects", chat_data["reply"].lower())


if __name__ == "__main__":
    unittest.main()
