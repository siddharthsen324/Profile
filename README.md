# Siddharth Sen - Full-Stack Developer Profile & Management Platform
## 🌐 Live Demo

[Visit My Portfolio](https://profile-3-mopg.onrender.com/)

A complete, production-grade, full-stack application built inside the `profile` workspace. It provides an interactive, modern public developer showcase for **Siddharth Sen** (AIML Student & Software Developer) along with a robust **Python (Flask + SQLite3) REST API** and an **Administrative Management Portal**.

All source code is fully visible, organized, and directly editable in the IDE without any external build steps or compilation overhead.

---

## 🌟 Key Features

### 1. 🎨 Modern Public Developer Showcase (`frontend/index.html`)
- **Hero & Status Showcase**: Dynamic typing role animations, live availability status dot, direct contact/project CTAs, and quick metrics (500+ DSA problems, 4+ key projects).
- **About & Dynamic Code Window**: Highlighting education at **Global College (B.Tech CS AIML)**, core paradigms, and an interactive developer code simulation.
- **Skills Matrix**: Categorized proficiencies (Languages & OOP, Core Algorithms & AI, Frontend & Tools) featuring animated percentage progress bars.
- **Interactive AI Playground**:
  - **AI Role & Resume Matcher**: Matches candidate skills against any job description or tech stack keywords with instant scoring and recommendations.
  - **Ask Siddharth's AI Assistant**: Real-time intelligent knowledge bot answering questions regarding projects, algorithms, and background.
- **Project Showcase**: Filterable gallery (AI/ML, Software & Java, Web) connecting to live GitHub repositories.
- **Real-Time Contact System**: Fully integrated form validating inputs and persisting messages directly into the SQLite database.

### 2. 🛡️ Developer Management Portal (`frontend/admin.html`)
- **Overview Dashboard**: Live statistics on Total Visits, Messages Received, Active Projects, and Tracked Skills.
- **Message Inbox**: View incoming contact inquiries with timestamps, sender details, and actions to toggle read status or delete.
- **Project Manager**: Complete CRUD operations to add, edit, or remove projects dynamically.
- **Skill Manager**: Add new skills, adjust proficiency levels (0-100%), and delete skills.
- **Profile Settings**: Live editor to update headline, tagline, bio, contact email, GitHub, and LinkedIn handles.

### 3. ⚡ Robust Python Backend REST API (`backend/`)
- **Database Layer**: SQLite (`data/profile.db`) with automatic table initialization and seeding on initial launch.
- **Clean Architecture**: Separation of concerns across `config`, `database`, `models`, and modular `routes`.
- **CORS & Static Serving**: Seamlessly serves both API endpoints and the frontend UI from a unified host.

---

## 📂 Project Architecture

```
profile/
├── backend/
│   ├── app.py                     # Flask application factory, routes & static file hosting
│   ├── config.py                  # Server configuration, paths, and environment settings
│   ├── database.py                # SQLite database connection, table schemas & auto-seeding
│   ├── models.py                  # Data access layer (Profile, Project, Skill, Message, Analytics)
│   ├── seed_data.py               # Default profile dataset for Siddharth Sen
│   ├── routes/
│   │   ├── profile_routes.py      # GET /api/profile, PUT /api/profile
│   │   ├── project_routes.py      # GET, POST, PUT, DELETE /api/projects
│   │   ├── skill_routes.py        # GET, POST, PUT, DELETE /api/skills
│   │   ├── contact_routes.py      # POST /api/contact, GET/DELETE/PATCH /api/messages
│   │   ├── analytics_routes.py    # POST /api/analytics/visit, GET /api/analytics/summary
│   │   └── ai_routes.py           # POST /api/ai/resume-match, POST /api/ai/chat
│   └── tests/
│       └── test_api.py            # Complete automated test suite (9 test cases)
├── frontend/
│   ├── index.html                 # Main public developer portfolio
│   ├── admin.html                 # Administrative management dashboard
│   ├── css/
│   │   ├── main.css               # Core styling, glassmorphism tokens, and responsive layout
│   │   ├── animations.css         # Cursor spotlight glow, ambient blobs, and keyframe animations
│   │   └── admin.css              # Dashboard layout, metrics cards, data tables & modal forms
│   ├── js/
│   │   ├── api.js                 # Centralized REST client with offline fallback support
│   │   ├── app.js                 # Public profile controller, filters & contact form
│   │   ├── admin.js               # Admin dashboard controller, inbox & CRUD operations
│   │   └── effects.js             # Spotlight cursor, typewriter animations, and toasts
│   └── assets/
│       ├── images/                # Profile photographs (phot.jpg, photo.png)
│       └── data/                  # Static fallback dataset
├── data/
│   └── profile.db                 # Auto-generated SQLite database
├── run.py                         # Unified server launcher (starts backend and opens browser)
├── start.bat                      # Windows double-click batch runner
├── start.ps1                      # Windows PowerShell runner
├── requirements.txt               # Dependencies (Flask, Flask-Cors)
└── README.md                      # Documentation & developer guide
```

---

## 🚀 How to Run the Application

### Option A: One-Click Launcher (Recommended)
Double-click `start.bat` in the project folder, or run:
```powershell
python run.py
```
This will automatically:
1. Initialize the SQLite database and seed Siddharth's default data.
2. Start the Flask server at `http://127.0.0.1:5000`.
3. Open your default web browser directly to the application.

### Option B: PowerShell
```powershell
.\start.ps1
```

---

## 🌐 URLs & Endpoints

| URL / Endpoint | Purpose |
| :--- | :--- |
| `http://127.0.0.1:5000/` | Public Developer Profile & Portfolio |
| `http://127.0.0.1:5000/admin.html` | Admin & Profile Management Dashboard |
| `GET /api/profile` | Retrieve developer profile, bio, and achievements |
| `PUT /api/profile` | Update profile information |
| `GET /api/projects` | List projects (supports `?category=AI` query filter) |
| `POST /api/projects` | Create a new project |
| `PUT /api/projects/<id>` | Update an existing project |
| `DELETE /api/projects/<id>` | Delete a project |
| `GET /api/skills` | List skills (supports `?grouped=true`) |
| `POST /api/skills` | Create a new skill |
| `PUT /api/skills/<id>` | Update an existing skill |
| `DELETE /api/skills/<id>` | Delete a skill |
| `POST /api/contact` | Submit a validated contact inquiry |
| `GET /api/messages` | View all received messages (Admin) |
| `PATCH /api/messages/<id>/read` | Mark message as read/unread |
| `DELETE /api/messages/<id>` | Delete a message |
| `POST /api/ai/resume-match` | AI match score & skill gap analysis |
| `POST /api/ai/chat` | Intelligent conversational assistant |
| `GET /api/analytics/summary` | Visitor & message counts |

---

## 🛠️ Editing Code in Your IDE

- **Changing Profile Details**: You can edit data directly from the live Admin Portal at `http://127.0.0.1:5000/admin.html`, or edit the initial dataset in [`backend/seed_data.py`](backend/seed_data.py).
- **Styling & Theme**: Modify color variables, fonts, or card layouts in [`frontend/css/main.css`](frontend/css/main.css).
- **Animations**: Customize spotlight sizing, ambient floating speeds, or typing delays in [`frontend/css/animations.css`](frontend/css/animations.css).
- **Backend Logic**: Add custom endpoints by creating blueprints in [`backend/routes/`](backend/routes/) and registering them in [`backend/app.py`](backend/app.py).

---

## 🧪 Running Automated Tests

Run the backend test suite anytime using:
```powershell
python -m unittest discover -s backend/tests -v
```
All 9 test cases will run against the API endpoints, validating database integrity, validation rules, CRUD operations, and AI responses.
