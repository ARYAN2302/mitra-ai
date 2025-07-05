# Mitra - Enhanced AI-Powered Recommendation Assistant

An advanced AI-powered recommendation assistant for Indian D2C food and fashion brands that delivers hyper-personalized product suggestions using semantic search, embeddings, and advanced natural language processing.

## 🌟 Enhanced Features

- **Semantic Search**: Uses sentence transformers for deep understanding of user queries
- **Advanced Embeddings**: Leverages `sentence-transformers/all-MiniLM-L6-v2` for semantic similarity
- **Enhanced LLM**: Powered by Groq Llama 3 70B for superior reasoning
- **Comprehensive Product Database**: 40+ diverse products across food and fashion categories
- **Multi-Modal Understanding**: Combines LLM reasoning with embedding-based similarity
- **Confidence Scoring**: Dual confidence metrics from both LLM and embedding models
- **Indian Market Focus**: Culturally aware recommendations with ₹ pricing and seasonal trends

## 🏗️ Enhanced Architecture

### Technical Stack (As Specified)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local model, zero latency)
- **Similarity Search**: Scikit-learn `cosine_similarity` (No database setup, fast computation)
- **LLM**: Groq (Llama 3 70B) (500+ tokens/sec speed, excellent reasoning)
- **UI Framework**: Streamlit (Single-script deployment, built-in chat)
- **Data Storage**: Static JSON (No preprocessing, immediate availability)
- **Context Management**: Session state (Built-in Streamlit session handling)

### Backend (FastAPI)
- **FastAPI**: High-performance REST API with enhanced endpoints
- **SQLite**: Extended database with 40+ products across categories
- **Groq AI**: Llama 3 70B model for advanced natural language understanding
- **Sentence Transformers**: Local embedding model for semantic search
- **Hybrid Recommendation Engine**: Combines semantic similarity with traditional scoring

### Frontend (Streamlit)
- **Interactive Chat Interface**: Conversational shopping experience
- **Product Display**: Rich product cards with confidence scores
- **User Preferences**: Customizable dietary and style preferences
- **Real-time Updates**: Live chat and recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (get from [Groq Console](https://console.groq.com))

### Setup
1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/mitra
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure environment:**
   - Edit `.env` file
   - Add your `GROQ_API_KEY=your_api_key_here`

4. **Start the application:**
   
   **Terminal 1 - Start FastAPI Backend:**
   ```bash
   source venv/bin/activate
   python main.py
   ```
   
   **Terminal 2 - Start Streamlit Frontend:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

5. **Access the application:**
   - **Streamlit UI**: http://localhost:8501
   - **FastAPI Docs**: http://localhost:8000/docs

## 🎯 Sample Queries

Try these example queries to see Mitra in action:

- "Vegan snacks under ₹300"
- "Light ethnic wear for summer"
- "Protein-rich breakfast options"
- "Trendy casual wear under ₹1000"
- "Healthy breakfast cereals"
- "Cotton kurtas for hot weather"

## 📊 API Endpoints

### Core Endpoints
- `POST /recommend` - Get personalized recommendations
- `GET /products` - Browse products with filters
- `GET /categories` - Get available categories
- `GET /user/{user_id}/preferences` - Get user preferences
- `POST /user/{user_id}/preferences` - Update user preferences

### Example API Usage
```python
import requests

# Get recommendations
response = requests.post("http://localhost:8000/recommend", json={
    "query": "vegan snacks under ₹300",
    "user_id": "user123"
})

recommendations = response.json()
```

## 🗄️ Database Schema

### Products Table
- Product information (name, category, price, brand)
- Dietary information and tags
- Seasonal relevance
- Ratings and availability

### User Preferences Table
- Dietary preferences (vegan, vegetarian, etc.)
- Style preferences (casual, ethnic, etc.)
- Budget ranges and preferred brands
- Interaction history

### Recommendations Log
- Query logging for analytics
- Recommendation tracking
- Confidence scores

## 🤖 AI Engine

### Preference Extraction
The AI engine uses Groq's Llama model to extract structured preferences from natural language:
- **Dietary needs**: vegan, vegetarian, gluten-free
- **Style preferences**: casual, ethnic, formal
- **Budget constraints**: price ranges in INR
- **Specific requirements**: protein-rich, summer wear, etc.

### Recommendation Scoring
Multi-factor scoring algorithm:
- **Budget matching (30%)**: Price within user's budget
- **Category matching (25%)**: Food vs Fashion alignment
- **Dietary preferences (20%)**: Dietary requirement matching
- **Requirements matching (15%)**: Specific needs fulfillment
- **Product rating (10%)**: Quality and customer satisfaction

## 🎨 UI Features

### Chat Interface
- Real-time conversational experience
- Message history preservation
- Sample query suggestions
- Clear and intuitive design

### Product Display
- Confidence score badges
- Detailed product information
- Reasoning explanations
- Brand and pricing details

### User Preferences
- Customizable dietary preferences
- Style preference selection
- Budget range configuration
- Preference persistence

## 📈 Sample Outputs

### Query: "Vegan snacks under ₹300"
```
🌟 Plant-Based Protein Cookies - ₹299
95% Match
Why it's perfect: Within your ₹300 budget at ₹299. Perfect vegan option 
with high protein content for health-conscious snacking.

🌟 Quinoa Energy Bites - ₹249
87% Match
Why it's perfect: Vegan superfood snacks under your budget with natural 
sweetness from dates and coconut.
```

## 🔧 Configuration

### Environment Variables
```env
GROQ_API_KEY=your_groq_api_key_here
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
DEBUG=True
```

### Database Configuration
SQLite database is automatically created and seeded with sample data on first run.

## 🚀 Deployment

### Local Development
- FastAPI with uvicorn for backend
- Streamlit for frontend
- SQLite for data storage

### Production Considerations
- Use PostgreSQL for production database
- Deploy FastAPI with gunicorn
- Use Docker for containerization
- Implement proper error handling and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Groq**: For providing powerful AI capabilities
- **FastAPI**: For the high-performance backend framework
- **Streamlit**: For the intuitive frontend framework
- **Indian D2C Brands**: For inspiration and market insights

---

**Built with ❤️ for Indian D2C brands and shoppers**
