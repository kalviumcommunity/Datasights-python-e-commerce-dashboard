import os
import random
import datetime
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_data():
    print("Generating e-commerce marketplace analytics mock data...")
    
    # 1. Define Sellers and Categories
    seller_categories = {
        # Electronics
        "Apex Electronics": "Electronics",
        "TechZone": "Electronics",
        "GadgetGuru": "Electronics",
        "ElectroStore": "Electronics",
        "SmartTech": "Electronics",
        "CircuitWorld": "Electronics",
        "FutureGadgets": "Electronics",
        "ByteSize": "Electronics",
        "VoltEdge": "Electronics",
        "SiliconValley": "Electronics",
        # Apparel
        "Vogue Apparel": "Apparel",
        "TrendFashion Co": "Apparel",
        "StyleVibe": "Apparel",
        "ClassicThread": "Apparel",
        "UrbanOutwear": "Apparel",
        "DrapeStyle": "Apparel",
        "SilkRoad": "Apparel",
        "VelvetLoom": "Apparel",
        "DenimCo": "Apparel",
        "ChicBoutique": "Apparel",
        # Home & Kitchen
        "DecoSpace": "Home & Kitchen",
        "KitchenPro": "Home & Kitchen",
        "ComfyHome": "Home & Kitchen",
        "SmartLiving": "Home & Kitchen",
        "CookMaster": "Home & Kitchen",
        "Cozydwell": "Home & Kitchen",
        "WoodCraft": "Home & Kitchen",
        "UrbanNest": "Home & Kitchen",
        "TableWare": "Home & Kitchen",
        "LuxeDecor": "Home & Kitchen",
        # Grocery
        "DailyGrocery": "Grocery",
        "FreshCart": "Grocery",
        "OrganicBite": "Grocery",
        "PantryStop": "Grocery",
        "GreenGrocer": "Grocery",
        "SuperFoods": "Grocery",
        "NatureChoice": "Grocery",
        "FarmFresh": "Grocery",
        "QuickStore": "Grocery",
        "ValueMart": "Grocery",
        # Beauty
        "GlowCosmetics": "Beauty",
        "AuraBeauty": "Beauty",
        "SkinCare Co": "Beauty",
        "LuxeScent": "Beauty",
        "PureRadiance": "Beauty",
        "FloraEssence": "Beauty",
        "GlamourSpade": "Beauty",
        "HerbalTouch": "Beauty",
        "SilkSkin": "Beauty",
        "VelvetTouch": "Beauty"
    }
    
    sellers = list(seller_categories.keys())
    
    # average item prices by category
    category_prices = {
        "Electronics": 150.0,
        "Apparel": 45.0,
        "Home & Kitchen": 65.0,
        "Grocery": 20.0,
        "Beauty": 35.0
    }
    
    # 2. Date Range: 52 weeks (1 year)
    start_date = datetime.date(2025, 7, 1)
    weeks = [start_date + datetime.timedelta(weeks=w) for w in range(52)]
    
    # Review text collections for sentiment mapping
    positive_comments = {
        "Electronics": ["Excellent phone, battery lasts 2 days!", "Very fast processor and crystal clear screen.", "Highly recommend this gadget, works flawlessly.", "Amazing sound quality, best headphones ever.", "Solid build and easy set up."],
        "Apparel": ["Very soft material, fits perfectly!", "Absolutely love the color, exactly as pictured.", "Great style and comfortable to wear all day.", "Excellent quality jeans, very durable.", "Perfect fit, fast delivery!"],
        "Home & Kitchen": ["Extremely sharp knives, cooks like a chef.", "Very cozy bedsheets, very soft fabric.", "Blender is super powerful, handles frozen fruit easily.", "Beautiful design, fits perfectly on my counter.", "Highly durable pan, non-stick works perfectly."],
        "Grocery": ["Super fresh organic apples, delicious!", "Excellent quality olive oil, great flavor.", "Very fast shipping, eggs arrived undamaged and fresh.", "Highly recommend these snacks, kids love them.", "Great coffee beans, wonderful aroma."],
        "Beauty": ["Excellent moisturizer, skin feels amazing.", "Smells wonderful and lasts all day.", "Perfect shade of lipstick, not drying.", "Very high quality serum, seen improvements in a week.", "Soft brushes, applies makeup smoothly."]
    }
    
    neutral_comments = [
        "Product is okay, nothing special.", "Average quality for the price.", "Took a bit long to ship, but works fine.", "Decent item, fits reasonably well.", "It does what it says, but feels a bit lightweight."
    ]
    
    negative_comments_by_reason = {
        "late_shipment": [
            "Took weeks to arrive. Arrived way past delivery window.",
            "Shipping was extremely delayed. No update from seller.",
            "Took forever to ship. Needed it for a birthday, arrived too late.",
            "Delivery kept getting pushed back. Frustrating experience.",
            "Worst delivery speed ever. Almost a month to ship out."
        ],
        "cancellation": [
            "Seller cancelled my order with no explanation. Very unprofessional.",
            "Order cancelled after 5 days of waiting. Stock issue?",
            "Extremely disappointed, seller cancelled order. Out of stock.",
            "They took my money, waited a week, then cancelled the order.",
            "Terrible customer service. Order was randomly cancelled by seller."
        ],
        "bad_quality": [
            "Cheap material, tore on the very first day. Waste of money.",
            "Poor quality product. Broke within five minutes of use.",
            "Looks cheap and plasticky, completely different from pictures.",
            "Very fragile. Fell apart immediately.",
            "Do not buy. Very poor construction and cheap build."
        ],
        "defective": [
            "Arrived damaged and scratched. Packaging was terrible.",
            "Defective unit. Will not turn on. Returning immediately.",
            "Broke after 2 days. The charging port doesn't work.",
            "Item doesn't work at all. Completely dead on arrival.",
            "Damaged in transit, fluid was leaking everywhere."
        ],
        "counterfeit": [
            "Warning: Fake counterfeit item. Not original brand!",
            "This is a scam. Counterfeit copy, serial number is invalid.",
            "Not original as advertised. Avoid this seller.",
            "Cheap copy of the branded product. Fake!",
            "Clearly a fake product. Scammed."
        ],
        "spoiled": [
            "Arrived rotten and spoiled. Smelled terrible.",
            "Fruits were completely molded. Unusable.",
            "Item expired 3 months ago! Unsafe.",
            "Warm and melted. Bad cooling during shipment.",
            "Vegetables were mushy and rotten. Bad quality."
        ]
    }
    
    # 3. Create datasets
    weekly_metrics = []
    reviews_data = []
    
    review_id_counter = 1
    
    for seller in sellers:
        category = seller_categories[seller]
        avg_price = category_prices[category]
        
        # Determine seller archetype (baked-in behaviors)
        # Type A: 'TechZone' -> Counterfeit Electronics scammer starting week 30
        # Type B: 'TrendFashion Co' -> Consistently bad sizing/quality Apparel
        # Type C: 'KitchenPro' -> Logistics failure (Late shipping/cancellations) starting week 15 (Dropshipper)
        # Type D: 'DailyGrocery' -> Fresh food logistics failure (Late shipping/rotten products) starting week 40
        # Type E: All other sellers are baseline healthy
        
        for w_idx, week in enumerate(weeks):
            # Base sales volume
            base_sales = random.randint(100, 300)
            
            # Default healthy behaviors
            lsr = np.random.uniform(0.005, 0.02)  # 0.5% - 2%
            scr = np.random.uniform(0.001, 0.005) # 0.1% - 0.5%
            sfrr = np.random.uniform(0.005, 0.015) # 0.5% - 1.5%
            nrr = np.random.uniform(0.02, 0.05)   # 2% - 5%
            avg_rating = np.random.uniform(4.3, 4.8)
            
            # Apply seller archetype deviations
            if seller == "TechZone":
                if w_idx >= 30:
                    # Counterfeit electronics start
                    sfrr = np.random.uniform(0.12, 0.18) # 12% - 18% returns
                    nrr = np.random.uniform(0.25, 0.35)  # 25% - 35% negative reviews
                    avg_rating = np.random.uniform(1.8, 2.4)
                    base_sales = int(base_sales * 1.5) # Sales boost initially due to fake listing prices
                else:
                    avg_rating = np.random.uniform(4.4, 4.7)
            
            elif seller == "TrendFashion Co":
                # Consistently low quality apparel (sizing and material issues)
                sfrr = np.random.uniform(0.10, 0.15) # 10% - 15% returns
                nrr = np.random.uniform(0.15, 0.25)  # 15% - 25% negative reviews
                avg_rating = np.random.uniform(3.1, 3.5)
                
            elif seller == "KitchenPro":
                if w_idx >= 15:
                    # Dropshipping issues, high shipping delays & cancellations
                    lsr = np.random.uniform(0.18, 0.28) # 18% - 28% late
                    scr = np.random.uniform(0.08, 0.14) # 8% - 14% cancelled
                    nrr = np.random.uniform(0.12, 0.20) # 12% - 20% negative
                    avg_rating = np.random.uniform(2.6, 3.2)
                    base_sales = int(base_sales * 0.8) # Sales drop due to poor experience
                else:
                    avg_rating = np.random.uniform(4.2, 4.6)
                    
            elif seller == "DailyGrocery":
                if w_idx >= 40:
                    # Cold chain logistics failure (Late + rotten grocery)
                    lsr = np.random.uniform(0.25, 0.38) # 25% - 38% late
                    sfrr = np.random.uniform(0.08, 0.14) # 8% - 14% returned (spoiled)
                    nrr = np.random.uniform(0.20, 0.30) # 20% - 30% negative
                    avg_rating = np.random.uniform(2.0, 2.7)
                else:
                    avg_rating = np.random.uniform(4.3, 4.7)
            
            # Calculate revenue
            revenue = round(base_sales * avg_price, 2)
            
            # Calculate composite Trust Score (0 - 100)
            # Subtract penalties from 100
            # LSR Penalty: LSR * 150 (up to max 25)
            # SCR Penalty: SCR * 250 (up to max 30)
            # SFRR Penalty: SFRR * 200 (up to max 30)
            # NRR Penalty: NRR * 150 (up to max 25)
            lsr_penalty = min(25, lsr * 150)
            scr_penalty = min(30, scr * 250)
            sfrr_penalty = min(30, sfrr * 200)
            nrr_penalty = min(25, nrr * 150)
            
            trust_score = 100.0 - (lsr_penalty + scr_penalty + sfrr_penalty + nrr_penalty)
            # Add a tiny bit of random noise to trust score to make it look organic
            trust_score += np.random.uniform(-1.0, 1.0)
            trust_score = max(0.0, min(100.0, round(trust_score, 1)))
            
            # Average review sentiment score
            # High rating (4-5) -> positive sentiment (0.3 to 0.8)
            # Mid rating (3) -> neutral sentiment (-0.1 to 0.2)
            # Low rating (1-2) -> negative sentiment (-0.8 to -0.3)
            if avg_rating >= 4.0:
                avg_sentiment = np.random.uniform(0.4, 0.8)
            elif avg_rating >= 3.0:
                avg_sentiment = np.random.uniform(0.0, 0.3)
            else:
                avg_sentiment = np.random.uniform(-0.7, -0.2)
                
            weekly_metrics.append({
                "seller_id": seller,
                "category": category,
                "week_start": week.strftime("%Y-%m-%d"),
                "sales_volume": base_sales,
                "revenue": revenue,
                "late_shipment_rate": round(lsr, 4),
                "seller_cancellation_rate": round(scr, 4),
                "seller_fault_return_rate": round(sfrr, 4),
                "negative_review_rate": round(nrr, 4),
                "avg_review_rating": round(avg_rating, 2),
                "avg_sentiment_score": round(avg_sentiment, 2),
                "trust_score": trust_score
            })
            
            # Generate sample raw reviews for review search / deep-dive
            # Let's generate ~3 reviews per week per seller to populate reviews table
            for _ in range(3):
                # Choose rating based on the week's average rating
                rating = int(np.clip(round(np.random.normal(avg_rating, 0.7)), 1, 5))
                
                # Assign sentiment and review text based on rating and archetype
                sentiment = 0.0
                review_text = ""
                
                if rating >= 4:
                    sentiment = np.random.uniform(0.3, 0.9)
                    review_text = random.choice(positive_comments[category])
                elif rating == 3:
                    sentiment = np.random.uniform(-0.1, 0.3)
                    review_text = random.choice(neutral_comments)
                else:
                    sentiment = np.random.uniform(-0.9, -0.2)
                    # Pick negative review reason depending on the active issue
                    reasons = ["bad_quality"]
                    if category == "Grocery" and seller == "DailyGrocery" and w_idx >= 40:
                        reasons = ["late_shipment", "spoiled", "defective"]
                    elif seller == "TechZone" and w_idx >= 30:
                        reasons = ["counterfeit", "defective"]
                    elif seller == "KitchenPro" and w_idx >= 15:
                        reasons = ["late_shipment", "cancellation"]
                    elif seller == "TrendFashion Co":
                        reasons = ["bad_quality"]
                    else:
                        reasons = ["bad_quality", "defective", "late_shipment"]
                    
                    reason = random.choice(reasons)
                    review_text = random.choice(negative_comments_by_reason[reason])
                
                reviews_data.append({
                    "review_id": f"REV{review_id_counter:05d}",
                    "seller_id": seller,
                    "category": category,
                    "review_date": (week + datetime.timedelta(days=random.randint(1, 6))).strftime("%Y-%m-%d"),
                    "rating": rating,
                    "review_text": review_text,
                    "sentiment_score": round(sentiment, 2),
                    "sentiment_category": "Positive" if rating >= 4 else ("Neutral" if rating == 3 else "Negative")
                })
                review_id_counter += 1

    # 4. Save to files
    os.makedirs("data/processed", exist_ok=True)
    
    df_metrics = pd.DataFrame(weekly_metrics)
    df_metrics.to_csv("data/processed/seller_weekly_metrics.csv", index=False)
    
    df_reviews = pd.DataFrame(reviews_data)
    df_reviews.to_csv("data/processed/customer_reviews_sample.csv", index=False)
    
    print(f"Data generation complete! Saved files to:")
    print(f"  - data/processed/seller_weekly_metrics.csv ({len(df_metrics)} rows)")
    print(f"  - data/processed/customer_reviews_sample.csv ({len(df_reviews)} rows)")

if __name__ == "__main__":
    generate_data()
