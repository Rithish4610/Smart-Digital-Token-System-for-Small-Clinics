// Form validation utilities

class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (!this.form) return;

        this.rules = {};
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });

        // Real-time validation
        this.form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });
    }

    addRule(fieldName, rules) {
        this.rules[fieldName] = rules;
        return this;
    }

    validate() {
        let isValid = true;

        for (const [fieldName, rules] of Object.entries(this.rules)) {
            const input = this.form.querySelector(`[name="${fieldName}"], #${fieldName}`);
            if (!input) continue;

            if (!this.validateField(input, rules)) {
                isValid = false;
            }
        }

        return isValid;
    }

    validateField(input, rules = null) {
        if (!rules) {
            rules = this.rules[input.name] || this.rules[input.id];
        }
        if (!rules) return true;

        const value = input.value.trim();

        // Required
        if (rules.required && !value) {
            this.showError(input, rules.requiredMessage || 'This field is required');
            return false;
        }

        // Min length
        if (rules.minLength && value.length < rules.minLength) {
            this.showError(input, `Minimum ${rules.minLength} characters required`);
            return false;
        }

        // Max length
        if (rules.maxLength && value.length > rules.maxLength) {
            this.showError(input, `Maximum ${rules.maxLength} characters allowed`);
            return false;
        }

        // Pattern
        if (rules.pattern && !rules.pattern.test(value)) {
            this.showError(input, rules.patternMessage || 'Invalid format');
            return false;
        }

        // Phone
        if (rules.phone) {
            const phonePattern = /^[\d\s\-\+\(\)]+$/;
            if (!phonePattern.test(value) || value.length < 10) {
                this.showError(input, 'Please enter a valid phone number');
                return false;
            }
        }

        // Email
        if (rules.email) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(value)) {
                this.showError(input, 'Please enter a valid email address');
                return false;
            }
        }

        // Number
        if (rules.number) {
            if (isNaN(value)) {
                this.showError(input, 'Please enter a valid number');
                return false;
            }
            if (rules.min !== undefined && parseFloat(value) < rules.min) {
                this.showError(input, `Minimum value is ${rules.min}`);
                return false;
            }
            if (rules.max !== undefined && parseFloat(value) > rules.max) {
                this.showError(input, `Maximum value is ${rules.max}`);
                return false;
            }
        }

        // Custom validator
        if (rules.custom && typeof rules.custom === 'function') {
            const result = rules.custom(value);
            if (result !== true) {
                this.showError(input, result || 'Invalid value');
                return false;
            }
        }

        this.clearError(input);
        return true;
    }

    showError(input, message) {
        this.clearError(input);

        input.classList.add('error');
        input.style.borderColor = '#ef476f';

        const error = document.createElement('div');
        error.className = 'validation-error';
        error.textContent = message;
        error.style.cssText = `
            color: #ef476f;
            font-size: 0.875rem;
            margin-top: 0.25rem;
            animation: fadeIn 0.3s ease;
        `;

        input.parentElement.appendChild(error);
    }

    clearError(input) {
        input.classList.remove('error');
        input.style.borderColor = '';

        const error = input.parentElement.querySelector('.validation-error');
        if (error) {
            error.remove();
        }
    }
}

// Auto-format phone numbers
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    input.value = value;
}

// Auto-format token numbers
function formatTokenNumber(input) {
    let value = input.value.replace(/\D/g, '');
    input.value = value;
}

// Initialize validators on common forms
document.addEventListener('DOMContentLoaded', () => {
    // Registration form
    if (document.getElementById('registrationForm')) {
        const validator = new FormValidator('registrationForm');
        validator
            .addRule('name', {
                required: true,
                minLength: 2,
                maxLength: 100,
                requiredMessage: 'Please enter patient name'
            })
            .addRule('phone', {
                required: true,
                phone: true,
                requiredMessage: 'Please enter phone number'
            });

        // Auto-format phone
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', () => formatPhoneNumber(phoneInput));
        }
    }

    // Login form
    if (document.getElementById('loginForm')) {
        const validator = new FormValidator('loginForm');
        validator
            .addRule('tokenNumber', {
                required: true,
                number: true,
                min: 1,
                requiredMessage: 'Please enter your token number'
            })
            .addRule('last4', {
                required: true,
                pattern: /^\d{4}$/,
                patternMessage: 'Please enter 4 digits',
                requiredMessage: 'Please enter last 4 digits of phone'
            });

        // Auto-format inputs
        const tokenInput = document.getElementById('tokenNumber');
        const last4Input = document.getElementById('last4');

        if (tokenInput) {
            tokenInput.addEventListener('input', () => formatTokenNumber(tokenInput));
        }
        if (last4Input) {
            last4Input.addEventListener('input', () => formatTokenNumber(last4Input));
        }
    }
});
