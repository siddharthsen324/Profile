/**
 * admin.js - Management Portal Controller
 * Full CRUD for Projects, Skills, Messages, and Profile Settings.
 */

document.addEventListener('DOMContentLoaded', async () => {
    // 0. Enforce Admin Authentication Guard
    const authCheck = await window.API.verifyAuth();
    if (!authCheck || !authCheck.authenticated) {
        window.location.href = 'login.html';
        return;
    }

    // Setup Logout handler
    const logoutBtn = document.getElementById('admin-logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await window.API.logout();
            window.location.href = 'login.html';
        });
    }

    // 1. Navigation tabs
    setupAdminNavigation();

    // 2. Load overview metrics
    await loadMetrics();

    // 3. Load tables
    await loadMessagesTable();
    await loadProjectsTable();
    await loadSkillsTable();
    await loadProfileForm();

    // 4. Setup modal actions
    setupModals();

    // 5. Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

/**
 * Switch tabs in the admin panel
 */
function setupAdminNavigation() {
    const navLinks = document.querySelectorAll('.admin-nav-item a');
    const panels = document.querySelectorAll('.admin-panel');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('data-tab');
            if (!targetId) return; // For external links like 'View Site'

            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            link.classList.add('active');
            const targetPanel = document.getElementById(`panel-${targetId}`);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });
}

/**
 * Load dashboard metrics
 */
async function loadMetrics() {
    const summary = await window.API.getAnalyticsSummary();
    if (!summary) return;

    document.getElementById('metric-visits').textContent = summary.total_visits || 0;
    document.getElementById('metric-messages').textContent = summary.total_messages || 0;
    document.getElementById('metric-projects').textContent = summary.total_projects || 0;
    document.getElementById('metric-skills').textContent = summary.total_skills || 0;

    // Update unread badge in sidebar
    const badge = document.getElementById('unread-badge');
    if (badge) {
        badge.textContent = summary.unread_messages || 0;
        badge.style.display = summary.unread_messages > 0 ? 'inline-block' : 'none';
    }
}

/**
 * Load received contact messages
 */
