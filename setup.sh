#!/bin/bash

# Mitra AI Recommendation Assistant - Setup Script

echo "🛍️ Setting up Mitra AI Recommendation Assistant..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo "📥 Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env .env.example
    echo "Please edit .env file and add your GROQ_API_KEY"
fi

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from database import DatabaseManager; db = DatabaseManager(); print('Database initialized successfully!')"

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Add your GROQ_API_KEY to .env file"
echo "3. Start FastAPI server: python main.py"
echo "4. In a new terminal, start Streamlit: streamlit run app.py"
echo ""
echo "🚀 Happy shopping with Mitra!"
