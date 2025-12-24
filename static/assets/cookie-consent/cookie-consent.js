/**
 * Cookie Consent Banner Handler
 * Shows cookie consent banner on first visit and handles user preferences
 */

(function() {
    'use strict';

    const COOKIE_CONSENT_KEY = 'cookie_consent';
    const COOKIE_PREFERENCES_KEY = 'cookie_preferences';
    
    // Check if consent has been given
    function hasConsent() {
        return localStorage.getItem(COOKIE_CONSENT_KEY) !== null;
    }
    
    // Get current preferences
    function getPreferences() {
        const prefs = localStorage.getItem(COOKIE_PREFERENCES_KEY);
        if (prefs) {
            try {
                return JSON.parse(prefs);
            } catch (e) {
                return null;
            }
        }
        return null;
    }
    
    // Save preferences
    function savePreferences(preferences) {
        localStorage.setItem(COOKIE_PREFERENCES_KEY, JSON.stringify(preferences));
        localStorage.setItem(COOKIE_CONSENT_KEY, 'true');
    }
    
    // Show the banner
    function showBanner() {
        const banner = document.getElementById('cookie-consent-banner');
        if (banner) {
            banner.style.display = 'block';
            // Add animation
            setTimeout(() => {
                banner.style.opacity = '1';
                banner.style.transform = 'translateY(0)';
            }, 10);
        }
    }
    
    // Hide the banner
    function hideBanner() {
        const banner = document.getElementById('cookie-consent-banner');
        if (banner) {
            banner.style.opacity = '0';
            banner.style.transform = 'translateY(100%)';
            setTimeout(() => {
                banner.style.display = 'none';
            }, 300);
        }
    }
    
    // Show customize panel
    function showCustomizePanel() {
        const panel = document.getElementById('cookie-customize-panel');
        const content = document.querySelector('.cookie-consent-content');
        if (panel && content) {
            panel.style.display = 'block';
            content.style.display = 'none';
            
            // Load current preferences if any
            const prefs = getPreferences();
            if (prefs) {
                document.getElementById('cookie-analytics').checked = prefs.analytics || false;
                document.getElementById('cookie-marketing').checked = prefs.marketing || false;
            }
        }
    }
    
    // Hide customize panel
    function hideCustomizePanel() {
        const panel = document.getElementById('cookie-customize-panel');
        const content = document.querySelector('.cookie-consent-content');
        if (panel && content) {
            panel.style.display = 'none';
            content.style.display = 'flex';
        }
    }
    
    // Accept all cookies
    function acceptAll() {
        savePreferences({
            necessary: true,
            analytics: true,
            marketing: true
        });
        hideBanner();
        // Trigger custom event for other scripts
        document.dispatchEvent(new CustomEvent('cookieConsentAccepted', { 
            detail: { necessary: true, analytics: true, marketing: true } 
        }));
    }
    
    // Accept necessary only
    function acceptNecessary() {
        savePreferences({
            necessary: true,
            analytics: false,
            marketing: false
        });
        hideBanner();
        // Trigger custom event
        document.dispatchEvent(new CustomEvent('cookieConsentAccepted', { 
            detail: { necessary: true, analytics: false, marketing: false } 
        }));
    }
    
    // Save custom preferences
    function saveCustomPreferences() {
        const preferences = {
            necessary: true, // Always true
            analytics: document.getElementById('cookie-analytics').checked,
            marketing: document.getElementById('cookie-marketing').checked
        };
        savePreferences(preferences);
        hideBanner();
        // Trigger custom event
        document.dispatchEvent(new CustomEvent('cookieConsentAccepted', { 
            detail: preferences 
        }));
    }
    
    // Initialize on DOM ready
    function init() {
        // Only show if consent hasn't been given
        if (!hasConsent()) {
            // Add initial styles for animation
            const banner = document.getElementById('cookie-consent-banner');
            if (banner) {
                banner.style.opacity = '0';
                banner.style.transform = 'translateY(100%)';
                banner.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            }
            
            // Show banner after a short delay
            setTimeout(showBanner, 500);
        }
        
        // Set up event listeners
        const acceptAllBtn = document.getElementById('cookie-accept-all');
        const acceptNecessaryBtn = document.getElementById('cookie-accept-necessary');
        const customizeBtn = document.getElementById('cookie-customize');
        const savePrefsBtn = document.getElementById('cookie-save-preferences');
        const cancelBtn = document.getElementById('cookie-cancel-customize');
        
        if (acceptAllBtn) {
            acceptAllBtn.addEventListener('click', acceptAll);
        }
        
        if (acceptNecessaryBtn) {
            acceptNecessaryBtn.addEventListener('click', acceptNecessary);
        }
        
        if (customizeBtn) {
            customizeBtn.addEventListener('click', showCustomizePanel);
        }
        
        if (savePrefsBtn) {
            savePrefsBtn.addEventListener('click', saveCustomPreferences);
        }
        
        if (cancelBtn) {
            cancelBtn.addEventListener('click', hideCustomizePanel);
        }
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Export functions for external use
    window.cookieConsent = {
        getPreferences: getPreferences,
        hasConsent: hasConsent,
        reset: function() {
            localStorage.removeItem(COOKIE_CONSENT_KEY);
            localStorage.removeItem(COOKIE_PREFERENCES_KEY);
            showBanner();
        }
    };
})();

