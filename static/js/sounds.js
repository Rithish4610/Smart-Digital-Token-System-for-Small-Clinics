// Sound notification system for better user alerts

class SoundNotification {
    constructor() {
        this.audioContext = null;
        this.enabled = true;
    }

    init() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    // Play success sound
    playSuccess() {
        if (!this.enabled) return;
        this.init();
        this.playTone(523.25, 0.1); // C5
        setTimeout(() => this.playTone(659.25, 0.15), 100); // E5
    }

    // Play notification sound
    playNotification() {
        if (!this.enabled) return;
        this.init();
        this.playTone(440, 0.1); // A4
        setTimeout(() => this.playTone(554.37, 0.1), 100); // C#5
    }

    // Play error sound
    playError() {
        if (!this.enabled) return;
        this.init();
        this.playTone(200, 0.2);
    }

    // Play calling sound (for when patient is called)
    playCalling() {
        if (!this.enabled) return;
        this.init();
        this.playTone(659.25, 0.15); // E5
        setTimeout(() => this.playTone(783.99, 0.15), 150); // G5
        setTimeout(() => this.playTone(1046.50, 0.3), 300); // C6
    }

    // Core tone generator
    playTone(frequency, duration) {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);

        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }

    toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
    }
}

// Create global sound instance
window.soundNotification = new SoundNotification();

// Add sound toggle button to pages
document.addEventListener('DOMContentLoaded', () => {
    const soundToggle = document.createElement('button');
    soundToggle.className = 'sound-toggle';
    soundToggle.innerHTML = '🔊';
    soundToggle.title = 'Toggle sound notifications';
    soundToggle.style.cssText = `
        position: fixed;
        bottom: 2rem;
        left: 2rem;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: linear-gradient(135deg, #5e60ce 0%, #7209b7 100%);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(94, 96, 206, 0.3);
        z-index: 1000;
        transition: all 0.3s ease;
    `;

    soundToggle.addEventListener('click', () => {
        const enabled = window.soundNotification.toggle();
        soundToggle.innerHTML = enabled ? '🔊' : '🔇';
        soundToggle.style.opacity = enabled ? '1' : '0.5';
        showToast(enabled ? 'Sound enabled' : 'Sound muted', 'info');
    });

    document.body.appendChild(soundToggle);
});
