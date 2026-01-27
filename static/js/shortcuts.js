// Keyboard shortcuts for faster navigation and actions

class KeyboardShortcuts {
    constructor() {
        this.shortcuts = {
            // Navigation
            'h': () => window.location.href = '/',
            'r': () => window.location.href = '/reception',
            'd': () => window.location.href = '/doctor',
            'p': () => window.location.href = '/display',
            's': () => window.location.href = '/statistics',

            // Actions (with Ctrl/Cmd)
            'n': (e) => {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.callNextPatient();
                }
            },
            'k': (e) => {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.toggleDarkMode();
                }
            },
            'm': (e) => {
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.toggleSound();
                }
            },
            '?': () => this.showHelp()
        };

        this.init();
    }

    init() {
        document.addEventListener('keydown', (e) => {
            // Ignore if typing in input
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            const key = e.key.toLowerCase();
            if (this.shortcuts[key]) {
                this.shortcuts[key](e);
            }
        });

        // Add help button
        this.createHelpButton();
    }

    createHelpButton() {
        const helpBtn = document.createElement('button');
        helpBtn.innerHTML = '⌨️';
        helpBtn.title = 'Keyboard shortcuts (?)';
        helpBtn.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 6rem;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6b9d 0%, #f72585 100%);
            color: white;
            border: none;
            font-size: 1.3rem;
            cursor: pointer;
            box-shadow: 0 4px 16px rgba(255, 107, 157, 0.3);
            z-index: 1000;
            transition: all 0.3s ease;
        `;

        helpBtn.addEventListener('click', () => this.showHelp());
        helpBtn.addEventListener('mouseenter', () => {
            helpBtn.style.transform = 'scale(1.1)';
        });
        helpBtn.addEventListener('mouseleave', () => {
            helpBtn.style.transform = 'scale(1)';
        });

        document.body.appendChild(helpBtn);
    }

    showHelp() {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        `;

        modal.innerHTML = `
            <div style="
                background: white;
                padding: 2.5rem;
                border-radius: 1.5rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 24px 64px rgba(0, 0, 0, 0.3);
            ">
                <h2 style="margin-bottom: 1.5rem; font-size: 1.8rem; color: #1a202c;">⌨️ Keyboard Shortcuts</h2>
                
                <div style="margin-bottom: 2rem;">
                    <h3 style="font-size: 1.1rem; color: #5e60ce; margin-bottom: 1rem;">Navigation</h3>
                    <div style="display: grid; gap: 0.75rem;">
                        ${this.createShortcutRow('H', 'Go to Home')}
                        ${this.createShortcutRow('R', 'Go to Reception')}
                        ${this.createShortcutRow('D', 'Go to Doctor Dashboard')}
                        ${this.createShortcutRow('P', 'Go to Public Display')}
                        ${this.createShortcutRow('S', 'Go to Statistics')}
                    </div>
                </div>

                <div style="margin-bottom: 2rem;">
                    <h3 style="font-size: 1.1rem; color: #5e60ce; margin-bottom: 1rem;">Actions</h3>
                    <div style="display: grid; gap: 0.75rem;">
                        ${this.createShortcutRow('Ctrl + N', 'Call Next Patient')}
                        ${this.createShortcutRow('Ctrl + K', 'Toggle Dark Mode')}
                        ${this.createShortcutRow('Ctrl + M', 'Toggle Sound')}
                        ${this.createShortcutRow('?', 'Show This Help')}
                    </div>
                </div>

                <button onclick="this.parentElement.parentElement.remove()" style="
                    width: 100%;
                    padding: 0.875rem;
                    background: linear-gradient(135deg, #5e60ce 0%, #7209b7 100%);
                    color: white;
                    border: none;
                    border-radius: 0.75rem;
                    font-weight: 600;
                    cursor: pointer;
                    font-size: 1rem;
                    transition: all 0.3s ease;
                ">Got it!</button>
            </div>
        `;

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        document.body.appendChild(modal);
    }

    createShortcutRow(key, description) {
        return `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0;">
                <span style="color: #64748b;">${description}</span>
                <kbd style="
                    background: #f1f5f9;
                    padding: 0.25rem 0.75rem;
                    border-radius: 0.375rem;
                    font-family: monospace;
                    font-size: 0.875rem;
                    border: 1px solid #cbd5e1;
                    color: #1e293b;
                    font-weight: 600;
                ">${key}</kbd>
            </div>
        `;
    }

    callNextPatient() {
        // Only works on doctor page
        if (window.location.pathname === '/doctor') {
            if (typeof callNext === 'function') {
                callNext();
                if (window.showToast) {
                    window.showToast('Calling next patient...', 'info');
                }
            }
        }
    }

    toggleDarkMode() {
        if (window.darkModeManager) {
            window.darkModeManager.toggle();
        }
    }

    toggleSound() {
        if (window.soundNotification) {
            const enabled = window.soundNotification.toggle();
            if (window.showToast) {
                window.showToast(enabled ? 'Sound enabled' : 'Sound muted', 'info');
            }
        }
    }
}

// Initialize keyboard shortcuts
document.addEventListener('DOMContentLoaded', () => {
    window.keyboardShortcuts = new KeyboardShortcuts();
});
