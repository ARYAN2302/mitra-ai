import streamlit as st
import requests
import json
import os
from typing import Dict, List
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Mitra - AI Shopping Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: white !important;
        transition: transform 0.2s;
        color: #333 !important;
    }
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .product-card h3 {
        color: #2c3e50 !important;
        font-weight: bold;
        margin-bottom: 0.8rem;
    }
    .product-card p {
        color: #444 !important;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .product-card strong {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    /* Force text visibility in dark themes */
    .product-card * {
        color: #333 !important;
    }
    .product-card h3,
    .product-card strong {
        color: #2c3e50 !important;
    }
    .confidence-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .high-confidence {
        background-color: #d4edda;
        color: #155724 !important;
        border: 1px solid #c3e6cb;
    }
    .medium-confidence {
        background-color: #fff3cd;
        color: #856404 !important;
        border: 1px solid #ffeaa7;
    }
    .low-confidence {
        background-color: #f8d7da;
        color: #721c24 !important;
        border: 1px solid #f5c6cb;
    }
    .recommendations-header {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        background: #f8f9fa;
    }
    .user-message {
        background: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: right;
    }
    .assistant-message {
        background: #e9ecef;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def call_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Make API calls to the FastAPI backend"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please ensure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return None

def display_product_card(product: Dict):
    """Display a product card with information"""
    confidence = product.get('confidence', 0)
    
    # Determine confidence badge class
    if confidence >= 85:
        badge_class = "high-confidence"
    elif confidence >= 70:
        badge_class = "medium-confidence"
    else:
        badge_class = "low-confidence"
    
    st.markdown(f"""
    <div class="product-card">
        <div class="confidence-badge {badge_class}">
            {confidence}% Match
        </div>
        <h3 style="color: #2c3e50 !important; font-size: 1.3rem; margin-bottom: 0.8rem;">{product['name']}</h3>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Brand:</strong> {product['brand']}</p>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Price:</strong> ₹{product['price']}</p>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Category:</strong> {product['category'].title()}</p>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Description:</strong> {product['description']}</p>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Why it's perfect:</strong> {product['reasoning']}</p>
        <p style="color: #444 !important; margin-bottom: 0.5rem;"><strong style="color: #2c3e50 !important;">Rating:</strong> {product['rating']}/5 Stars</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Mitra - AI Shopping Assistant</h1>
        <p>Your AI shopping companion.</p>
        <p>Discover food & fashion, tailored for India.</p>
        <p>Chat with our AI Shopping Bot, Mitra for instant, personalized food & fashion recommendations tailored just for you!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Quick Actions")
        
        # Sample queries
        st.subheader("Try these queries:")
        sample_queries = [
            "Vegan protein snacks under ₹300",
            "Comfortable cotton kurta for summer",
            "High-protein breakfast bars",
            "Trendy casual jeans under ₹2000",
            "Herbal tea for immunity",
            "Formal blazer for office",
            "Winter jacket for cold weather",
            "Organic smoothie ingredients",
            "Traditional silk saree",
            "Comfortable running shoes",
            "Masala chai ingredients",
            "Linen summer dress"
        ]
        
        for query in sample_queries:
            if st.button(f"{query}", key=f"sample_{query}"):
                st.session_state.current_query = query
        
        st.divider()
        
        # User preferences
        st.subheader("Your Preferences")
        
        # Dietary preferences
        dietary_prefs = st.multiselect(
            "Dietary Preferences:",
            ["Vegan", "Vegetarian", "Gluten-Free", "Organic", "High-Protein"],
            key="dietary_prefs"
        )
        
        # Style preferences
        style_prefs = st.multiselect(
            "Style Preferences:",
            ["Casual", "Ethnic", "Formal", "Trendy", "Traditional"],
            key="style_prefs"
        )
        
        # Budget range
        budget_range = st.slider(
            "Budget Range (₹):",
            min_value=0,
            max_value=5000,
            value=(0, 2000),
            step=100,
            key="budget_range"
        )
        
        if st.button("Save Preferences"):
            preferences = {
                "dietary_preferences": dietary_prefs,
                "style_preferences": style_prefs,
                "budget_range": f"{budget_range[0]}-{budget_range[1]}",
                "preferred_brands": [],
                "size_info": {},
                "interaction_history": []
            }
            
            result = call_api(f"user/{st.session_state.user_id}/preferences", "POST", preferences)
            if result:
                st.success("Preferences saved!")
        
        st.divider()
        
        # Product categories
        st.subheader("Browse Categories")
        categories = call_api("categories")
        if categories:
            for category in categories.get("categories", []):
                if st.button(f"Browse {category['name']}", key=f"browse_{category['id']}"):
                    st.session_state.browse_category = category['id']
    
    # Main content area
    col1, col2 = st.columns([3, 2])  # Make left column wider
    
    with col1:
        st.header("Chat with Mitra")
        
        # Chat interface
        with st.container():
            # Display chat history
            if st.session_state.chat_history:
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for message in st.session_state.chat_history:
                    if message['role'] == 'user':
                        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Input form
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "What are you looking for today?",
                    placeholder="e.g., comfortable cotton kurta for summer, vegan protein snacks, formal blazer for office",
                    value=st.session_state.get('current_query', '')
                )
                
                col_send, col_clear = st.columns([1, 1])
                with col_send:
                    submit_button = st.form_submit_button("Get Recommendations", use_container_width=True)
                with col_clear:
                    clear_button = st.form_submit_button("Clear Chat", use_container_width=True)
                
                if clear_button:
                    st.session_state.chat_history = []
                    st.rerun()
                
                if submit_button and user_input:
                    # Add user message to chat history
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': user_input
                    })
                    
                    # Get recommendations from API
                    with st.spinner("Finding perfect recommendations for you..."):
                        result = call_api("recommend", "POST", {
                            "query": user_input,
                            "user_id": st.session_state.user_id
                        })
                        
                        if result:
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({
                                'role': 'assistant',
                                'content': result['ai_response']
                            })
                            
                            # Store recommendations for display
                            st.session_state.current_recommendations = result['recommendations']
                            st.session_state.current_preferences = result['preferences_extracted']
                    
                    # Clear the current query
                    if 'current_query' in st.session_state:
                        del st.session_state.current_query
                    
                    st.rerun()
    
    with col2:
        st.header("AI Understanding")
        
        # Display extracted preferences
        if 'current_preferences' in st.session_state:
            prefs = st.session_state.current_preferences
            
            if prefs.get('category'):
                st.write(f"**Category:** {prefs['category'].title()}")
            
            if prefs.get('subcategory'):
                st.write(f"**Subcategory:** {prefs['subcategory'].title()}")
            
            if prefs.get('budget_max', 0) > 0:
                st.write(f"**Budget:** ₹{prefs.get('budget_min', 0)} - ₹{prefs['budget_max']}")
            
            if prefs.get('dietary_preferences'):
                st.write(f"**Dietary:** {', '.join(prefs['dietary_preferences'])}")
            
            if prefs.get('style_preferences'):
                st.write(f"**Style:** {', '.join(prefs['style_preferences'])}")
            
            if prefs.get('seasonal'):
                st.write(f"**Season:** {prefs['seasonal'].title()}")
            
            if prefs.get('extracted_keywords'):
                st.write(f"**Keywords:** {', '.join(prefs['extracted_keywords'][:5])}")
            
            # Show confidence scores
            if prefs.get('confidence_scores'):
                conf_scores = prefs['confidence_scores']
                st.write("**AI Confidence:**")
                st.write(f"- LLM: {conf_scores.get('llm_confidence', 0):.2f}")
                st.write(f"- Matching: {conf_scores.get('matching_confidence', 0):.2f}")
    
    # Display current recommendations in main area (full width)
    if 'current_recommendations' in st.session_state:
        st.markdown("---")
        st.markdown("""
        <div class="recommendations-header">
            <h2>Smart Recommendations - Powered by AI</h2>
            <p>Here are the best matches based on your preferences!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display recommendations in a grid layout
        recommendations = st.session_state.current_recommendations[:6]  # Show top 6
        
        # Create 2 columns for product display
        for i in range(0, len(recommendations), 2):
            col_left, col_right = st.columns(2)
            
            with col_left:
                if i < len(recommendations):
                    display_product_card(recommendations[i])
                    # Add to cart button
                    if st.button(f"Add to Cart", key=f"cart_{recommendations[i]['id']}"):
                        st.success(f"Added {recommendations[i]['name']} to cart!")
            
            with col_right:
                if i + 1 < len(recommendations):
                    display_product_card(recommendations[i + 1])
                    # Add to cart button
                    if st.button(f"Add to Cart", key=f"cart_{recommendations[i + 1]['id']}"):
                        st.success(f"Added {recommendations[i + 1]['name']} to cart!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Enhanced with TF-IDF Similarity Search & Advanced AI</p>
        <p>Powered by Groq Llama 3 70B • Scikit-learn • Built with Streamlit & FastAPI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
