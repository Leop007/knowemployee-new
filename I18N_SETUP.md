# Internationalization (i18n) Setup Guide

## Best Option: Flask-Babel

Flask-Babel is the standard, professional solution for Flask applications. It provides:
- ✅ Full integration with Jinja2 templates
- ✅ gettext support (industry standard)
- ✅ Easy extraction of translatable strings
- ✅ Support for pluralization and date/number formatting
- ✅ Works seamlessly with Flask

## Implementation Steps

### 1. Install Flask-Babel

Add to `requirements.txt`:
```
Flask-Babel==4.0.0
```

Then install:
```bash
pip install Flask-Babel==4.0.0
```

### 2. Configure Flask-Babel in server.py

Add these imports at the top:
```python
from flask_babel import Babel, gettext as _, lazy_gettext as _l
from flask_babel import get_locale
```

Add configuration after app creation:
```python
app.config['LANGUAGES'] = {
    'en': 'English',
    'fr': 'Français'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel(app)

@babel.localeselector
def get_locale():
    # Check if language is in session
    language = session.get('language', 'en')
    if language in app.config['LANGUAGES']:
        return language
    # Fallback to browser language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'
```

### 3. Create Language Switching Route

Add to server.py:
```python
@app.route('/set_language/<language>')
def set_language(language):
    if language in app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))
```

### 4. Update Language Selector JavaScript

Update `static/assets/menu/script.js`:
```javascript
languageSelector.addEventListener('change', (e) => {
    const selectedLanguage = e.target.value;
    localStorage.setItem('selectedLanguage', selectedLanguage);
    // Redirect to set language route
    window.location.href = `/set_language/${selectedLanguage}`;
});
```

### 5. Create Translation Files

Create directory structure:
```bash
mkdir -p babel
mkdir -p translations
```

Create `babel/babel.cfg`:
```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

### 6. Extract Translatable Strings

```bash
# Extract strings from code and templates
pybabel extract -F babel/babel.cfg -k _l -o messages.pot .

# Initialize French translation
pybabel init -i messages.pot -d translations -l fr

# Update translations (after adding new strings)
pybabel update -i messages.pot -d translations
```

### 7. Translate Strings

Edit `translations/fr/LC_MESSAGES/messages.po` and translate all strings.

### 8. Compile Translations

```bash
pybabel compile -d translations
```

### 9. Update Templates

Replace hardcoded text with translation functions:

**Before:**
```html
<h1>Welcome</h1>
<p>Contact us</p>
```

**After:**
```html
<h1>{{ _('Welcome') }}</h1>
<p>{{ _('Contact us') }}</p>
```

### 10. Update server.py Routes

Pass locale to templates:
```python
from flask_babel import get_locale

@app.route('/')
def index():
    # ... existing code ...
    return render_template('index.html', 
                         is_authenticated=is_authenticated,
                         locale=str(get_locale()))
```

## Alternative: Simpler JSON-Based Approach

If you prefer a simpler approach without Flask-Babel:

1. Create `translations.json`:
```json
{
  "en": {
    "welcome": "Welcome",
    "contact_us": "Contact us",
    "home": "Home"
  },
  "fr": {
    "welcome": "Bienvenue",
    "contact_us": "Contactez-nous",
    "home": "Accueil"
  }
}
```

2. Create helper function in server.py:
```python
def get_translations(lang='en'):
    with open('translations.json', 'r', encoding='utf-8') as f:
        return json.load(f).get(lang, {})
```

3. Pass to templates:
```python
translations = get_translations(session.get('language', 'en'))
return render_template('index.html', t=translations)
```

4. Use in templates:
```html
<h1>{{ t.welcome }}</h1>
```

## Recommendation

**Use Flask-Babel** for:
- Professional, scalable solution
- Industry standard (gettext)
- Better for long-term maintenance
- Supports pluralization and date formatting
- Easy to add more languages later

**Use JSON approach** for:
- Quick implementation
- Simple use cases
- Small number of strings
- No need for advanced features

## Next Steps

1. Choose your approach (recommended: Flask-Babel)
2. Install dependencies
3. Extract all translatable strings from templates
4. Create French translations
5. Test language switching
6. Update all templates to use translations

