/**
 * app.js - Main Public Profile Controller
 * Dynamic data rendering, category filtering, contact form handling, and AI demos.
 */

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Log visit analytics
    if (window.API) {
        window.API.logVisit('home');
    }

    // 2. Load and render Profile Data
    await loadProfileData();

    // 3. Load and render Skills Matrix
    await loadSkillsData();

    // 4. Load and render Projects Gallery
    await loadProjectsData();

    // 5. Setup Contact Form Listener
    setupContactForm();

    // 6. Setup AI Interactive Demos
    setupAiPlayground();

    // 7. Refresh Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

/**
 * Load and render developer profile details
 */
async function loadProfileData() {
    const profile = await window.API.getProfile();
    if (!profile) return;

    // Hero Section
    setTextContent('hero-name', profile.name);
    setTextContent('profile-card-name', profile.name);
    setTextContent('hero-tagline', profile.tagline);
    setTextContent('profile-status-text', profile.status || 'Open to Opportunities');
    setTextContent('stat-dsa-count', `${profile.dsa_solved}+`);
    setTextContent('stat-projects-count', `${profile.projects_count}+`);

    // About Section
    setTextContent('about-bio-intro', profile.bio_intro);
    setTextContent('about-bio-detail', profile.bio_detail);

    // Code Box Values
    setTextContent('code-name', `"${profile.name}"`);
    setTextContent('code-college', `"${profile.college}"`);
    setTextContent('code-spec', `"${profile.specialization}"`);

    // Contact Links
    setHref('contact-email-link', `mailto:${profile.email}`, profile.email);
    setHref('contact-github-link', profile.github, 'github.com/siddharthsen324');
    setHref('contact-linkedin-link', profile.linkedin, 'linkedin.com/in/siddharth-sen-572259396');
    setHref('social-github', profile.github);
    setHref('social-linkedin', profile.linkedin);
    setHref('social-email', `mailto:${profile.email}`);
}

/**
 * Load and render technical skills grouped by category
 */
async function loadSkillsData() {
    const container = document.getElementById('skills-container');
    if (!container) return;

    const grouped = await window.API.getSkills(true);
    if (!grouped || Object.keys(grouped).length === 0) return;

    container.innerHTML = '';

    for (const [category, skills] of Object.entries(grouped)) {
        const catCard = document.createElement('div');
        catCard.className = 'skills-category glass-card reveal';

        const categoryIcon = category.includes('AI') ? 'brain' : (category.includes('Languages') ? 'terminal' : 'panels-top-left');

        let skillsHtml = '';
        skills.forEach(skill => {
            skillsHtml += `
                <div class="skill-item">
                    <div class="skill-info">
                        <span class="skill-name">${escapeHtml(skill.name)}</span>
                        <span class="skill-percentage">${skill.proficiency}%</span>
                    </div>
                    <div class="skill-bar-bg">
                        <div class="skill-bar-fill" style="width: ${skill.proficiency}%;"></div>
                    </div>
                </div>
            `;
        });

        catCard.innerHTML = `
            <h3 class="skills-category-title">
                <i data-lucide="${categoryIcon}"></i>
                <span>${escapeHtml(category)}</span>
            </h3>
            <div class="skills-list">
                ${skillsHtml}
            </div>
        `;

        container.appendChild(catCard);
    }

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

/**
 * Load and render projects with category filtering
 */
async function loadProjectsData(category = '') {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;

    const projects = await window.API.getProjects(category);
    grid.innerHTML = '';

    if (!projects || projects.length === 0) {
        grid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No projects found in this category.</p>`;
        return;
    }

    projects.forEach(p => {
        const card = document.createElement('div');
        card.className = 'project-card glass-card reveal';

        const tagsHtml = (p.tag_list || []).map(t => `<span class="project-tag">${escapeHtml(t)}</span>`).join('');
        const iconName = p.icon || (p.category.includes('AI') ? 'brain' : (p.category.includes('Java') ? 'database' : 'code'));

        card.innerHTML = `
            <div class="project-header">
                <div class="project-icon">
                    <i data-lucide="${iconName}"></i>
                </div>
                <span class="project-category-badge">${escapeHtml(p.category)}</span>
            </div>
            <div class="project-body">
                <h3 class="project-title">${escapeHtml(p.title)}</h3>
                <p class="project-desc">${escapeHtml(p.description)}</p>
                <div class="project-tags">
                    ${tagsHtml}
                </div>
            </div>
            <div class="project-footer">
                <a href="${escapeHtml(p.github_url)}" target="_blank" rel="noopener noreferrer" class="project-link">
                    <i data-lucide="github"></i> Repository
                </a>
                <a href="#contact" class="project-link">
                    <i data-lucide="external-link"></i> Inquire
                </a>
            </div>
        `;

        grid.appendChild(card);
    });

    // Setup filter button listeners once
    setupFilterButtons();

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function setupFilterButtons() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.onclick = async () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const cat = btn.getAttribute('data-category');
            await loadProjectsData(cat);
        };
    });
}

/**
 * Handle Contact Form submission
 */
function setupContactForm() {
    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnHtml = submitBtn.innerHTML;

        const payload = {
            name: document.getElementById('form-name').value.trim(),
            email: document.getElementById('form-email').value.trim(),
            subject: document.getElementById('form-subject').value.trim(),
            message: document.getElementById('form-message').value.trim()
        };

        try {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span>Sending...</span>`;

            const res = await window.API.submitContact(payload);

            if (res.success) {
                showToast(res.message || 'Message sent successfully!', 'success');
                form.reset();
            } else {
                const errorMsg = res.errors ? res.errors.join(', ') : (res.error || 'Failed to send message');
                showToast(errorMsg, 'error');
            }
        } catch (err) {
            showToast('Unable to connect to the backend server.', 'error');
            console.error('Contact submission error:', err);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHtml;
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    });
}

