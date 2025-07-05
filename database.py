import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path: str = "recommendation_db.sqlite"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                price REAL NOT NULL,
                brand TEXT NOT NULL,
                description TEXT,
                tags TEXT,
                dietary_info TEXT,
                seasonal_relevance TEXT,
                image_url TEXT,
                availability BOOLEAN DEFAULT 1,
                rating REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                dietary_preferences TEXT,
                style_preferences TEXT,
                budget_range TEXT,
                preferred_brands TEXT,
                size_info TEXT,
                interaction_history TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Recommendations log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT NOT NULL,
                user_preferences TEXT,
                recommended_products TEXT,
                confidence_scores TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        self.seed_sample_data()
    
    def seed_sample_data(self):
        """Seed the database with comprehensive sample products"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        sample_products = [
            # FOOD PRODUCTS
            # Snacks
            ("Plant-Based Protein Cookies", "food", "snacks", 299, "GreenBite", 
             "Gluten-free vegan cookies with 12g plant protein per serving", 
             "vegan,protein,gluten-free,healthy,cookies,snacks", "vegan,gluten-free", "all-seasons", 
             "https://example.com/cookies.jpg", True, 4.5),
            
            ("Quinoa Energy Bites", "food", "snacks", 249, "SuperFoods", 
             "Vegan superfood snacks with natural sweetness from dates and coconut",
             "vegan,superfood,energy,natural,quinoa,bites,healthy", "vegan,organic", "all-seasons",
             "https://example.com/bites.jpg", True, 4.3),
            
            ("Masala Peanuts", "food", "snacks", 149, "Desi Munch", 
             "Traditional Indian roasted peanuts with spicy masala coating",
             "spicy,traditional,peanuts,masala,indian,crunchy", "vegetarian", "all-seasons",
             "https://example.com/peanuts.jpg", True, 4.2),
            
            ("Banana Chips", "food", "snacks", 129, "Kerala Delights", 
             "Crispy banana chips made from fresh Kerala bananas",
             "crispy,banana,chips,kerala,traditional,south-indian", "vegetarian", "all-seasons",
             "https://example.com/banana-chips.jpg", True, 4.4),
            
            ("Protein Bars - Chocolate", "food", "snacks", 399, "FitFuel", 
             "High-protein chocolate bars with 20g protein per serving",
             "protein,chocolate,bars,fitness,high-protein,energy", "vegetarian", "all-seasons",
             "https://example.com/protein-bars.jpg", True, 4.6),
            
            # Breakfast Items
            ("Oats & Chia Seed Bars", "food", "breakfast", 349, "HealthyStart",
             "Protein-rich breakfast bars with 15g plant protein per serving",
             "protein,breakfast,healthy,oats,chia,bars,energy", "vegetarian,high-protein", "all-seasons",
             "https://example.com/bars.jpg", True, 4.4),
            
            ("Millet Breakfast Cereal", "food", "breakfast", 199, "AncientGrains",
             "Traditional Indian millets with modern nutrition",
             "millet,traditional,breakfast,fiber,cereal,healthy", "vegetarian,gluten-free", "all-seasons",
             "https://example.com/cereal.jpg", True, 4.2),
            
            ("Granola - Honey & Nuts", "food", "breakfast", 459, "Morning Bliss", 
             "Crunchy granola with honey, almonds, and cashews",
             "granola,honey,nuts,crunchy,breakfast,healthy", "vegetarian", "all-seasons",
             "https://example.com/granola.jpg", True, 4.5),
            
            ("Instant Oats - Masala", "food", "breakfast", 179, "Quick Bowl", 
             "Indian-style masala oats ready in 2 minutes",
             "oats,masala,instant,indian,quick,breakfast", "vegetarian", "all-seasons",
             "https://example.com/masala-oats.jpg", True, 4.1),
            
            ("Smoothie Mix - Green", "food", "breakfast", 329, "Nutri Blend", 
             "Organic green smoothie mix with spinach and fruits",
             "smoothie,green,organic,healthy,spinach,fruits", "vegan,organic", "all-seasons",
             "https://example.com/smoothie-mix.jpg", True, 4.3),
            
            # Beverages
            ("Herbal Tea - Tulsi", "food", "beverages", 249, "Ayur Tea", 
             "Traditional tulsi tea with immunity-boosting properties",
             "tea,tulsi,herbal,immunity,ayurvedic,healthy", "vegan", "all-seasons",
             "https://example.com/tulsi-tea.jpg", True, 4.7),
            
            ("Cold Brew Coffee", "food", "beverages", 399, "Brew Masters", 
             "Smooth cold brew coffee concentrate",
             "coffee,cold-brew,concentrate,smooth,caffeine", "vegan", "summer",
             "https://example.com/cold-brew.jpg", True, 4.4),
            
            ("Kombucha - Ginger", "food", "beverages", 299, "Ferment Co", 
             "Probiotic ginger kombucha for gut health",
             "kombucha,ginger,probiotic,fermented,healthy", "vegan", "all-seasons",
             "https://example.com/kombucha.jpg", True, 4.2),
            
            ("Coconut Water", "food", "beverages", 99, "Tropical Pure", 
             "Natural coconut water with electrolytes",
             "coconut,water,natural,electrolytes,hydration", "vegan", "summer",
             "https://example.com/coconut-water.jpg", True, 4.0),
            
            ("Protein Shake - Vanilla", "food", "beverages", 599, "Muscle Fuel", 
             "Whey protein shake with 25g protein per serving",
             "protein,shake,vanilla,whey,muscle,fitness", "vegetarian", "all-seasons",
             "https://example.com/protein-shake.jpg", True, 4.5),
            
            # FASHION PRODUCTS
            # Ethnic Wear
            ("Handblock Print Kurta", "fashion", "ethnic", 1499, "Craftsman",
             "100% cotton kurta with traditional handblock prints",
             "ethnic,cotton,traditional,summer,kurta,handblock", "", "summer,monsoon",
             "https://example.com/kurta.jpg", True, 4.6),
            
            ("Silk Saree - Banarasi", "fashion", "ethnic", 4999, "Weave Heritage", 
             "Authentic Banarasi silk saree with gold zari work",
             "saree,silk,banarasi,traditional,gold,zari,wedding", "", "all-seasons",
             "https://example.com/saree.jpg", True, 4.8),
            
            ("Linen Palazzo Pants", "fashion", "ethnic", 1299, "ComfortWear",
             "Breathable linen palazzo pants perfect for summer",
             "linen,palazzo,summer,comfortable,ethnic,breathable", "", "summer",
             "https://example.com/palazzo.jpg", True, 4.3),
            
            ("Anarkali Suit Set", "fashion", "ethnic", 2499, "Royal Threads", 
             "Georgette anarkali suit with dupatta",
             "anarkali,georgette,suit,dupatta,ethnic,party", "", "all-seasons",
             "https://example.com/anarkali.jpg", True, 4.4),
            
            ("Dhoti Kurta Set", "fashion", "ethnic", 1899, "Traditional Men", 
             "Cotton dhoti kurta set for festivals",
             "dhoti,kurta,cotton,traditional,festival,men", "", "all-seasons",
             "https://example.com/dhoti-kurta.jpg", True, 4.2),
            
            # Casual Wear
            ("Oversized Cotton Tee", "fashion", "casual", 799, "UrbanStyle",
             "Premium cotton oversized t-shirt in trending colors",
             "casual,cotton,trendy,comfortable,tee,oversized", "", "all-seasons",
             "https://example.com/tee.jpg", True, 4.1),
            
            ("Denim Jeans - Skinny", "fashion", "casual", 1699, "Denim Craft", 
             "Stretchable skinny jeans with perfect fit",
             "jeans,denim,skinny,stretchable,casual,comfort", "", "all-seasons",
             "https://example.com/jeans.jpg", True, 4.3),
            
            ("Hoodie - Graphic Print", "fashion", "casual", 1299, "Street Style", 
             "Comfortable hoodie with trendy graphic print",
             "hoodie,graphic,print,comfortable,casual,winter", "", "winter,monsoon",
             "https://example.com/hoodie.jpg", True, 4.2),
            
            ("Cargo Pants", "fashion", "casual", 1599, "Utility Wear", 
             "Multi-pocket cargo pants for casual outings",
             "cargo,pants,pockets,utility,casual,comfortable", "", "all-seasons",
             "https://example.com/cargo.jpg", True, 4.0),
            
            ("Polo T-Shirt", "fashion", "casual", 899, "Classic Fit", 
             "Cotton polo t-shirt with collar",
             "polo,tshirt,collar,cotton,classic,casual", "", "all-seasons",
             "https://example.com/polo.jpg", True, 4.1),
            
            # Formal Wear
            ("Formal Shirt - White", "fashion", "formal", 1299, "Office Pro", 
             "Crisp white formal shirt for office wear",
             "formal,shirt,white,office,professional,cotton", "", "all-seasons",
             "https://example.com/formal-shirt.jpg", True, 4.3),
            
            ("Blazer - Navy Blue", "fashion", "formal", 3499, "Suit Up", 
             "Tailored navy blue blazer for business meetings",
             "blazer,navy,blue,formal,business,tailored", "", "all-seasons",
             "https://example.com/blazer.jpg", True, 4.5),
            
            ("Formal Trousers", "fashion", "formal", 1799, "Perfect Fit", 
             "Wrinkle-free formal trousers with perfect drape",
             "trousers,formal,wrinkle-free,office,professional", "", "all-seasons",
             "https://example.com/trousers.jpg", True, 4.2),
            
            ("Formal Dress - Black", "fashion", "formal", 2299, "Executive Style", 
             "Elegant black formal dress for corporate events",
             "dress,formal,black,elegant,corporate,women", "", "all-seasons",
             "https://example.com/formal-dress.jpg", True, 4.4),
            
            ("Leather Shoes - Oxford", "fashion", "formal", 2999, "Shoe Craft", 
             "Genuine leather Oxford shoes for formal occasions",
             "shoes,leather,oxford,formal,genuine,professional", "", "all-seasons",
             "https://example.com/oxford-shoes.jpg", True, 4.6),
            
            # Seasonal & Specialty Items
            ("Winter Jacket", "fashion", "casual", 2499, "Warm Wear", 
             "Insulated winter jacket with hood",
             "jacket,winter,insulated,hood,warm,casual", "", "winter",
             "https://example.com/winter-jacket.jpg", True, 4.3),
            
            ("Raincoat - Waterproof", "fashion", "casual", 899, "Monsoon Gear", 
             "Lightweight waterproof raincoat",
             "raincoat,waterproof,monsoon,lightweight,protection", "", "monsoon",
             "https://example.com/raincoat.jpg", True, 4.1),
            
            ("Summer Dress - Floral", "fashion", "casual", 1199, "Breezy Style", 
             "Light floral summer dress in cotton",
             "dress,summer,floral,cotton,light,breezy", "", "summer",
             "https://example.com/summer-dress.jpg", True, 4.2),
            
            ("Woolen Scarf", "fashion", "casual", 699, "Cozy Knits", 
             "Soft woolen scarf for winter warmth",
             "scarf,woolen,winter,soft,warm,cozy", "", "winter",
             "https://example.com/scarf.jpg", True, 4.0),
            
            ("Sandals - Leather", "fashion", "casual", 1499, "Comfort Walk", 
             "Genuine leather sandals for summer",
             "sandals,leather,summer,comfort,casual,genuine", "", "summer",
             "https://example.com/sandals.jpg", True, 4.2),
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, category, subcategory, price, brand, 
                                description, tags, dietary_info, seasonal_relevance, 
                                image_url, availability, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_products)
        
        conn.commit()
        conn.close()
    
    def get_products(self, category: Optional[str] = None, 
                    max_price: Optional[float] = None,
                    tags: Optional[List[str]] = None) -> List[Dict]:
        """Retrieve products based on filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM products WHERE availability = 1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if max_price:
            query += " AND price <= ?"
            params.append(max_price)
        
        if tags:
            for tag in tags:
                query += " AND tags LIKE ?"
                params.append(f"%{tag}%")
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        products = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return products
    
    def log_recommendation(self, user_query: str, user_preferences: Dict,
                          recommended_products: List[Dict], confidence_scores: List[float]):
        """Log recommendation for analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recommendations_log (user_query, user_preferences, 
                                           recommended_products, confidence_scores)
            VALUES (?, ?, ?, ?)
        ''', (user_query, json.dumps(user_preferences), 
              json.dumps(recommended_products), json.dumps(confidence_scores)))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user preferences by user_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_preferences WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            columns = [description[0] for description in cursor.description]
            prefs = dict(zip(columns, result))
            conn.close()
            return prefs
        
        conn.close()
        return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict):
        """Update or insert user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        existing = self.get_user_preferences(user_id)
        
        if existing:
            cursor.execute('''
                UPDATE user_preferences 
                SET dietary_preferences = ?, style_preferences = ?, 
                    budget_range = ?, preferred_brands = ?, size_info = ?,
                    interaction_history = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (
                json.dumps(preferences.get('dietary_preferences', [])),
                json.dumps(preferences.get('style_preferences', [])),
                preferences.get('budget_range', ''),
                json.dumps(preferences.get('preferred_brands', [])),
                json.dumps(preferences.get('size_info', {})),
                json.dumps(preferences.get('interaction_history', [])),
                user_id
            ))
        else:
            cursor.execute('''
                INSERT INTO user_preferences (user_id, dietary_preferences, 
                                            style_preferences, budget_range, 
                                            preferred_brands, size_info, 
                                            interaction_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                json.dumps(preferences.get('dietary_preferences', [])),
                json.dumps(preferences.get('style_preferences', [])),
                preferences.get('budget_range', ''),
                json.dumps(preferences.get('preferred_brands', [])),
                json.dumps(preferences.get('size_info', {})),
                json.dumps(preferences.get('interaction_history', []))
            ))
        
        conn.commit()
        conn.close()
