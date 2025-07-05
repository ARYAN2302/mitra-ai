# Mitra - AI-Powered Shopping Assistant

An intelligent shopping assistant for Indian D2C food and fashion brands. Just tell Mitra what you're looking for in plain English, and it will find the perfect products for you!

## What is Mitra?

Mitra is your personal shopping assistant that understands what you want and helps you find the best products from Indian brands. Think of it as having a smart friend who knows all the best food and fashion items and can instantly recommend what's perfect for you.

## How Does It Work? (Simple Explanation)

1. **You Ask**: Type what you want in natural language, like "I need healthy snacks under ₹300" or "Show me cotton kurtas for summer"

2. **Mitra Understands**: The AI reads your message and figures out:
   - What type of product you want (food or fashion)
   - Your budget
   - Your preferences (vegan, cotton, summer, etc.)

3. **Mitra Searches**: It looks through a database of 40+ products from Indian brands and finds the best matches using smart algorithms

4. **Mitra Recommends**: It shows you the top products with explanations of why they're perfect for you

## Key Features

- **Smart Search**: Understands natural language - no need for exact keywords
- **Budget Aware**: Respects your price range and shows affordable options
- **Preference Matching**: Remembers if you're vegan, prefer cotton, etc.
- **Indian Brands**: Focuses on Indian D2C food and fashion brands
- **Confidence Scores**: Shows how well each product matches your needs
- **Clean Interface**: Simple, professional design without distractions

## Technical Stack

### Current Setup
- **Backend**: FastAPI (handles the smart recommendations)
- **Frontend**: Streamlit (the chat interface you see)
- **Database**: SQLite (stores product information)
- **AI Engine**: Groq LLM + TF-IDF (the "brain" that understands and recommends)
- **Search**: Semantic similarity using TF-IDF vectorization

### Why This Stack?
- **Fast**: TF-IDF provides quick semantic search without heavy dependencies
- **Reliable**: SQLite works perfectly for our product database
- **Smart**: Groq LLM understands complex queries in natural language
- **Simple**: Streamlit makes it easy to chat with the AI
- **Efficient**: FastAPI handles requests quickly and reliably

## Quick Start Guide

### What You Need
- Python 3.8 or higher
- A Groq API key (free from [Groq Console](https://console.groq.com))

### Installation Steps

1. **Download the project:**
   ```bash
   git clone https://github.com/ARYAN2302/mitra-ai.git
   cd mitra-ai
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

4. **Start the application:**
   
   **Option 1: Quick Start (Recommended)**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   
   **Option 2: Manual Start**
   
   Open two terminals:
   
   **Terminal 1 - Backend:**
   ```bash
   source venv/bin/activate
   python main.py
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

5. **Start shopping:**
   - Open your browser to http://localhost:8501
   - Start chatting with Mitra!

## How to Use Mitra

### Sample Conversations

**For Food Products:**
- "I want healthy breakfast options under ₹200"
- "Show me vegan snacks"
- "I need protein-rich food for my workout"
- "Suggest some organic cereals"

**For Fashion:**
- "I need cotton kurtas for summer"
- "Show me casual wear under ₹1000"
- "Comfortable ethnic wear for office"
- "Lightweight shirts for hot weather"

### Tips for Best Results
- Be specific about your budget (e.g., "under ₹500")
- Mention your preferences (vegan, cotton, casual, etc.)
- Ask follow-up questions to refine recommendations
- Check the confidence scores to see how well products match

## Understanding the Results

### Confidence Scores
- **90-100%**: Perfect match for your requirements
- **80-89%**: Very good match with minor differences
- **70-79%**: Good match but may not meet all criteria
- **Below 70%**: Partial match, consider if it works for you

### Why This Product?
Each recommendation includes an explanation of why Mitra chose it for you, based on:
- Your budget requirements
- Dietary or style preferences
- Product category match
- Quality and ratings

## For Developers

### Project Structure
```
mitra-ai/
├── app.py              # Streamlit frontend (main chat interface)
├── main.py             # FastAPI backend (API server)
├── database.py         # SQLite database setup and operations
├── enhanced_ai_engine_basic.py  # AI recommendation engine
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── README.md          # This file
└── start.sh           # Quick start script
```

### Key Components

1. **FastAPI Backend (main.py)**
   - Provides REST API endpoints
   - Handles recommendation requests
   - Manages database operations
   - Runs on http://localhost:8000

2. **Streamlit Frontend (app.py)**
   - Chat interface for users
   - Displays product recommendations
   - Handles user interactions
   - Runs on http://localhost:8501

3. **AI Engine (enhanced_ai_engine_basic.py)**
   - Processes natural language queries
   - Uses Groq LLM for understanding
   - Implements TF-IDF for semantic search
   - Scores and ranks products

4. **Database (database.py)**
   - SQLite database with product information
   - Automatically creates and populates data
   - Handles user preferences

### API Endpoints

The FastAPI backend provides these endpoints:

- `GET /` - Health check
- `POST /recommend` - Get product recommendations
- `GET /products` - List all products
- `GET /categories` - Get product categories
- `GET /health` - System health status

### Technology Choices Explained

**Why Groq?**
- Fast inference (500+ tokens/second)
- Excellent reasoning capabilities
- Free tier available
- Easy API integration

**Why TF-IDF instead of embeddings?**
- Lighter weight, fewer dependencies
- Good performance for our use case
- Faster startup time
- No GPU requirements

**Why SQLite?**
- Perfect for development and small datasets
- No setup required
- Fast for our product catalog size
- Easy to inspect and modify

**Why Streamlit?**
- Rapid prototyping
- Built-in chat interface
- Easy to customize
- Perfect for AI applications

