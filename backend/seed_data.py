"""
seed_data.py - Default profile data for Siddharth Sen
This data pre-populates the SQLite database on first startup.
"""

DEFAULT_PROFILE = {
    "name": "Siddharth Sen",
    "title": "AIML Student & Software Developer",
    "tagline": "Passionate about AI, Machine Learning, Data Structures & Algorithms, and Frontend Development.",
    "college": "Global College",
    "specialization": "Computer Science (Artificial Intelligence & Machine Learning)",
    "degree": "B.Tech in CS (AIML)",
    "year": "2023 - Present",
    "bio_intro": "I am a Computer Science engineering student specializing in Artificial Intelligence & Machine Learning (AIML) at Global College. I am deeply interested in exploring data patterns, training smart algorithms, and writing clean, efficient code.",
    "bio_detail": "I have a strong foundation in core computer science paradigms, and I continuously seek out opportunities to learn new tech stacks and implement them in real-world environments.",
    "interests": "AI & ML, Algorithms, UI Development, OOP Design",
    "dsa_solved": 500,
    "projects_count": 4,
    "email": "siddharthsen324@gmail.com",
    "github": "https://github.com/siddharthsen324",
    "linkedin": "https://www.linkedin.com/in/siddharth-sen-572259396/",
    "location": "India",
    "avatar_url": "/assets/images/phot.jpg",
    "status": "Open to Internships & Collaborative Projects"
}

DEFAULT_SKILLS = [
    # Category: Languages & OOP
    {
        "name": "Java",
        "category": "Languages & OOP",
        "proficiency": 90,
        "icon": "terminal",
        "description": "Core Java, Multithreading, Collections Framework, OOP design patterns"
    },
    {
        "name": "C++",
        "category": "Languages & OOP",
        "proficiency": 85,
        "icon": "code-2",
        "description": "STL, memory management, algorithmic problem solving and low-level optimization"
    },
    {
        "name": "Python",
        "category": "Languages & OOP",
        "proficiency": 80,
        "icon": "binary",
        "description": "Scripting, OOP, NumPy, Pandas, Scikit-Learn, Flask, automation"
    },
    {
        "name": "Object-Oriented Programming (OOP)",
        "category": "Languages & OOP",
        "proficiency": 85,
        "icon": "box",
        "description": "Encapsulation, Inheritance, Polymorphism, Abstraction, Clean Code architecture"
    },

    # Category: Core Algorithms & AI
    {
        "name": "Data Structures & Algorithms (DSA)",
        "category": "Core Algorithms & AI",
        "proficiency": 90,
        "icon": "git-branch",
        "description": "Arrays, LinkedLists, Trees, Graphs, Dynamic Programming, Sorting & Searching"
    },
    {
        "name": "Machine Learning",
        "category": "Core Algorithms & AI",
        "proficiency": 75,
        "icon": "brain",
        "description": "Supervised & Unsupervised Learning, Regression, Classification, NLP, Model Evaluation"
    },

    # Category: Frontend & Tools
    {
        "name": "HTML & CSS",
        "category": "Frontend & Tools",
        "proficiency": 90,
        "icon": "layout",
        "description": "Semantic HTML5, CSS3, Flexbox, Grid, Glassmorphism, Responsive Web Design"
    },
    {
        "name": "JavaScript",
        "category": "Frontend & Tools",
        "proficiency": 80,
        "icon": "sparkles",
        "description": "Modern ES6+, DOM manipulation, Asynchronous JavaScript, Fetch API, Event Handling"
    },
    {
        "name": "Frontend Development",
        "category": "Frontend & Tools",
        "proficiency": 85,
        "icon": "panels-top-left",
        "description": "Building interactive single-page interfaces, mobile-friendly layouts, clean UX"
    },
    {
        "name": "Git & GitHub",
        "category": "Frontend & Tools",
        "proficiency": 85,
        "icon": "git-commit",
        "description": "Version control, branching, pull requests, collaborative workflows, repo management"
    }
]

DEFAULT_PROJECTS = [
    {
        "title": "AI Resume Analyzer",
        "category": "AI / ML",
        "description": "An intelligence-driven parsing web tool analyzing resume PDFs against custom job requirements. Provides matching scores, identifies keyword gaps, and recommends updates using Natural Language Processing models.",
        "tags": "Python, NLP, Machine Learning, Streamlit, PyPDF2",
        "github_url": "https://github.com/siddharthsen324",
        "live_url": "#",
        "featured": 1,
        "icon": "file-search"
    },
    {
        "title": "Student Management System",
        "category": "Software & Java",
        "description": "A fully featured administration application implemented in Java. Utilizes OOP concepts, core data structures, and relational storage. Allows CRUD operations, attendance logs, and GPA calculations.",
        "tags": "Java, OOP, SQLite, Data Structures, Desktop App",
        "github_url": "https://github.com/siddharthsen324",
        "live_url": "#",
        "featured": 1,
        "icon": "database"
    },
    {
        "title": "Machine Learning Prediction Project",
        "category": "AI / ML",
        "description": "A predictive regression model analyzing target outcomes based on academic and demographic inputs. Implements data scrubbing pipelines, feature scaling, model scoring, and graphical performance charts.",
        "tags": "Python, Scikit-Learn, Pandas, Matplotlib, Data Science",
        "github_url": "https://github.com/siddharthsen324",
        "live_url": "#",
        "featured": 1,
        "icon": "trending-up"
    },
    {
        "title": "Personal Portfolio & Profile Hub",
        "category": "Full Stack / Web",
        "description": "A responsive full-stack developer portfolio and management portal with SQLite-backed REST API, glassmorphism UI, real-time contact inbox, interactive AI keyword analyzer, and admin dashboard.",
        "tags": "HTML5, CSS3, JavaScript, Python, Flask, SQLite, REST API",
        "github_url": "https://github.com/siddharthsen324",
        "live_url": "#",
        "featured": 1,
        "icon": "code"
    }
]

DEFAULT_ACHIEVEMENTS = [
    {
        "title": "Regular DSA Problem Solver",
        "icon": "award",
        "description": "Consistently practice logic on LeetCode and HackerRank, sharpening knowledge of Trees, Graphs, Dynamic Programming, and Search/Sort optimization."
    },
    {
        "title": "Deep Learning & AI Exploration",
        "icon": "sparkles",
        "description": "Continuously learning new concepts, including Regression pipelines, NLP engines, Classification heuristics, and fine-tuning lightweight models."
    },
    {
        "title": "Real-World Software Crafting",
        "icon": "hammer",
        "description": "Committed to designing utility tools, structured database solutions, and intuitive web interfaces that combine analytical logic with slick frontend details."
    }
]
