"""
database.py - SQLite database management, schema creation, user auth table, and seeding
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from werkzeug.security import generate_password_hash
from backend.config import DB_PATH, ADMIN_USERNAME, ADMIN_PASSWORD
from backend.seed_data import DEFAULT_PROFILE, DEFAULT_SKILLS, DEFAULT_PROJECTS


def dict_factory(cursor, row):
    """Convert SQLite row to Python dictionary."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@contextmanager
def get_db_connection():
    """Context manager for SQLite connections with row-to-dict factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Create tables if they do not exist and seed default profile & admin user data."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Profile table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                tagline TEXT,
                college TEXT,
                specialization TEXT,
                degree TEXT,
                year TEXT,
                bio_intro TEXT,
                bio_detail TEXT,
                interests TEXT,
                dsa_solved INTEGER DEFAULT 500,
                projects_count INTEGER DEFAULT 4,
                email TEXT,
                github TEXT,
                linkedin TEXT,
                location TEXT,
                avatar_url TEXT,
                status TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                proficiency INTEGER NOT NULL CHECK(proficiency >= 0 AND proficiency <= 100),
                icon TEXT DEFAULT 'code',
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 3. Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                tags TEXT,
                github_url TEXT,
                live_url TEXT,
                featured INTEGER DEFAULT 1,
                icon TEXT DEFAULT 'code',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 4. Messages (Contact submissions) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 5. Visitor Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page TEXT NOT NULL,
                visitor_ip TEXT,
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 6. Admin Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Ensure default admin user exists
        cursor.execute("SELECT * FROM users WHERE username = ?;", (ADMIN_USERNAME,))
        if not cursor.fetchone():
            hashed_pw = generate_password_hash(ADMIN_PASSWORD)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?);", (ADMIN_USERNAME, hashed_pw))

        # Seed data if profile table is empty
        cursor.execute("SELECT COUNT(*) as count FROM profile;")
        if cursor.fetchone()["count"] == 0:
            seed_database(cursor)


def seed_database(cursor):
    """Populate database with default data from seed_data.py."""
    # Insert Profile
    cursor.execute("""
        INSERT INTO profile (
            name, title, tagline, college, specialization, degree, year,
            bio_intro, bio_detail, interests, dsa_solved, projects_count,
            email, github, linkedin, location, avatar_url, status
        ) VALUES (
            :name, :title, :tagline, :college, :specialization, :degree, :year,
            :bio_intro, :bio_detail, :interests, :dsa_solved, :projects_count,
            :email, :github, :linkedin, :location, :avatar_url, :status
        )
    """, DEFAULT_PROFILE)

    # Insert Skills
    for skill in DEFAULT_SKILLS:
        cursor.execute("""
            INSERT INTO skills (name, category, proficiency, icon, description)
            VALUES (:name, :category, :proficiency, :icon, :description)
        """, skill)

    # Insert Projects
    for project in DEFAULT_PROJECTS:
        cursor.execute("""
            INSERT INTO projects (title, category, description, tags, github_url, live_url, featured, icon)
            VALUES (:title, :category, :description, :tags, :github_url, :live_url, :featured, :icon)
        """, project)
