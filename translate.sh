#!/bin/bash
# Translation helper script for Docker environment

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CONTAINER_NAME="knowemployee-app-dev"

echo -e "${BLUE}Flask-Babel Translation Helper${NC}"
echo "================================"
echo ""

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo -e "${YELLOW}Warning: Container '$CONTAINER_NAME' is not running.${NC}"
    echo "Starting container..."
    docker-compose -f docker-compose.dev.yml up -d
    sleep 2
fi

# Clean up messages.pot directory on host if it exists (before any operations)
if [ -d messages.pot ]; then
    echo -e "${YELLOW}Removing messages.pot directory from host (may require container restart)...${NC}"
    rm -rf messages.pot 2>/dev/null || {
        echo -e "${YELLOW}Could not remove messages.pot directory. Please run:${NC}"
        echo "  docker-compose -f docker-compose.dev.yml stop knowemployee"
        echo "  rm -rf messages.pot"
        echo "  docker-compose -f docker-compose.dev.yml start knowemployee"
    }
fi

# Function to run babel commands in container
run_babel() {
    docker exec -it "$CONTAINER_NAME" "$@"
}

# Function to clean up messages.pot if it's a directory
clean_messages_pot() {
    # Try to remove from container, but if it's a mounted volume, remove from host
    if [ -d messages.pot ]; then
        echo -e "${YELLOW}Removing messages.pot directory from host...${NC}"
        rm -rf messages.pot
    fi
    # Also try to remove from container (in case it's not mounted)
    run_babel sh -c "if [ -d messages.pot ] && [ ! -L messages.pot ]; then rm -rf messages.pot 2>/dev/null; fi" 2>/dev/null || true
}

case "$1" in
    extract)
        echo -e "${GREEN}Extracting translatable strings...${NC}"
        clean_messages_pot
        # Extract directly to /tmp first, then copy to final location
        echo -e "${YELLOW}Extracting translatable strings...${NC}"
        run_babel pybabel extract -F babel/babel.cfg -k _l -o /tmp/messages.pot .
        # Copy from container to host, then remove directory if needed
        echo -e "${YELLOW}Copying to host...${NC}"
        docker cp "$CONTAINER_NAME:/tmp/messages.pot" ./messages.pot.tmp 2>/dev/null || {
            echo -e "${YELLOW}Could not copy from container. Trying to copy inside container...${NC}"
            run_babel sh -c "cd /know && if [ -d messages.pot ]; then rm -rf messages.pot; fi && cp /tmp/messages.pot messages.pot && rm -f /tmp/messages.pot"
        }
        # If we copied to host, move it to final location
        if [ -f messages.pot.tmp ]; then
            if [ -d messages.pot ]; then
                rm -rf messages.pot
            fi
            mv messages.pot.tmp messages.pot
            echo -e "${GREEN}✓ File copied to host: messages.pot${NC}"
        fi
        echo -e "${GREEN}✓ Extraction complete. Check messages.pot${NC}"
        ;;
    init)
        if [ -z "$2" ]; then
            echo -e "${YELLOW}Usage: ./translate.sh init <language_code>${NC}"
            echo "Example: ./translate.sh init fr"
            exit 1
        fi
        echo -e "${GREEN}Initializing translation for language: $2${NC}"
        # Use messages.pot from host if it exists, otherwise try /tmp/messages.pot from container
        if [ -f messages.pot ]; then
            # Copy host file to container temporarily
            docker cp messages.pot "$CONTAINER_NAME:/tmp/messages.pot" 2>/dev/null || true
            run_babel pybabel init -i /tmp/messages.pot -d translations -l "$2"
        else
            # Try to use /tmp/messages.pot if extraction was done recently
            run_babel pybabel init -i /tmp/messages.pot -d translations -l "$2" || {
                echo -e "${YELLOW}messages.pot not found. Running extract first...${NC}"
                # Extract first, then init
                run_babel pybabel extract -F babel/babel.cfg -k _l -o /tmp/messages.pot .
                run_babel pybabel init -i /tmp/messages.pot -d translations -l "$2"
            }
        fi
        echo -e "${GREEN}✓ Translation file created: translations/$2/LC_MESSAGES/messages.po${NC}"
        echo -e "${YELLOW}Now edit the .po file and translate the strings, then run: ./translate.sh compile${NC}"
        ;;
    update)
        echo -e "${GREEN}Updating translation files...${NC}"
        clean_messages_pot
        # Check if messages.pot exists, if not extract first
        if [ ! -f messages.pot ]; then
            echo -e "${YELLOW}messages.pot not found. Extracting strings first...${NC}"
            run_babel pybabel extract -F babel/babel.cfg -k _l -o /tmp/messages.pot .
            docker cp "$CONTAINER_NAME:/tmp/messages.pot" ./messages.pot.tmp 2>/dev/null || {
                run_babel sh -c "cd /know && if [ -f /tmp/messages.pot ]; then cp /tmp/messages.pot messages.pot 2>/dev/null || true; fi"
            }
            if [ -f messages.pot.tmp ]; then
                if [ -d messages.pot ]; then rm -rf messages.pot; fi
                mv messages.pot.tmp messages.pot
            fi
        fi
        # Copy messages.pot to container if it exists on host
        if [ -f messages.pot ]; then
            docker cp messages.pot "$CONTAINER_NAME:/tmp/messages.pot" 2>/dev/null || true
            run_babel pybabel update -i /tmp/messages.pot -d translations
        else
            echo -e "${YELLOW}Error: messages.pot not found. Run './translate.sh extract' first.${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓ Translation files updated${NC}"
        echo -e "${YELLOW}Review and update translations in .po files, then run: ./translate.sh compile${NC}"
        ;;
    compile)
        echo -e "${GREEN}Compiling translations...${NC}"
        run_babel pybabel compile -d translations
        echo -e "${GREEN}✓ Translations compiled${NC}"
        echo -e "${BLUE}Your translations are now active!${NC}"
        ;;
    all)
        echo -e "${GREEN}Running full translation workflow...${NC}"
        echo ""
        echo "1. Extracting strings..."
        clean_messages_pot
        run_babel pybabel extract -F babel/babel.cfg -k _l -o messages.pot .
        echo ""
        echo "2. Updating translations..."
        run_babel pybabel update -i messages.pot -d translations
        echo ""
        echo "3. Compiling translations..."
        run_babel pybabel compile -d translations
        echo ""
        echo -e "${GREEN}✓ Complete!${NC}"
        echo -e "${YELLOW}Note: If you added new strings, edit the .po files and run './translate.sh compile'${NC}"
        ;;
    *)
        echo "Usage: ./translate.sh {extract|init|update|compile|all}"
        echo ""
        echo "Commands:"
        echo "  extract  - Extract translatable strings from code and templates"
        echo "  init     - Initialize new language (usage: ./translate.sh init fr)"
        echo "  update   - Update existing translation files with new strings"
        echo "  compile  - Compile translations to binary format"
        echo "  all      - Run extract, update, and compile in sequence"
        echo ""
        echo "Examples:"
        echo "  ./translate.sh extract              # Extract strings"
        echo "  ./translate.sh init fr              # Initialize French"
        echo "  ./translate.sh update                # Update after code changes"
        echo "  ./translate.sh compile               # Compile translations"
        echo "  ./translate.sh all                  # Full workflow"
        exit 1
        ;;
esac

