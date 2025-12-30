#!/bin/bash
# One-click setup script for SmartJobHunter Pro

set -e  # Exit on error

echo "🚀 Setting up SmartJobHunter Pro..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! python3 --version | grep -q "Python 3.1[1-9]"; then
    echo "❌ Python 3.11+ required. Please install Python 3.11 or higher."
    exit 1
fi
echo "✅ Python version OK"

# Check Node.js version
echo "📋 Checking Node.js version..."
if ! node --version | grep -qE "v1[89]|v2[0-9]"; then
    echo "❌ Node.js 18+ required. Please install Node.js 18 or higher."
    exit 1
fi
echo "✅ Node.js version OK"

# Check Docker
echo "📋 Checking Docker..."
if ! docker --version &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi
echo "✅ Docker OK"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - GEMINI_API_KEY (required for AI features)"
    echo "   - Other API keys are optional"
    echo ""
    read -p "Press Enter to continue after editing .env..."
fi

# Create necessary directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/resumes data/exports logs
echo "✅ Directories created"

# Build Docker containers
echo ""
echo "🐳 Building Docker containers..."
docker-compose build

# Initialize database
echo ""
echo "🗄️  Initializing database..."
docker-compose run --rm backend python -c "from database import init_db; init_db()"

# Seed companies database
echo ""
echo "📊 Seeding companies database..."
docker-compose run --rm backend python scripts/seed_companies.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 SmartJobHunter Pro is ready to use!"
echo ""
echo "📍 To start the application:"
echo "   docker-compose up"
echo ""
echo "🌐 Once running, access:"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo "   API:      http://localhost:8000"
echo ""
echo "📝 Next steps:"
echo "   1. Make sure you've added your Gemini API key to .env"
echo "   2. Start the application with: docker-compose up"
echo "   3. Upload your resume in Settings (http://localhost:3000/settings)"
echo "   4. Run your first job scrape from the Dashboard"
echo ""
echo "🎯 Happy job hunting!"
