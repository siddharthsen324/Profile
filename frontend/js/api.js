/**
 * api.js - Centralized API client for communicating with the Backend REST API.
 * Includes token authorization for protected Admin routes and fallback data.
 */

const API_BASE = '/api';
const TOKEN_KEY = 'admin_token';

function getAuthToken() {
    return localStorage.getItem(TOKEN_KEY) || '';
}

function setAuthToken(token) {
    if (token) {
        localStorage.setItem(TOKEN_KEY, token);
    } else {
        localStorage.removeItem(TOKEN_KEY);
    }
}

function clearAuthToken() {
    localStorage.removeItem(TOKEN_KEY);
}

function getHeaders(customHeaders = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...customHeaders
    };
    const token = getAuthToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
}

const API = {
    /**
     * Admin Login
     */
    async login(username, password) {
        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (data.success && data.token) {
                setAuthToken(data.token);
            }
            return data;
        } catch (err) {
            console.error('Login request failed:', err);
            return { success: false, error: 'Network error during login' };
        }
    },

    /**
     * Admin Logout
     */
    async logout() {
        try {
            await fetch(`${API_BASE}/auth/logout`, {
                method: 'POST',
                headers: getHeaders()
            });
        } catch (e) {
            // Ignore error
        } finally {
            clearAuthToken();
        }
    },

    /**
     * Verify Admin Auth Token
     */
    async verifyAuth() {
        const token = getAuthToken();
        if (!token) return { success: false, authenticated: false };

        try {
            const res = await fetch(`${API_BASE}/auth/verify`, {
                method: 'GET',
                headers: getHeaders()
            });
            if (!res.ok) {
                clearAuthToken();
                return { success: false, authenticated: false };
            }
            return await res.json();
        } catch (err) {
            return { success: false, authenticated: false };
        }
    },

    /**
     * Fetch the profile data (Public)
     */
    async getProfile() {
        try {
            const res = await fetch(`${API_BASE}/profile`, { headers: getHeaders() });
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const json = await res.json();
            return json.data;
        } catch (err) {
            console.warn('API getProfile failed, attempting fallback JSON...', err);
            try {
                const fallback = await fetch('assets/data/profile_default.json');
                const fbData = await fallback.json();
                return fbData.profile;
            } catch (e) {
                console.error('All profile fetch attempts failed.', e);
                return null;
            }
        }
    },

    /**
     * Update profile data (Protected)
     */
    async updateProfile(payload) {
        const res = await fetch(`${API_BASE}/profile`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        return await res.json();
    },

    /**
     * Fetch technical skills (Public)
     */
    async getSkills(grouped = false) {
        try {
            const res = await fetch(`${API_BASE}/skills?grouped=${grouped}`, { headers: getHeaders() });
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const json = await res.json();
            return json.data;
        } catch (err) {
            console.warn('API getSkills failed:', err);
            return grouped ? {} : [];
        }
    },

    /**
     * Create a new skill (Protected)
     */
    async createSkill(data) {
        const res = await fetch(`${API_BASE}/skills`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        return await res.json();
    },

    /**
     * Update an existing skill (Protected)
     */
    async updateSkill(id, data) {
        const res = await fetch(`${API_BASE}/skills/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        return await res.json();
    },

    /**
     * Delete a skill (Protected)
     */
    async deleteSkill(id) {
        const res = await fetch(`${API_BASE}/skills/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        return await res.json();
    },

    /**
     * Fetch projects, optionally filtered by category (Public)
     */
    async getProjects(category = '') {
        try {
            const url = category ? `${API_BASE}/projects?category=${encodeURIComponent(category)}` : `${API_BASE}/projects`;
            const res = await fetch(url, { headers: getHeaders() });
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const json = await res.json();
            return json.data;
        } catch (err) {
            console.warn('API getProjects failed:', err);
            return [];
        }
    },

    /**
     * Create a project (Protected)
     */
    async createProject(data) {
        const res = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        return await res.json();
    },

    /**
     * Update a project (Protected)
     */
    async updateProject(id, data) {
        const res = await fetch(`${API_BASE}/projects/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        return await res.json();
    },

    /**
     * Delete a project (Protected)
     */
    async deleteProject(id) {
        const res = await fetch(`${API_BASE}/projects/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        return await res.json();
    },

    /**
     * Submit a contact message (Public)
     */
    async submitContact(data) {
        const res = await fetch(`${API_BASE}/contact`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        return await res.json();
    },

    /**
     * Get all received messages (Protected)
     */
    async getMessages() {
        try {
            const res = await fetch(`${API_BASE}/messages`, { headers: getHeaders() });
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            return await res.json();
        } catch (err) {
            console.warn('API getMessages failed:', err);
            return { data: [], unread_count: 0 };
        }
    },

    /**
     * Toggle read status of a message (Protected)
     */
    async toggleMessageRead(id, isRead = 1) {
        const res = await fetch(`${API_BASE}/messages/${id}/read`, {
            method: 'PATCH',
            headers: getHeaders(),
            body: JSON.stringify({ is_read: isRead })
        });
        return await res.json();
    },

    /**
     * Delete a message (Protected)
     */
    async deleteMessage(id) {
        const res = await fetch(`${API_BASE}/messages/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        return await res.json();
    },

    /**
     * Log a visitor interaction (Public)
     */
    async logVisit(page = 'home') {
        try {
            await fetch(`${API_BASE}/analytics/visit`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify({ page })
            });
        } catch (e) {
            // Silently ignore visit logging error
        }
    },

    /**
     * Fetch analytics summary (Protected)
     */
    async getAnalyticsSummary() {
        try {
            const res = await fetch(`${API_BASE}/analytics/summary`, { headers: getHeaders() });
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const json = await res.json();
            return json.data;
        } catch (err) {
            console.warn('API getAnalyticsSummary failed:', err);
            return null;
        }
    },

    /**
     * Run AI resume matcher (Public)
     */
    async runResumeMatch(payload) {
        const res = await fetch(`${API_BASE}/ai/resume-match`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        return await res.json();
    },

    /**
     * Send message to AI assistant (Public)
     */
    async sendAiChat(message) {
        const res = await fetch(`${API_BASE}/ai/chat`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ message })
        });
        return await res.json();
    }
};

window.API = API;
