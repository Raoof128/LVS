#!/bin/bash
echo "🚀 Starting LLM Vulnerability Scanner..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null

echo "Starting Backend..."
# Run in background
cd backend
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Backend running on PID $BACKEND_PID"
echo "Opening Dashboard..."

# Simple way to open the file
if [[ "$OSTYPE" == "darwin"* ]]; then
    open ../frontend/index.html
else
    xdg-open ../frontend/index.html
fi

echo "Press CTRL+C to stop."
wait $BACKEND_PID
