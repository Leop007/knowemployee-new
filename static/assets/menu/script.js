// Language selector handler - works independently on all pages
function initLanguageSelector() {
    const languageSelectors = document.querySelectorAll('#language-selector, .language-selector');
    
    languageSelectors.forEach((languageSelector) => {
        // Skip if already initialized
        if (languageSelector.dataset.initialized === 'true') {
            return;
        }
        
        // Mark as initialized
        languageSelector.dataset.initialized = 'true';
        
        // Get current language from data attribute, localStorage, or default to 'en'
        const currentLang = languageSelector.getAttribute('data-current-lang') || 
                          localStorage.getItem('selectedLanguage') || 
                          'en';
        
        // Set the selector to match current language
        if (currentLang && ['en', 'fr'].includes(currentLang)) {
            languageSelector.value = currentLang;
        }

        languageSelector.addEventListener('change', (e) => {
            const selectedLanguage = e.target.value;
            
            // Save language preference
            localStorage.setItem('selectedLanguage', selectedLanguage);
            
            // Get current page URL to preserve it after language change
            const currentPath = window.location.pathname;
            const currentQuery = window.location.search;
            const currentUrl = currentPath + currentQuery;
            
            // Redirect to set language route, which will redirect back to current page
            window.location.href = `/set_language/${selectedLanguage}?redirect=${encodeURIComponent(currentUrl)}`;
        });
    });
}

// Menu toggle functionality (only if menu elements exist)
function initMenuToggle() {
    const menu = document.querySelector('.menu');
    const button = document.querySelector('.menu_toggler');
    
    if (!menu || !button) {
        return; // Menu elements don't exist on this page
    }
    
    const toggleMenu = () => {
        if (window.innerWidth >= 768) {
            menu.style.display = 'block';
        } else {
            if (button.classList.contains('cross')) {
                menu.style.display = 'block';
            } else {
                menu.style.display = 'none';
            }
        }
    };

    toggleMenu();

    button.addEventListener('click', () => {
        if (button.classList.contains('cross')) {
            button.classList.remove('cross');
            button.classList.add('toggle');
            toggleMenu();
        } else {
            button.classList.remove('toggle');
            button.classList.add('cross');
            toggleMenu();
        }
    });

    window.addEventListener('resize', toggleMenu);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initLanguageSelector();
        initMenuToggle();
    });
} else {
    // DOM is already loaded
    initLanguageSelector();
    initMenuToggle();
}
