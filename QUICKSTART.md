# 🛍️ Mitra AI Recommendation Assistant - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Groq API Key (free from [console.groq.com](https://console.groq.com))

## Installation Steps

### 1. Get Your Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Create a new API key
4. Copy the API key

### 2. Setup the Project
```bash
# Navigate to the project directory
cd /Users/adarshthakur/Desktop/mitra

# Run the setup script
./setup.sh
```

### 3. Configure Environment
Edit the `.env` file and add your Groq API key:
```env
GROQ_API_KEY=your_actual_api_key_here
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
DEBUG=True
```

### 4. Test the Setup
```bash
python test_setup.py
```

### 5. Start the Application
```bash
# Option 1: Use the start script (recommended)
./start.sh

# Option 2: Manual start
# Terminal 1 - FastAPI Backend
python main.py

# Terminal 2 - Streamlit Frontend
streamlit run app.py
```

## Access the Application
- **Chat Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## Quick Test
Try these sample queries in the chat:
- "Vegan snacks under ₹300"
- "Light ethnic wear for summer"
- "Protein-rich breakfast options"

## Troubleshooting

### Common Issues
1. **Import Errors**: Run `pip install -r requirements.txt`
2. **API Connection Error**: Ensure FastAPI is running on port 8000
3. **Groq API Error**: Check your API key in `.env` file
4. **Database Error**: Delete `recommendation_db.sqlite` and restart

### Getting Help
- Check the logs in the terminal
- Verify all dependencies are installed
- Ensure Python version is 3.8+
- Make sure ports 8000 and 8501 are available

## Next Steps
1. Customize the product database in `database.py`
2. Adjust recommendation scoring in `ai_engine.py`
3. Modify the UI in `app.py`
4. Add more product categories and brands

Happy shopping with Mitra! 🎉
