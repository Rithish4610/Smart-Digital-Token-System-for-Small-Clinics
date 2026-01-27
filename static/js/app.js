// Enhanced interactions and utilities for Smart Token System

// Smooth scroll behavior
document.documentElement.style.scrollBehavior = 'smooth';

// Add ripple effect to buttons
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Add focus animations to inputs
const inputs = document.querySelectorAll('input, select, textarea');
inputs.forEach(input => {
    input.addEventListener('focus', function () {
        this.parentElement.classList.add('input-focused');
    });

    input.addEventListener('blur', function () {
        this.parentElement.classList.remove('input-focused');
    });
});

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    const styles = {
        position: 'fixed',
        bottom: '2rem',
        right: '2rem',
        padding: '1rem 1.5rem',
        borderRadius: '1rem',
        color: 'white',
        fontWeight: '600',
        fontSize: '0.95rem',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.2)',
        zIndex: '10000',
        animation: 'slideInRight 0.4s ease-out',
        maxWidth: '400px'
    };

    Object.assign(toast.style, styles);

    // Set background based on type
    const backgrounds = {
        success: 'linear-gradient(135deg, #06d6a0 0%, #05b589 100%)',
        error: 'linear-gradient(135deg, #ef476f 0%, #d62828 100%)',
        warning: 'linear-gradient(135deg, #ffd60a 0%, #fca311 100%)',
        info: 'linear-gradient(135deg, #5e60ce 0%, #7209b7 100%)'
    };

    toast.style.background = backgrounds[type] || backgrounds.info;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.4s ease-out';
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
    
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .input-focused {
        transform: translateY(-2px);
        transition: transform 0.3s ease;
    }
`;
document.head.appendChild(style);

// Auto-hide alerts after 5 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert, .error-msg, .success-msg');
    alerts.forEach(alert => {
        if (alert.style.display !== 'none') {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.style.display = 'none', 500);
        }
    });
}, 5000);

// Expose toast globally
window.showToast = showToast;
