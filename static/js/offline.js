// Offline support with Service Worker

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
}

// Cache management
class CacheManager {
    constructor() {
        this.cacheName = 'clinic-cache-v1';
        this.offlineMode = false;
        this.init();
    }

    init() {
        // Check online status
        this.updateOnlineStatus();

        window.addEventListener('online', () => this.updateOnlineStatus());
        window.addEventListener('offline', () => this.updateOnlineStatus());
    }

    updateOnlineStatus() {
        this.offlineMode = !navigator.onLine;

        const indicator = document.getElementById('offline-indicator') || this.createIndicator();

        if (this.offlineMode) {
            indicator.style.display = 'flex';
            if (window.showToast) {
                window.showToast('You are offline. Some features may be limited.', 'warning');
            }
        } else {
            indicator.style.display = 'none';
            if (window.showToast && this.wasOffline) {
                window.showToast('Back online!', 'success');
            }
        }

        this.wasOffline = this.offlineMode;
    }

    createIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #ffd60a 0%, #fca311 100%);
            color: #1a202c;
            padding: 0.75rem;
            text-align: center;
            font-weight: 600;
            z-index: 10000;
            display: none;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            box-shadow: 0 4px 16px rgba(252, 163, 17, 0.3);
        `;
        indicator.innerHTML = `
            <span>⚠️</span>
            <span>Offline Mode - Limited functionality</span>
        `;
        document.body.appendChild(indicator);
        return indicator;
    }

    async cacheData(key, data) {
        try {
            localStorage.setItem(`cache_${key}`, JSON.stringify({
                data: data,
                timestamp: Date.now()
            }));
        } catch (error) {
            console.error('Cache error:', error);
        }
    }

    getCachedData(key, maxAge = 300000) { // 5 minutes default
        try {
            const cached = localStorage.getItem(`cache_${key}`);
            if (!cached) return null;

            const { data, timestamp } = JSON.parse(cached);

            if (Date.now() - timestamp > maxAge) {
                localStorage.removeItem(`cache_${key}`);
                return null;
            }

            return data;
        } catch (error) {
            console.error('Cache retrieval error:', error);
            return null;
        }
    }

    clearCache() {
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('cache_')) {
                localStorage.removeItem(key);
            }
        });
    }
}

// Enhanced fetch with offline support
async function fetchWithCache(url, options = {}) {
    const cacheManager = window.cacheManager || new CacheManager();

    // Try network first
    if (navigator.onLine) {
        try {
            const response = await fetch(url, options);
            const data = await response.json();

            // Cache successful responses
            if (response.ok) {
                cacheManager.cacheData(url, data);
            }

            return data;
        } catch (error) {
            console.error('Fetch error:', error);
        }
    }

    // Fallback to cache
    const cached = cacheManager.getCachedData(url);
    if (cached) {
        console.log('Using cached data for:', url);
        return cached;
    }

    throw new Error('No network and no cached data available');
}

// Initialize cache manager
window.addEventListener('DOMContentLoaded', () => {
    window.cacheManager = new CacheManager();
});
