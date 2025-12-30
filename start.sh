#!/bin/bash
# Simple startup script for SmartJobHunter Pro

echo "🚀 Starting SmartJobHunter Pro with Docker..."
echo ""

# Stop any running containers
echo "🛑 Stopping any existing containers..."
sudo docker compose down

echo ""
echo "🔨 Building containers..."
sudo docker compose build

echo ""
echo "🚀 Starting services..."
sudo docker compose up -d

echo ""
echo "⏳ Waiting for services to start (45 seconds)..."
sleep 45

echo ""
echo "✅ Checking status..."
sudo docker compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Access your application:"
echo ""
echo "   📊 Frontend Dashboard: http://localhost:3000"
echo "   📖 API Documentation:  http://localhost:8000/docs"
echo "   ✅ Health Check:       http://localhost:8000/health"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Useful commands:"
echo "   View logs:    cd jobHunter && sudo docker compose logs -f"
echo "   Stop:         cd jobHunter && sudo docker compose down"
echo "   Restart:      cd jobHunter && sudo docker compose restart"
echo ""
echo "🎉 Ready to use! Visit http://localhost:3000"
