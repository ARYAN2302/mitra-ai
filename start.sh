#!/bin/bash

# Mitra AI Recommendation Assistant - Start Script

echo "🛍️ Starting Mitra AI Recommendation Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists and has GROQ_API_KEY
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your GROQ_API_KEY."
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=.*[^[:space:]]" .env; then
    echo "❌ GROQ_API_KEY not found in .env file. Please add your API key."
    exit 1
fi

# Test the setup
echo "🧪 Running setup tests..."
python test_setup.py

if [ $? -ne 0 ]; then
    echo "❌ Setup tests failed. Please check the errors above."
    exit 1
fi

echo "✅ Setup tests passed!"

# Start FastAPI backend in background
echo "🚀 Starting FastAPI backend..."
python main.py &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 3

# Start Streamlit frontend
echo "🌟 Starting Streamlit frontend..."
streamlit run app.py &
STREAMLIT_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    kill $FASTAPI_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    wait
    echo "✅ Services stopped."
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Wait for user to stop the services
echo ""
echo "🎉 Mitra is now running!"
echo "📱 Streamlit UI: http://localhost:8501"
echo "🔧 FastAPI Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user interrupt
wait
