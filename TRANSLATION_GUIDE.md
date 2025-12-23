# Flask-Babel Translation Guide (Docker)

## Setup Complete ✅

Flask-Babel has been configured in your application. Here's what was done:

1. ✅ Added Flask-Babel to `requirements.txt`
2. ✅ Configured Flask-Babel in `server.py`
3. ✅ Created language switching route `/set_language/<language>`
4. ✅ Updated JavaScript to use the language switching route
5. ✅ Created Babel configuration file
6. ✅ Updated Docker volumes to include translations directory
7. ✅ Created `translate.sh` helper script for Docker

## Docker-Specific Setup

The translations directory is mounted as a volume in both `docker-compose.yml` and `docker-compose.dev.yml`, so:
- Translations persist across container restarts
- You can edit `.po` files on your host machine
- Compiled `.mo` files are generated inside the container

## Quick Start (Using Helper Script)

### Option 1: Use the Helper Script (Recommended)

```bash
# Make script executable (first time only)
chmod +x translate.sh

# Extract all translatable strings
./translate.sh extract

# Initialize French translation
./translate.sh init fr

# Edit translations/fr/LC_MESSAGES/messages.po and translate strings

# Compile translations
./translate.sh compile

# Or run everything at once
./translate.sh all
```

### Option 2: Run Commands Directly in Docker

If your container is named `knowemployee-app-dev`:

```bash
# Extract strings
docker exec -it knowemployee-app-dev pybabel extract -F babel/babel.cfg -k _l -o messages.pot .

# Initialize French
docker exec -it knowemployee-app-dev pybabel init -i messages.pot -d translations -l fr

# Update translations (after code changes)
docker exec -it knowemployee-app-dev pybabel update -i messages.pot -d translations

# Compile translations
docker exec -it knowemployee-app-dev pybabel compile -d translations
```

## Step-by-Step Workflow

### 1. Extract Translatable Strings
```bash
./translate.sh extract
```
This creates `messages.pot` with all translatable strings from your code and templates.

### 2. Initialize French Translation
```bash
./translate.sh init fr
```
This creates: `translations/fr/LC_MESSAGES/messages.po`

### 3. Translate Strings
Edit `translations/fr/LC_MESSAGES/messages.po` on your host machine and translate all the `msgstr ""` entries.

Example:
```po
msgid "Welcome"
msgstr "Bienvenue"

msgid "Contact us"
msgstr "Contactez-nous"
```

### 4. Compile Translations
```bash
./translate.sh compile
```
This compiles `.po` files to `.mo` binary format that Flask-Babel uses.

### 5. Restart Container (if needed)
```bash
docker-compose -f docker-compose.dev.yml restart knowemployee
```

### 6. Update Templates

Replace hardcoded text with translation functions:

**Before:**
```html
<h1>Welcome</h1>
<p>Contact us</p>
<a href="/">Home</a>
```

**After:**
```html
<h1>{{ _('Welcome') }}</h1>
<p>{{ _('Contact us') }}</p>
<a href="/">{{ _('Home') }}</a>
```

### 7. Update Python Code

In `server.py`, wrap strings that need translation:

**Before:**
```python
return jsonify({"message": "Thanks for the feedback!"})
```

**After:**
```python
return jsonify({"message": _("Thanks for the feedback!")})
```

### 8. Update Translations After Adding New Strings

When you add new translatable strings:
```bash
# Run the full workflow
./translate.sh all

# Or step by step:
./translate.sh extract
./translate.sh update
# Edit .po files with new translations
./translate.sh compile
```

## How It Works

1. **Language Selection**: User selects language from dropdown
2. **Session Storage**: Language is stored in Flask session
3. **Locale Selection**: `get_locale()` function returns the selected language
4. **Template Translation**: `{{ _('Text') }}` automatically translates based on current locale
5. **Automatic Fallback**: Falls back to English if translation is missing

## Testing in Docker

1. Make sure your container is running:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. Access your app at `http://localhost:8001`

3. Select "FR" from language dropdown

4. Page should reload and show French translations (once you've translated the strings)

5. Check that session persists language across page navigations

6. View container logs if needed:
   ```bash
   docker logs -f knowemployee-app-dev
   ```

## File Structure

```
knowemployee-new/
├── babel/
│   └── babel.cfg              # Babel configuration
├── translations/
│   └── fr/
│       └── LC_MESSAGES/
│           ├── messages.po    # Source translation file (edit this)
│           └── messages.mo    # Compiled binary (auto-generated)
├── messages.pot               # Template file (auto-generated)
├── translate.sh               # Helper script for Docker
└── TRANSLATION_GUIDE.md       # This file
```

## Important Notes for Docker

- **Translations directory is mounted**: Edit `.po` files on your host, they sync to container
- **Compiled files (.mo)**: Generated inside container, but persist via volume
- **After compiling**: You may need to restart the container for changes to take effect
- **Git ignore**: `.mo` files are ignored (compiled), but `.po` files should be committed

## Tips

- Use `_l()` for lazy translations (evaluated when used, not at import time)
- Use `_()` for immediate translations
- Pluralization: `ngettext('singular', 'plural', count)`
- Date formatting: `format_date(date_obj)`
- Number formatting: `format_number(number)`

## Example Template Usage

```html
{% extends "base.html" %}

{% block title %}{{ _('Home') }}{% endblock %}

{% block content %}
    <h1>{{ _('Welcome to KnowEmployee') }}</h1>
    <p>{{ _('Contact us') }}</p>
    <a href="/contact">{{ _('Contact') }}</a>
{% endblock %}
```

