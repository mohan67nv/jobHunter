#!/bin/bash

# Build Script for SmartJobHunter Pro
# This script handles Docker build issues and ensures clean deployment

echo "🚀 SmartJobHunter Pro - Build & Deploy Script"
echo "=============================================="

# Stop any running containers
echo ""
echo "📦 Stopping existing containers..."
sudo docker compose down

# Remove dangling images to free up space
echo ""
echo "🧹 Cleaning up dangling images..."
sudo docker image prune -f

# Build with no cache to avoid snapshot issues
echo ""
echo "🔨 Building frontend (this may take a few minutes)..."
sudo docker compose build --no-cache frontend

echo ""
echo "🔨 Building backend..."
sudo docker compose build --no-cache backend

# Start all services
echo ""
echo "🚀 Starting all services..."
sudo docker compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo ""
echo "📊 Service Status:"
sudo docker compose ps

# Show logs
echo ""
echo "📋 Recent logs:"
sudo docker compose logs --tail=20

echo ""
echo "✅ Build complete!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 To view live logs: sudo docker compose logs -f"
echo "🛑 To stop: ./stop.sh or sudo docker compose down"
