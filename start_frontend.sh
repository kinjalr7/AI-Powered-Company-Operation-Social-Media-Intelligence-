#!/bin/bash

# AI Social Intelligence Frontend Startup Script
echo "🎨 Starting AI Social Intelligence Frontend..."

# Start frontend server
echo "🚀 Starting Next.js development server..."
cd /Users/tirthpatel/Documents/team/frontend
PATH=/Users/tirthpatel/Documents/team/backend/node-v18.19.0-darwin-arm64/bin:$PATH npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Frontend Started Successfully!"
echo ""
echo "🌐 Frontend URL: http://localhost:3000"
echo "⚙️ Settings Page: http://localhost:3000/settings"
echo "📊 Dashboard: http://localhost:3000/dashboard"
echo ""
echo "📝 Note: Backend API calls will use fallback/demo data when backend is not running"
echo ""

# Wait for frontend
wait $FRONTEND_PID