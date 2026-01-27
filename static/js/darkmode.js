// Dark mode toggle functionality

class DarkModeManager {
    constructor() {
        this.darkMode = localStorage.getItem('darkMode') === 'true';
        this.init();
    }

    init() {
        // Apply saved preference
        if (this.darkMode) {
            this.enable();
        }

        // Create toggle button
        this.createToggleButton();
    }

    createToggleButton() {
        const toggle = document.createElement('button');
        toggle.className = 'dark-mode-toggle';
        toggle.innerHTML = this.darkMode ? '☀️' : '🌙';
        toggle.title = 'Toggle dark mode';
        toggle.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
            z-index: 1000;
            transition: all 0.3s ease;
        `;

        toggle.addEventListener('click', () => this.toggle());

        toggle.addEventListener('mouseenter', () => {
            toggle.style.transform = 'scale(1.1) rotate(15deg)';
        });

        toggle.addEventListener('mouseleave', () => {
            toggle.style.transform = 'scale(1) rotate(0deg)';
        });

        document.body.appendChild(toggle);
        this.toggleButton = toggle;
    }

    toggle() {
        this.darkMode = !this.darkMode;
        localStorage.setItem('darkMode', this.darkMode);

        if (this.darkMode) {
            this.enable();
        } else {
            this.disable();
        }

        this.toggleButton.innerHTML = this.darkMode ? '☀️' : '🌙';

        // Show toast
        if (window.showToast) {
            window.showToast(
                this.darkMode ? 'Dark mode enabled' : 'Light mode enabled',
                'info'
            );
        }
    }

    enable() {
        document.documentElement.classList.add('dark-mode');
        this.applyDarkStyles();
    }

    disable() {
        document.documentElement.classList.remove('dark-mode');
        this.removeDarkStyles();
    }

    applyDarkStyles() {
        const style = document.createElement('style');
        style.id = 'dark-mode-styles';
        style.textContent = `
            .dark-mode {
                --bg: #1a1d29;
                --bg-dark: #0f1117;
                --surface: #242938;
                --text: #e2e8f0;
                --text-light: #94a3b8;
                --text-lighter: #64748b;
            }

            .dark-mode body {
                background: var(--bg);
                color: var(--text);
            }

            .dark-mode .card {
                background: var(--surface);
                border-color: rgba(255, 255, 255, 0.1);
            }

            .dark-mode input,
            .dark-mode select,
            .dark-mode textarea {
                background: var(--bg-dark);
                color: var(--text);
                border-color: rgba(255, 255, 255, 0.1);
            }

            .dark-mode .nav-card {
                background: var(--surface);
                border-color: rgba(255, 255, 255, 0.1);
            }

            .dark-mode .nav-desc {
                color: var(--text-light);
            }

            .dark-mode .stat-label,
            .dark-mode .stat-info {
                color: var(--text-light);
            }

            .dark-mode .modal-content {
                background: var(--surface);
            }

            .dark-mode .info-box {
                background: linear-gradient(135deg, rgba(94, 96, 206, 0.2) 0%, rgba(114, 9, 183, 0.1) 100%);
                border-color: rgba(94, 96, 206, 0.3);
            }

            .dark-mode .chart-container {
                background: var(--surface);
            }

            .dark-mode .stat-card {
                background: var(--surface);
                border-color: rgba(255, 255, 255, 0.1);
            }

            .dark-mode .queue-item:hover {
                background: linear-gradient(135deg, rgba(94, 96, 206, 0.1) 0%, rgba(6, 214, 160, 0.1) 100%);
            }

            .dark-mode .upcoming-item {
                background: rgba(255, 255, 255, 0.05);
                border-color: rgba(255, 255, 255, 0.1);
            }

            .dark-mode .filter-btn {
                border-color: var(--primary);
                color: var(--primary);
            }

            .dark-mode .filter-btn:not(.active) {
                background: transparent;
            }

            /* Smooth transition */
            * {
                transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }

    removeDarkStyles() {
        const style = document.getElementById('dark-mode-styles');
        if (style) {
            style.remove();
        }
    }
}

// Initialize dark mode on page load
document.addEventListener('DOMContentLoaded', () => {
    window.darkModeManager = new DarkModeManager();
});
