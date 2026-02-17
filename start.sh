#!/bin/bash

# AI Social Intelligence Startup Script
echo "🚀 Starting AI Social Intelligence Platform..."

# Set environment variables
export DB_HOST=localhost
export DB_PORT=5433
export DB_USER=postgres
export DB_PASSWORD=password123
export DB_NAME=ai_social_db

# Start database services
echo "📊 Starting database services..."
cd /Users/tirthpatel/Documents/team/database
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Start backend server
echo "🔧 Starting backend server on port 8001..."
cd /Users/tirthpatel/Documents/team/backend
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# Start frontend server
echo "🎨 Starting frontend server on port 3001..."
cd /Users/tirthpatel/Documents/team/frontend
PATH=/Users/tirthpatel/Documents/team/backend/node-v18.19.0-darwin-arm64/bin:$PATH npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Frontend: http://localhost:3001"
echo "🔌 Backend API: http://localhost:8001"
echo "📖 API Documentation: http://localhost:8001/docs"
echo ""
echo "📧 To stop services, press Ctrl+C"
echo ""

# Wait for services
wait $BACKEND_PID $FRONTEND_PID