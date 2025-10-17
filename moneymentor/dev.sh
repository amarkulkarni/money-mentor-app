#!/bin/bash
# MoneyMentor Development Workflow Script
# Builds frontend and restarts FastAPI

set -e

echo "============================================================"
echo "MoneyMentor - Development Workflow"
echo "============================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Build Frontend
echo "Step 1: Building frontend..."
echo "------------------------------------------------------------"
cd app/frontend
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

echo ""
echo "✅ Frontend built successfully!"
echo ""

# Step 2: Check if FastAPI is running
echo "Step 2: Checking FastAPI status..."
echo "------------------------------------------------------------"

# Kill any existing FastAPI processes
pkill -f "python.*main.py" 2>/dev/null || true
sleep 1

# Step 3: Load environment and start FastAPI
echo ""
echo "Step 3: Starting FastAPI server..."
echo "------------------------------------------------------------"

cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Load environment variables if .env exists
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
fi

# Start FastAPI in background
cd app
nohup python3 main.py > ../fastapi.log 2>&1 &
FASTAPI_PID=$!

echo "✅ FastAPI started (PID: $FASTAPI_PID)"
echo ""

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

# Check if server is responding
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Server is running!"
else
    echo "⚠️  Server might still be starting..."
fi

echo ""
echo "============================================================"
echo "✨ Development Environment Ready!"
echo "============================================================"
echo ""
echo "🌐 Frontend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "💚 Health:   http://localhost:8000/api/health"
echo ""
echo "📝 Logs: tail -f fastapi.log"
echo "🛑 Stop:  pkill -f 'python.*main.py'"
echo ""
echo "To make frontend changes:"
echo "  1. Edit files in app/frontend/src/"
echo "  2. Run: ./dev.sh"
echo "  3. Refresh browser"
echo ""
echo "============================================================"

# Open browser (optional - comment out if you don't want this)
if command -v open &> /dev/null; then
    sleep 1
    open http://localhost:8000
fi

