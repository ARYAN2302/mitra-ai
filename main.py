from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import os
from dotenv import load_dotenv

from database import DatabaseManager
from enhanced_ai_engine_basic import EnhancedAIEngine

load_dotenv()

app = FastAPI(title="Mitra - Enhanced AI Recommendation Assistant", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db_manager = DatabaseManager()
ai_engine = EnhancedAIEngine()

# Initialize product embeddings
print("🔄 Initializing product embeddings...")
products = db_manager.get_products()
ai_engine.generate_product_embeddings(products)
print("✅ System ready!")

# Pydantic models
class UserQuery(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"

class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[Dict]
    ai_response: str
    preferences_extracted: Dict

class ProductFilter(BaseModel):
    category: Optional[str] = None
    max_price: Optional[float] = None
    tags: Optional[List[str]] = None

@app.get("/")
async def root():
    return {"message": "Mitra AI Recommendation Assistant API", "status": "active"}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(query: UserQuery):
    """Get enhanced personalized recommendations based on user query"""
    try:
        # Extract user preferences using enhanced AI
        preferences = ai_engine.extract_user_preferences_enhanced(query.query)
        
        # Get products from database based on preferences
        products = db_manager.get_products(
            category=preferences.get('category') if preferences.get('category') != 'both' else None,
            max_price=preferences.get('budget_max') if preferences.get('budget_max', 0) > 0 else None,
            tags=None  # Don't filter by tags here, let the AI engine handle it
        )
        
        # Calculate enhanced recommendation scores
        recommendations = []
        for product in products:
            score, reasoning = ai_engine.calculate_enhanced_recommendation_score(product, preferences)
            
            recommendations.append({
                **product,
                'confidence': round(score * 100),
                'reasoning': reasoning
            })
        
        # Sort by confidence score
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Take top 10 recommendations
        top_recommendations = recommendations[:10]
        
        # Generate enhanced personalized AI response
        ai_response = ai_engine.generate_enhanced_response(query.query, top_recommendations, preferences)
        
        # Log the recommendation
        db_manager.log_recommendation(
            query.query, 
            preferences, 
            top_recommendations, 
            [rec['confidence'] for rec in top_recommendations]
        )
        
        return RecommendationResponse(
            query=query.query,
            recommendations=top_recommendations,
            ai_response=ai_response,
            preferences_extracted=preferences
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing recommendation: {str(e)}")

@app.get("/products")
async def get_products(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    tags: Optional[str] = None
):
    """Get products with optional filters"""
    try:
        tag_list = tags.split(',') if tags else None
        products = db_manager.get_products(category, max_price, tag_list)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@app.get("/categories")
async def get_categories():
    """Get available product categories"""
    return {
        "categories": [
            {"id": "food", "name": "Food & Beverages", "subcategories": ["snacks", "breakfast", "beverages"]},
            {"id": "fashion", "name": "Fashion", "subcategories": ["ethnic", "casual", "formal"]}
        ]
    }

@app.get("/user/{user_id}/preferences")
async def get_user_preferences(user_id: str):
    """Get user preferences"""
    try:
        preferences = db_manager.get_user_preferences(user_id)
        return {"preferences": preferences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preferences: {str(e)}")

@app.post("/user/{user_id}/preferences")
async def update_user_preferences(user_id: str, preferences: Dict):
    """Update user preferences"""
    try:
        db_manager.update_user_preferences(user_id, preferences)
        return {"message": "Preferences updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating preferences: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-07-05"}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=os.getenv("FASTAPI_HOST", "127.0.0.1"), 
        port=int(os.getenv("FASTAPI_PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
