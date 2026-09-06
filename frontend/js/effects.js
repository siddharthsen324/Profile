/**
 * effects.js - Visual effects, cursor tracking, typing animations, and reveals
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Interactive Cursor Glow
    const cursorGlow = document.getElementById('cursor-glow');
    if (cursorGlow) {
        window.addEventListener('mousemove', (e) => {
            cursorGlow.style.setProperty('--mouse-x', `${e.clientX}px`);
            cursorGlow.style.setProperty('--mouse-y', `${e.clientY}px`);
        });
    }

    // 2. Header Scroll Effect
    const header = document.getElementById('header');
    if (header) {
        const handleScrollHeader = () => {
            if (window.scrollY > 40) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', handleScrollHeader);
        handleScrollHeader();
    }

    // 3. Mobile Navigation Toggle
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            const icon = navToggle.querySelector('i');
            if (icon && typeof lucide !== 'undefined') {
                if (navLinks.classList.contains('open')) {
                    icon.setAttribute('data-lucide', 'x');
                } else {
                    icon.setAttribute('data-lucide', 'menu');
                }
                lucide.createIcons();
            }
        });

        // Close on clicking nav links
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('open');
                const icon = navToggle.querySelector('i');
                if (icon && typeof lucide !== 'undefined') {
                    icon.setAttribute('data-lucide', 'menu');
                    lucide.createIcons();
                }
            });
        });
    }

    // 4. Typing Animation in Hero Subtitle
    const typedText = document.getElementById('typed-text');
    if (typedText) {
        const roles = [
            "AIML Student",
            "Software Developer",
            "DSA Enthusiast",
            "Machine Learning Engineer"
        ];
        let roleIdx = 0;
        let charIdx = 0;
        let isDeleting = false;
        const typeSpeed = 90;
        const deleteSpeed = 50;
        const delayBetween = 2000;

        function typeLoop() {
            const current = roles[roleIdx];
            if (isDeleting) {
                typedText.textContent = current.substring(0, charIdx - 1);
                charIdx--;
            } else {
                typedText.textContent = current.substring(0, charIdx + 1);
                charIdx++;
            }

            if (!isDeleting && charIdx === current.length) {
                isDeleting = true;
                setTimeout(typeLoop, delayBetween);
                return;
            } else if (isDeleting && charIdx === 0) {
                isDeleting = false;
                roleIdx = (roleIdx + 1) % roles.length;
                setTimeout(typeLoop, 400);
                return;
            }

            const speed = isDeleting ? deleteSpeed : typeSpeed;
            setTimeout(typeLoop, speed);
        }

        setTimeout(typeLoop, 500);
    }

    // 5. Scroll Reveal with Intersection Observer
    const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        reveals.forEach(el => revealObserver.observe(el));
    } else {
        reveals.forEach(el => el.classList.add('active'));
    }

    // 6. Active Section Link Spy
    const sections = document.querySelectorAll('section[id], header[id]');
    const navAnchors = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', () => {
        let current = '';
        const scrollPos = window.scrollY + 180;

        sections.forEach(sec => {
            const top = sec.offsetTop;
            const height = sec.offsetHeight;
            if (scrollPos >= top && scrollPos < top + height) {
                current = sec.getAttribute('id');
            }
        });

        navAnchors.forEach(a => {
            a.classList.remove('active');
            if (a.getAttribute('href') === `#${current}`) {
                a.classList.add('active');
            }
        });
    });
});

/**
 * Global Toast Notification Generator
 */
function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const iconName = type === 'success' ? 'check-circle' : 'alert-circle';
    toast.innerHTML = `<i data-lucide="${iconName}"></i><span>${message}</span>`;
    container.appendChild(toast);

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    setTimeout(() => toast.classList.add('show'), 50);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

window.showToast = showToast;
