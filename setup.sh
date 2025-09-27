#!/bin/bash

# Asterix Project Setup Script
echo "🚀 Setting up Asterix - Asteroid Visualization Tool"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please update .env file with your configuration before running the application."
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p frontend/public/cesium
mkdir -p database/migrations

# Copy Cesium assets to public directory
echo "🌍 Setting up Cesium assets..."
if [ -d "frontend/node_modules/cesium/Build/Cesium" ]; then
    cp -r frontend/node_modules/cesium/Build/Cesium/* frontend/public/cesium/
    echo "✅ Cesium assets copied to public directory"
else
    echo "⚠️  Cesium assets not found. Run 'npm install' in frontend directory first."
fi

# Set up database migrations
echo "🗄️  Setting up database migrations..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
    alembic revision --autogenerate -m "Initial migration"
    echo "✅ Database migration created"
else
    echo "⚠️  Virtual environment not found. Please run 'python3 -m venv venv' and 'pip install -r requirements.txt' in backend directory first."
fi
cd ..

# Build and start services
echo "🐳 Building and starting Docker services..."
cd deployment
docker-compose build
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Application URLs:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📚 Next steps:"
    echo "   1. Update .env file with your NASA API key"
    echo "   2. Visit http://localhost:3000 to see the application"
    echo "   3. Check http://localhost:8000/docs for API documentation"
else
    echo "❌ Some services failed to start. Check logs with 'docker-compose logs'"
fi

cd ..
echo "🎉 Setup complete!"
