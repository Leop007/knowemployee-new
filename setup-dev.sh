#!/bin/bash

# Setup script for local development environment

echo "Setting up KnowEmployee local development environment..."
echo ""

# Check if .env.dev exists
if [ ! -f .env.dev ]; then
    echo "Creating .env.dev file..."
    cat > .env.dev << 'EOF'
# Local Development Environment Variables
FLASK_ENV=development
DOMAIN=http://localhost:8000

# Email Configuration
EMAIL_SENDER=knowemployee.ca@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here

# API Keys
DEEPGRAM_API_KEY=your_deepgram_api_key_here
API_KEY_OPENAI=your_openai_api_key_here
OPENAI_ORGANIZATION_ID=your_openai_organization_id_here
MAX_TOKENS=4000
INPUT_COST_PER_1K_TOKENS=0.0015
OUTPUT_COST_PER_1K_TOKENS=0.002
EOF
    echo "✓ Created .env.dev file"
    echo "⚠️  Please edit .env.dev and add your actual API keys and credentials"
else
    echo "✓ .env.dev already exists"
fi

# Check if .env exists (for production)
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file for production..."
    cat > .env << 'EOF'
# Production Environment Variables
FLASK_ENV=production
DOMAIN=https://knowemployee.com

# Email Configuration
EMAIL_SENDER=knowemployee.ca@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here

# API Keys
DEEPGRAM_API_KEY=your_deepgram_api_key_here
API_KEY_OPENAI=your_openai_api_key_here
OPENAI_ORGANIZATION_ID=your_openai_organization_id_here
MAX_TOKENS=4000
INPUT_COST_PER_1K_TOKENS=0.0015
OUTPUT_COST_PER_1K_TOKENS=0.002
EOF
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env and add your actual API keys and credentials"
else
    echo "✓ .env already exists"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.dev and add your API keys and credentials"
echo "2. Run: docker-compose -f docker-compose.dev.yml up --build"
echo "3. Access the app at: http://localhost:8000"
echo ""
echo "For more information, see DEV_SETUP.md"