async function loadMessagesTable() {
    const res = await window.API.getMessages();
    const tbody = document.getElementById('messages-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    const messages = res.data || [];

    if (messages.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-muted); padding:2rem;">No messages in inbox.</td></tr>`;
        return;
    }

    messages.forEach(msg => {
        const tr = document.createElement('tr');
        const statusBadge = msg.is_read
            ? `<span class="badge-read">Read</span>`
            : `<span class="badge-unread">New</span>`;

        tr.innerHTML = `
            <td>${statusBadge}</td>
            <td><strong>${escapeHtml(msg.name)}</strong></td>
            <td><a href="mailto:${escapeHtml(msg.email)}" style="color:var(--accent-blue);">${escapeHtml(msg.email)}</a></td>
            <td>${escapeHtml(msg.subject)}</td>
            <td style="max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${escapeHtml(msg.message)}</td>
            <td>
                <div style="display:flex; gap:6px;">
                    <button class="btn-icon-action" title="Toggle Read" onclick="toggleRead(${msg.id}, ${msg.is_read ? 0 : 1})">
                        <i data-lucide="${msg.is_read ? 'mail-open' : 'mail'}"></i>
                    </button>
                    <button class="btn-icon-action delete" title="Delete" onclick="deleteMessage(${msg.id})">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

/**
 * Load projects into admin table
 */
async function loadProjectsTable() {
    const projects = await window.API.getProjects();
    const tbody = document.getElementById('projects-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    projects.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${escapeHtml(p.title)}</strong></td>
            <td><span class="tag-pill">${escapeHtml(p.category)}</span></td>
            <td>${escapeHtml(p.tags)}</td>
            <td>
                <div style="display:flex; gap:6px;">
                    <button class="btn-icon-action" title="Edit" onclick="openEditProjectModal(${p.id})">
                        <i data-lucide="edit-3"></i>
                    </button>
                    <button class="btn-icon-action delete" title="Delete" onclick="deleteProject(${p.id})">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

/**
 * Load skills into admin table
 */
async function loadSkillsTable() {
    const skills = await window.API.getSkills();
    const tbody = document.getElementById('skills-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';
    skills.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${escapeHtml(s.name)}</strong></td>
            <td><span class="tag-pill">${escapeHtml(s.category)}</span></td>
            <td>
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:70px; height:6px; background:rgba(255,255,255,0.1); border-radius:99px; overflow:hidden;">
                        <div style="width:${s.proficiency}%; height:100%; background:var(--gradient-primary);"></div>
                    </div>
                    <span>${s.proficiency}%</span>
                </div>
            </td>
            <td>
                <div style="display:flex; gap:6px;">
                    <button class="btn-icon-action" title="Edit" onclick="openEditSkillModal(${s.id})">
                        <i data-lucide="edit-3"></i>
                    </button>
                    <button class="btn-icon-action delete" title="Delete" onclick="deleteSkill(${s.id})">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });

    if (typeof lucide !== 'undefined') lucide.createIcons();
}

/**
 * Load profile info into edit form
 */
async function loadProfileForm() {
    const profile = await window.API.getProfile();
    if (!profile) return;

    document.getElementById('edit-name').value = profile.name || '';
    document.getElementById('edit-title').value = profile.title || '';
    document.getElementById('edit-tagline').value = profile.tagline || '';
    document.getElementById('edit-college').value = profile.college || '';
    document.getElementById('edit-specialization').value = profile.specialization || '';
    document.getElementById('edit-status').value = profile.status || '';
    document.getElementById('edit-email').value = profile.email || '';
    document.getElementById('edit-github').value = profile.github || '';
    document.getElementById('edit-linkedin').value = profile.linkedin || '';
    document.getElementById('edit-bio-intro').value = profile.bio_intro || '';
    document.getElementById('edit-bio-detail').value = profile.bio_detail || '';
}

/**
 * Handle saving profile settings
 */
document.getElementById('profile-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('edit-name').value,
        title: document.getElementById('edit-title').value,
        tagline: document.getElementById('edit-tagline').value,
        college: document.getElementById('edit-college').value,
        specialization: document.getElementById('edit-specialization').value,
        status: document.getElementById('edit-status').value,
        email: document.getElementById('edit-email').value,
        github: document.getElementById('edit-github').value,
        linkedin: document.getElementById('edit-linkedin').value,
        bio_intro: document.getElementById('edit-bio-intro').value,
        bio_detail: document.getElementById('edit-bio-detail').value
    };

    const res = await window.API.updateProfile(payload);
    if (res.success) {
        showToast('Profile updated successfully!', 'success');
    } else {
        showToast(res.error || 'Failed to update profile', 'error');
    }
});

/**
 * Message Actions
 */
window.toggleRead = async (id, isRead) => {
    await window.API.toggleMessageRead(id, isRead);
    await loadMessagesTable();
    await loadMetrics();
};

window.deleteMessage = async (id) => {
    if (!confirm('Are you sure you want to delete this message?')) return;
    await window.API.deleteMessage(id);
    showToast('Message deleted', 'success');
    await loadMessagesTable();
    await loadMetrics();
};

/**
 * Project Actions
 */
window.deleteProject = async (id) => {
    if (!confirm('Delete this project?')) return;
    await window.API.deleteProject(id);
    showToast('Project deleted', 'success');
    await loadProjectsTable();
    await loadMetrics();
};

window.openAddProjectModal = () => {
    document.getElementById('project-modal-title').textContent = 'Add New Project';
    document.getElementById('project-form').reset();
    document.getElementById('project-id').value = '';
    document.getElementById('project-modal').classList.add('open');
};

window.openEditProjectModal = async (id) => {
    const projects = await window.API.getProjects();
    const p = projects.find(item => item.id === id);
    if (!p) return;

    document.getElementById('project-modal-title').textContent = 'Edit Project';
    document.getElementById('project-id').value = p.id;
    document.getElementById('project-title-input').value = p.title;
    document.getElementById('project-category-input').value = p.category;
    document.getElementById('project-tags-input').value = p.tags;
    document.getElementById('project-desc-input').value = p.description;
    document.getElementById('project-github-input').value = p.github_url;
    document.getElementById('project-modal').classList.add('open');
};

/**
 * Skill Actions
 */
window.deleteSkill = async (id) => {
    if (!confirm('Delete this skill?')) return;
    await window.API.deleteSkill(id);
    showToast('Skill deleted', 'success');
    await loadSkillsTable();
    await loadMetrics();
};

window.openAddSkillModal = () => {
    document.getElementById('skill-modal-title').textContent = 'Add New Skill';
    document.getElementById('skill-form').reset();
    document.getElementById('skill-id').value = '';
    document.getElementById('skill-modal').classList.add('open');
};

window.openEditSkillModal = async (id) => {
    const skills = await window.API.getSkills();
    const s = skills.find(item => item.id === id);
    if (!s) return;

    document.getElementById('skill-modal-title').textContent = 'Edit Skill';
    document.getElementById('skill-id').value = s.id;
    document.getElementById('skill-name-input').value = s.name;
    document.getElementById('skill-category-input').value = s.category;
    document.getElementById('skill-prof-input').value = s.proficiency;
    document.getElementById('skill-modal').classList.add('open');
};

/**
 * Modals setup
 */
function setupModals() {
    // Close modal on close button or background click
    document.querySelectorAll('.modal-close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
        });
    });

    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('open');
        });
    });

    // Save project form
    document.getElementById('project-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('project-id').value;
        const payload = {
            title: document.getElementById('project-title-input').value.trim(),
            category: document.getElementById('project-category-input').value.trim(),
            tags: document.getElementById('project-tags-input').value.trim(),
            description: document.getElementById('project-desc-input').value.trim(),
            github_url: document.getElementById('project-github-input').value.trim()
        };

        if (id) {
            await window.API.updateProject(id, payload);
            showToast('Project updated!', 'success');
        } else {
            await window.API.createProject(payload);
            showToast('Project created!', 'success');
        }

        document.getElementById('project-modal').classList.remove('open');
        await loadProjectsTable();
        await loadMetrics();
    });

    // Save skill form
    document.getElementById('skill-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('skill-id').value;
        const payload = {
            name: document.getElementById('skill-name-input').value.trim(),
            category: document.getElementById('skill-category-input').value.trim(),
            proficiency: parseInt(document.getElementById('skill-prof-input').value, 10)
        };

        if (id) {
            await window.API.updateSkill(id, payload);
            showToast('Skill updated!', 'success');
        } else {
            await window.API.createSkill(payload);
            showToast('Skill created!', 'success');
        }

        document.getElementById('skill-modal').classList.remove('open');
        await loadSkillsTable();
        await loadMetrics();
    });
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
