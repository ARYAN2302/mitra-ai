from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import pickle
import os
from typing import Dict, List, Optional, Tuple
from groq import Groq
import re
from dotenv import load_dotenv

load_dotenv()

class EnhancedAIEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"  # Using Llama 3 70B for better reasoning
        
        # Initialize TF-IDF vectorizer for basic text similarity
        print("Initializing TF-IDF vectorizer...")
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Cache for embeddings
        self.embeddings_cache = {}
        self.embeddings_file = "embeddings_cache.pkl"
        self.product_vectors = None
        self.product_descriptions = []
        
        # Product categories and their embeddings
        self.categories = {
            "food": {
                "snacks": ["chips", "cookies", "crackers", "nuts", "protein bars", "energy bites"],
                "breakfast": ["cereals", "oats", "bread", "pancakes", "smoothies", "bars"],
                "beverages": ["tea", "coffee", "juice", "smoothies", "protein shakes"],
                "healthy": ["organic", "vegan", "gluten-free", "protein-rich", "low-sugar"],
                "traditional": ["millet", "quinoa", "chia seeds", "ancient grains"]
            },
            "fashion": {
                "ethnic": ["kurta", "saree", "lehenga", "palazzo", "dupatta", "traditional"],
                "casual": ["t-shirt", "jeans", "shorts", "hoodie", "sneakers", "casual wear"],
                "formal": ["shirt", "pants", "blazer", "dress", "formal wear", "office wear"],
                "seasonal": ["summer", "winter", "monsoon", "cotton", "linen", "warm"],
                "style": ["trendy", "classic", "modern", "vintage", "bohemian", "minimalist"]
            }
        }
        
        print("Enhanced AI Engine initialized successfully!")
    
    def generate_product_embeddings(self, products: List[Dict]):
        """Generate TF-IDF vectors for all products"""
        print(f"Generating TF-IDF vectors for {len(products)} products...")
        
        # Create product descriptions
        self.product_descriptions = []
        for product in products:
            desc = f"{product['name']} {product['brand']} {product['category']} {' '.join(product.get('tags', []))}"
            self.product_descriptions.append(desc)
        
        # Fit vectorizer and transform descriptions
        if self.product_descriptions:
            self.product_vectors = self.vectorizer.fit_transform(self.product_descriptions)
            print(f"✅ Generated TF-IDF vectors for {len(products)} products")
        else:
            print("⚠️ No products to vectorize")
    
    def get_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using TF-IDF"""
        try:
            vectors = self.vectorizer.transform([text1, text2])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return similarity
        except:
            return 0.0
    
    def extract_user_preferences_enhanced(self, user_query: str) -> Dict:
        """Enhanced preference extraction using category matching and LLM"""
        
        # Find similar categories using basic text matching
        query_lower = user_query.lower()
        category_scores = {}
        
        for category, subcategories in self.categories.items():
            max_score = 0
            best_matches = []
            
            for subcategory, keywords in subcategories.items():
                for keyword in keywords:
                    if keyword in query_lower:
                        score = 1.0
                        best_matches.append((keyword, score, subcategory))
                        max_score = max(max_score, score)
                    else:
                        # Basic similarity check
                        score = self.get_text_similarity(query_lower, keyword)
                        if score > 0.3:
                            best_matches.append((keyword, score, subcategory))
                            max_score = max(max_score, score)
            
            if best_matches:
                category_scores[category] = {
                    'score': max_score,
                    'matches': sorted(best_matches, key=lambda x: x[1], reverse=True)[:5]
                }
        
        # Use LLM for structured extraction
        llm_preferences = self.extract_with_llm(user_query)
        
        # Combine basic matching and LLM results
        enhanced_preferences = self.combine_preferences(llm_preferences, category_scores, user_query)
        
        return enhanced_preferences
    
    def extract_with_llm(self, user_query: str) -> Dict:
        """Extract preferences using LLM"""
        prompt = f"""
        Analyze this Indian shopping query and extract structured preferences in JSON format.
        
        Query: "{user_query}"
        
        Extract:
        1. Main category (food/fashion/both)
        2. Subcategory (snacks, breakfast, ethnic, casual, etc.)
        3. Dietary preferences (vegan, vegetarian, gluten-free, organic, etc.)
        4. Style preferences (casual, ethnic, formal, trendy, traditional, etc.)
        5. Budget (extract ₹ amounts)
        6. Specific requirements (protein-rich, summer wear, cotton, etc.)
        7. Occasion (breakfast, party, office, casual outing, etc.)
        8. Brand preferences (if mentioned)
        9. Size/fit preferences (if mentioned)
        10. Color preferences (if mentioned)
        
        Consider Indian context:
        - Traditional vs modern preferences
        - Seasonal requirements (summer/winter/monsoon)
        - Regional preferences
        - Festival/occasion wear
        
        Return JSON:
        {{
            "category": "food" or "fashion" or "both",
            "subcategory": "specific subcategory",
            "dietary_preferences": ["vegan", "organic"],
            "style_preferences": ["casual", "trendy"],
            "budget_min": 0,
            "budget_max": 1000,
            "specific_requirements": ["protein-rich", "cotton"],
            "occasion": "breakfast",
            "brand_preferences": ["specific brands"],
            "size_preferences": {{"size": "M", "fit": "regular"}},
            "color_preferences": ["blue", "black"],
            "seasonal": "summer",
            "urgency": "normal",
            "quantity": 1
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert at extracting detailed shopping preferences from Indian consumer queries. Always return valid JSON with comprehensive details."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._fallback_extraction(user_query)
                
        except Exception as e:
            print(f"Error in LLM extraction: {e}")
            return self._fallback_extraction(user_query)
    
    def combine_preferences(self, llm_prefs: Dict, category_scores: Dict, user_query: str) -> Dict:
        """Combine LLM and basic matching preferences"""
        
        # Start with LLM preferences
        enhanced_prefs = llm_prefs.copy()
        
        # Add semantic matches from basic matching
        enhanced_prefs['semantic_matches'] = category_scores
        
        # Determine primary category based on both methods
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1]['score'])
            if best_category[1]['score'] > 0.5:
                enhanced_prefs['category'] = best_category[0]
        
        # Extract keywords from matches
        extracted_keywords = []
        for category, data in category_scores.items():
            for match in data['matches']:
                extracted_keywords.append(match[0])
        
        enhanced_prefs['extracted_keywords'] = extracted_keywords
        
        # Calculate confidence scores
        enhanced_prefs['confidence_scores'] = {
            'llm_confidence': self._calculate_llm_confidence(llm_prefs),
            'matching_confidence': max([data['score'] for data in category_scores.values()]) if category_scores else 0.0
        }
        
        return enhanced_prefs
    
    def _calculate_llm_confidence(self, preferences: Dict) -> float:
        """Calculate confidence score for LLM extraction"""
        score = 0.0
        
        # Check if key fields are populated
        if preferences.get('category') in ['food', 'fashion', 'both']:
            score += 0.3
        
        if preferences.get('subcategory'):
            score += 0.2
        
        if preferences.get('budget_max', 0) > 0:
            score += 0.2
        
        if preferences.get('dietary_preferences') or preferences.get('style_preferences'):
            score += 0.2
        
        if preferences.get('specific_requirements'):
            score += 0.1
        
        return min(score, 1.0)
    
    def calculate_enhanced_recommendation_score(self, product: Dict, preferences: Dict) -> Tuple[float, str]:
        """Calculate enhanced recommendation score for a product"""
        
        score = 0.0
        reasoning_parts = []
        
        # Category matching (30%)
        if preferences.get('category') == product['category']:
            score += 0.3
            reasoning_parts.append(f"Perfect category match ({product['category']})")
        elif preferences.get('category') == 'both':
            score += 0.2
            reasoning_parts.append(f"Category compatible ({product['category']})")
        
        # Product type matching (special bonus 20%)
        extracted_keywords = preferences.get('extracted_keywords', [])
        product_name_lower = product['name'].lower()
        product_tags_lower = [tag.lower() for tag in product.get('tags', [])]
        
        for keyword in extracted_keywords:
            keyword_lower = keyword.lower()
            # Check for t-shirt specific matches
            if keyword_lower in ['t-shirt', 'tshirt', 'tee']:
                if any(tag in ['tee', 'tshirt'] for tag in product_tags_lower) or 'tee' in product_name_lower:
                    score += 0.2
                    reasoning_parts.append(f"Perfect product type match ({keyword})")
                    break
            # Check for other direct matches
            elif keyword_lower in product_name_lower or any(keyword_lower in tag for tag in product_tags_lower):
                score += 0.15
                reasoning_parts.append(f"Product type match ({keyword})")
                break
        
        # Subcategory matching (bonus 15%)
        if preferences.get('subcategory') and product.get('subcategory'):
            if preferences.get('subcategory').lower() in product.get('subcategory', '').lower():
                score += 0.15
                reasoning_parts.append(f"Subcategory match ({product['subcategory']})")
            elif product.get('subcategory', '').lower() in preferences.get('subcategory', '').lower():
                score += 0.1
                reasoning_parts.append(f"Subcategory compatible ({product['subcategory']})")
        
        # Price matching (25%)
        budget_max = preferences.get('budget_max', 0)
        if budget_max > 0:
            if product['price'] <= budget_max:
                price_score = 0.25 * (1 - (product['price'] / budget_max) * 0.5)
                score += price_score
                reasoning_parts.append(f"Within budget (₹{product['price']} ≤ ₹{budget_max})")
            else:
                reasoning_parts.append(f"Over budget (₹{product['price']} > ₹{budget_max})")
        else:
            score += 0.15  # Neutral score if no budget specified
            reasoning_parts.append("No budget constraint")
        
        # Tag/preference matching (25%)
        product_tags = set(product.get('tags', []))
        user_prefs = set(preferences.get('dietary_preferences', []) + 
                        preferences.get('style_preferences', []) + 
                        preferences.get('specific_requirements', []) +
                        preferences.get('extracted_keywords', []))
        
        # Also check for partial matches in product tags
        product_tags_lower = set([tag.lower() for tag in product_tags])
        user_prefs_lower = set([pref.lower() for pref in user_prefs])
        
        # Check for exact matches
        exact_matches = product_tags_lower.intersection(user_prefs_lower)
        
        # Check for meaningful partial matches (at least 3 characters)
        partial_matches = set()
        for user_pref in user_prefs_lower:
            if len(user_pref) >= 3:  # Only consider meaningful words
                for product_tag in product_tags_lower:
                    if len(product_tag) >= 3:  # Only consider meaningful tags
                        # Special case for t-shirt variations
                        if (user_pref in ["t-shirt", "tshirt"] and product_tag in ["tee", "tshirt", "t-shirt"]) or \
                           (user_pref == "tee" and product_tag in ["tshirt", "t-shirt"]):
                            partial_matches.add(product_tag)
                        # Check if words contain each other (but not single letters)
                        elif (user_pref in product_tag or product_tag in user_pref) and \
                             len(user_pref) > 2 and not any(c.isdigit() for c in user_pref):
                            partial_matches.add(product_tag)
        
        all_matches = exact_matches.union(partial_matches)
        
        if user_prefs:
            if all_matches:
                # Give higher score for more matches
                tag_score = 0.25 * min(1.0, len(all_matches) / max(1, len(user_prefs_lower)))
                
                # Special bonus for t-shirt matches
                if any(match in ["tee", "tshirt"] for match in all_matches):
                    tag_score += 0.15  # Extra bonus for t-shirt matches
                    reasoning_parts.append(f"T-shirt match: {', '.join(list(all_matches)[:3])}")
                else:
                    reasoning_parts.append(f"Matches preferences: {', '.join(list(all_matches)[:3])}")
                
                score += tag_score
            else:
                reasoning_parts.append("No specific preference matches")
        else:
            score += 0.1  # Neutral score if no preferences
        
        # Brand matching (10%)
        brand_prefs = preferences.get('brand_preferences', [])
        if brand_prefs:
            if product['brand'] in brand_prefs:
                score += 0.1
                reasoning_parts.append(f"Preferred brand ({product['brand']})")
            else:
                reasoning_parts.append(f"Different brand ({product['brand']})")
        else:
            score += 0.05  # Neutral score
        
        # Rating boost (10%)
        rating_score = (product.get('rating', 3) / 5) * 0.1
        score += rating_score
        reasoning_parts.append(f"Quality rating: {product.get('rating', 3)}/5")
        
        # Text similarity with product description
        if hasattr(self, 'product_vectors') and self.product_vectors is not None:
            try:
                user_query_vector = self.vectorizer.transform([preferences.get('original_query', '')])
                product_idx = self.product_descriptions.index(
                    f"{product['name']} {product['brand']} {product['category']} {' '.join(product.get('tags', []))}"
                )
                text_sim = cosine_similarity(user_query_vector, self.product_vectors[product_idx:product_idx+1])[0][0]
                score += text_sim * 0.1
                if text_sim > 0.3:
                    reasoning_parts.append(f"High text similarity ({text_sim:.2f})")
            except:
                pass
        
        # Ensure score is between 0 and 1
        score = max(0, min(1, score))
        
        # Create reasoning string
        reasoning = " • ".join(reasoning_parts)
        
        return score, reasoning
    
    def generate_enhanced_response(self, user_query: str, recommendations: List[Dict], preferences: Dict) -> str:
        """Generate enhanced personalized AI response"""
        
        if not recommendations:
            return self._generate_no_results_response(user_query, preferences)
        
        # Prepare context for LLM
        context = {
            'user_query': user_query,
            'preferences': preferences,
            'recommendations': recommendations[:5],  # Top 5 for context
            'category_insights': preferences.get('semantic_matches', {}),
            'confidence_scores': preferences.get('confidence_scores', {})
        }
        
        prompt = f"""
        You are Mitra, an AI shopping assistant for Indian D2C brands. Create a personalized, helpful response.
        
        User Query: "{user_query}"
        
        User Preferences Extracted:
        - Category: {preferences.get('category', 'Not specified')}
        - Subcategory: {preferences.get('subcategory', 'Not specified')}
        - Budget: ₹{preferences.get('budget_min', 0)}-{preferences.get('budget_max', 'No limit')}
        - Dietary/Style Preferences: {', '.join(preferences.get('dietary_preferences', []) + preferences.get('style_preferences', []))}
        - Specific Requirements: {', '.join(preferences.get('specific_requirements', []))}
        - Occasion: {preferences.get('occasion', 'Not specified')}
        
        Top Recommendations:
        {self._format_recommendations_for_prompt(recommendations)}
        
        Create a response that:
        1. Acknowledges the user's specific needs
        2. Explains why these recommendations are perfect for them
        3. Highlights key benefits of top 3 products
        4. Provides helpful shopping tips
        5. Maintains a friendly, enthusiastic tone
        6. Uses Indian context and culturally relevant language
        7. Includes emojis and formatting for better readability
        
        Keep the response conversational, informative, and actionable.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Mitra, a friendly AI shopping assistant specializing in Indian D2C brands. You provide personalized, culturally relevant recommendations with enthusiasm and expertise."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self._generate_fallback_response(user_query, recommendations)
    
    def _format_recommendations_for_prompt(self, recommendations: List[Dict]) -> str:
        """Format recommendations for LLM prompt"""
        formatted = ""
        for i, rec in enumerate(recommendations, 1):
            formatted += f"{i}. {rec['name']} - ₹{rec['price']} ({rec['confidence']}% match)\n"
            formatted += f"   Brand: {rec['brand']}\n"
            formatted += f"   Reasoning: {rec['reasoning']}\n"
            formatted += f"   Rating: {rec['rating']}/5\n\n"
        return formatted
    
    def _generate_no_results_response(self, user_query: str, preferences: Dict) -> str:
        """Generate response when no products match"""
        return f"""
        I understand you're looking for {user_query}, but I couldn't find exact matches in our current collection. 
        
        Here are some suggestions:
        • Try adjusting your budget range
        • Consider similar categories
        • Check back later as we regularly add new products
        
        Would you like me to suggest alternatives or help you refine your search? 🤔
        """
    
    def _generate_fallback_response(self, user_query: str, recommendations: List[Dict]) -> str:
        """Fallback response generation"""
        response = f"Great! I found some excellent options for you:\n\n"
        
        for i, rec in enumerate(recommendations[:3], 1):
            response += f"🌟 **{rec['name']}** - ₹{rec['price']}\n"
            response += f"✨ {rec['confidence']}% Match\n"
            response += f"💡 {rec['reasoning']}\n\n"
        
        return response
    
    def _fallback_extraction(self, user_query: str) -> Dict:
        """Fallback extraction method"""
        query_lower = user_query.lower()
        
        # Extract budget
        budget_match = re.search(r'₹\s*(\d+)', query_lower)
        budget_match_alt = re.search(r'under\s+(\d+)', query_lower)
        budget_max = 0
        
        if budget_match:
            budget_max = int(budget_match.group(1))
        elif budget_match_alt:
            budget_max = int(budget_match_alt.group(1))
        
        # Basic category detection
        food_keywords = ['snacks', 'food', 'breakfast', 'protein', 'vegan', 'meal', 'drink', 'cereal']
        fashion_keywords = ['wear', 'clothes', 'kurta', 'tee', 'shirt', 'dress', 'jacket', 'pants']
        
        category = "both"
        if any(keyword in query_lower for keyword in food_keywords):
            category = "food"
        elif any(keyword in query_lower for keyword in fashion_keywords):
            category = "fashion"
        
        return {
            "category": category,
            "subcategory": "",
            "dietary_preferences": [],
            "style_preferences": [],
            "budget_min": 0,
            "budget_max": budget_max,
            "specific_requirements": [],
            "occasion": "",
            "brand_preferences": [],
            "size_preferences": {},
            "color_preferences": [],
            "seasonal": "",
            "urgency": "normal",
            "quantity": 1,
            "extracted_keywords": [],
            "confidence_scores": {
                "llm_confidence": 0.3,
                "matching_confidence": 0.2
            },
            "original_query": user_query
        }
