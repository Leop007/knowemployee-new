# Local Development Setup Guide

This guide will help you set up the KnowEmployee application for local development.

## Quick Start

### 1. Create Environment File

Create a `.env.dev` file in the project root with the following variables:

```env
# Flask Environment
FLASK_ENV=development

# Domain Configuration (for local development)
DOMAIN=http://localhost:8000

# Secret Key (change this in production!)
SECRET_KEY=97473497e94c7289a98fae8e9636ae67

# Database
SQLALCHEMY_DATABASE_URI=sqlite:///service.db

# Email Configuration
EMAIL_SENDER=knowemployee.ca@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here

# Deepgram API
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# OpenAI Configuration
API_KEY_OPENAI=your_openai_api_key_here
OPENAI_ORGANIZATION_ID=your_openai_organization_id_here
MAX_TOKENS=4000
INPUT_COST_PER_1K_TOKENS=0.0015
OUTPUT_COST_PER_1K_TOKENS=0.002
```

### 2. Run Development Environment

Use the development docker-compose file:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Or run in detached mode:

```bash
docker-compose -f docker-compose.dev.yml up -d --build
```

### 3. Access the Application

- **Application**: http://localhost:8000
- **No nginx/certbot** - Direct access to Flask app

## Development vs Production

### Development (`docker-compose.dev.yml`)
- Direct port exposure (8000:8005)
- HTTP only (no HTTPS)
- Source files mounted for easy editing
- No nginx/certbot
- Development environment variables

### Production (`docker-compose.yml`)
- Behind nginx reverse proxy
- HTTPS with Let's Encrypt certificates
- Ports 80/443 exposed
- Production environment variables

## Environment Variables

### Required Variables

| Variable | Description | Example (Dev) | Example (Prod) |
|----------|-------------|---------------|----------------|
| `FLASK_ENV` | Environment mode | `development` | `production` |
| `DOMAIN` | Application domain | `http://localhost:8000` | `https://knowemployee.com` |
| `EMAIL_SENDER` | Email sender address | `knowemployee.ca@gmail.com` | `knowemployee.ca@gmail.com` |
| `EMAIL_PASSWORD` | Gmail App Password | `your_app_password` | `your_app_password` |
| `DEEPGRAM_API_KEY` | Deepgram API key | `your_key` | `your_key` |
| `API_KEY_OPENAI` | OpenAI API key | `your_key` | `your_key` |
| `OPENAI_ORGANIZATION_ID` | OpenAI Org ID | `your_org_id` | `your_org_id` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `97473497e94c7289a98fae8e9636ae67` |
| `SQLALCHEMY_DATABASE_URI` | Database URI | `sqlite:///service.db` |
| `MAX_TOKENS` | OpenAI max tokens | `4000` |
| `INPUT_COST_PER_1K_TOKENS` | Input cost | `0.0015` |
| `OUTPUT_COST_PER_1K_TOKENS` | Output cost | `0.002` |

## File Structure

```
knowemployee-new/
├── docker-compose.yml          # Production setup (nginx + certbot)
├── docker-compose.dev.yml      # Development setup (direct access)
├── .env.dev                    # Development environment variables (create this)
├── .env                        # Production environment variables (create this)
├── .env.example                # Template for environment variables
└── DEV_SETUP.md               # This file
```

## Common Commands

### Development

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker-compose.dev.yml down

# Rebuild after code changes
docker-compose -f docker-compose.dev.yml up --build
```

### Production

```bash
# Start production environment
docker-compose up -d

# View logs
docker-compose logs -f knowemployee

# Stop
docker-compose down
```

## Troubleshooting

### Email Not Sending

1. Make sure `EMAIL_PASSWORD` is a Gmail App Password (not regular password)
2. Enable 2-Step Verification in Google Account
3. Generate App Password at: https://myaccount.google.com/apppasswords

### Database Issues

- Database is stored in `./instance/service.db`
- To reset: Delete `./instance/service.db` and restart container
- Migrations are in `./migrations/` directory

### Port Already in Use

If port 8000 is already in use, change it in `docker-compose.dev.yml`:

```yaml
ports:
  - "8001:8005"  # Change 8000 to 8001 or any available port
```

And update `DOMAIN` in `.env.dev` accordingly.

## Notes

- `.env.dev` and `.env` files are gitignored for security
- Development mode uses HTTP (no HTTPS)
- Source files are mounted as volumes for easy editing
- Database persists in `./instance/` directory

