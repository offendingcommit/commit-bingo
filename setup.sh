#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up bingo development environment...${NC}"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Poetry not found. Installing poetry...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
poetry install

# Set up pre-commit hooks
echo -e "${GREEN}Setting up git hooks...${NC}"
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

# Run black
echo "Running black..."
poetry run black .

# Run isort
echo "Running isort..."
poetry run isort .

# Run flake8
echo "Running flake8..."
poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Run tests
echo "Running tests..."
poetry run pytest
EOF

chmod +x .git/hooks/pre-commit

echo -e "${GREEN}Setup complete! You're ready to start developing.${NC}"
echo -e "${GREEN}Run 'poetry shell' to activate the virtual environment${NC}"
echo -e "${GREEN}Run 'python app.py' to start the application${NC}"