/**
 * Setup Interactive AI Playground (Resume Matcher & Assistant Chat)
 */
function setupAiPlayground() {
    // 1. Resume Matcher
    const matchBtn = document.getElementById('ai-match-btn');
    if (matchBtn) {
        matchBtn.addEventListener('click', async () => {
            const role = document.getElementById('ai-match-role').value.trim();
            const jobText = document.getElementById('ai-match-desc').value.trim();
            const resultBox = document.getElementById('ai-match-result');

            if (!role && !jobText) {
                showToast('Please enter a role or job requirements.', 'error');
                return;
            }

            matchBtn.disabled = true;
            matchBtn.innerHTML = `<span>Analyzing...</span>`;

            try {
                const res = await window.API.runResumeMatch({ target_role: role, job_text: jobText });
                if (res.success) {
                    resultBox.style.display = 'block';
                    document.getElementById('ai-match-score').textContent = `${res.match_percentage}%`;
                    document.getElementById('ai-match-verdict').textContent = res.verdict;

                    const matchedChips = (res.matched_skills || []).map(s => `<span class="tag-pill" style="color:var(--accent-green);">${s}</span>`).join(' ');
                    document.getElementById('ai-matched-skills').innerHTML = matchedChips || '<span>Baseline Match</span>';
                }
            } catch (e) {
                showToast('Failed to run AI Match analysis', 'error');
            } finally {
                matchBtn.disabled = false;
                matchBtn.innerHTML = `<span>Run AI Match</span><i data-lucide="sparkles"></i>`;
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }
        });
    }

    // 2. AI Assistant Chat
    const chatBtn = document.getElementById('ai-chat-btn');
    const chatInput = document.getElementById('ai-chat-input');
    if (chatBtn && chatInput) {
        const sendChat = async () => {
            const msg = chatInput.value.trim();
            if (!msg) return;

            const responseBox = document.getElementById('ai-chat-response');
            chatBtn.disabled = true;
            responseBox.style.display = 'block';
            responseBox.innerHTML = '<span style="color:var(--text-muted);">Thinking...</span>';

            try {
                const res = await window.API.sendAiChat(msg);
                if (res.success) {
                    responseBox.innerHTML = `<p style="color:var(--text-primary); font-size:0.95rem;">${escapeHtml(res.reply)}</p>`;
                }
            } catch (e) {
                responseBox.innerHTML = '<span style="color:#ef4444;">Could not reach AI assistant.</span>';
            } finally {
                chatBtn.disabled = false;
            }
        };

        chatBtn.addEventListener('click', sendChat);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendChat();
        });
    }
}

// Helper utility functions
function setTextContent(id, text) {
    const el = document.getElementById(id);
    if (el && text !== undefined) el.textContent = text;
}

function setHref(id, href, text) {
    const el = document.getElementById(id);
    if (el) {
        el.href = href;
        if (text) el.textContent = text;
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
