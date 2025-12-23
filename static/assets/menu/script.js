document.addEventListener('DOMContentLoaded', () => {
    const menu = document.querySelector('.menu');
    const button = document.querySelector('.menu_toggler');
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

    // Language selector handler
    const languageSelector = document.getElementById('language-selector');
    if (languageSelector) {
        // Get current language from URL or localStorage
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get('lang');
        const savedLanguage = localStorage.getItem('selectedLanguage') || urlLang || 'en';
        
        // Set the selector to match current language
        if (savedLanguage && ['en', 'fr'].includes(savedLanguage)) {
            languageSelector.value = savedLanguage;
        }

        languageSelector.addEventListener('change', (e) => {
            const selectedLanguage = e.target.value;
            
            // Save language preference
            localStorage.setItem('selectedLanguage', selectedLanguage);
            
            // Redirect to set language route (Flask-Babel)
            window.location.href = `/set_language/${selectedLanguage}`;
        });
    }
});
