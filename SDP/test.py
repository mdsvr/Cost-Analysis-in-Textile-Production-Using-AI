import pandas as pd
import numpy as np
import random
from faker import Faker

# Initialize Faker for realistic brand names
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define fabric types and their product categories
fabric_categories = {
    'cotton': ['Formal Shirt', 'T-shirt', 'Pants', 'Saree', 'Dhoti', 'Kurta', 'Shorts', 'Salwar Suit', 'Dress', 'Blouse'],
    'silk': ['Saree', 'Dhoti', 'Lehenga', 'Sherwani', 'Blouse', 'Dupatta', 'Kurta', 'Scarf'],
    'wool': ['Sweater', 'Coat', 'Scarf', 'Shawl', 'Cardigan', 'Gloves', 'Hat', 'Socks'],
    'linen': ['Kurta', 'Dress', 'Shirt', 'Pants', 'Skirt', 'Blouse', 'Jacket'],
    'leather': ['Jacket', 'Pants', 'Skirt', 'Vest', 'Gloves', 'Bag'],
    'denim': ['Jeans', 'Jacket', 'Shirt', 'Skirt', 'Shorts', 'Overall'],
    'fleece': ['Jacket', 'Hoodie', 'Sweatshirt', 'Pants', 'Blanket', 'Scarf']
}

# Brand tiers with realistic multipliers
brand_tiers = {
    'budget': {'cost_multiplier': 1.0, 'margin_multiplier': 1.0, 'brand_value_multiplier': 1.0},
    'mid_range': {'cost_multiplier': 1.5, 'margin_multiplier': 1.8, 'brand_value_multiplier': 2.5},
    'premium': {'cost_multiplier': 2.5, 'margin_multiplier': 3.0, 'brand_value_multiplier': 5.0},
    'luxury': {'cost_multiplier': 5.0, 'margin_multiplier': 6.0, 'brand_value_multiplier': 10.0}
}

# Base costs by fabric type (per meter/unit)
base_fabric_costs = {
    'cotton': 200,
    'silk': 500,
    'wool': 400,
    'linen': 300,
    'leather': 1000,
    'denim': 250,
    'fleece': 150
}

# Product complexity factors (affects manufacturing cost)
product_complexity = {
    'Shirt': 1.0,
    'T-shirt': 0.8,
    'Pants': 1.2,
    'Saree': 1.5,
    'Dhoti': 0.7,
    'Kurta': 1.3,
    'Shorts': 0.9,
    'Salwar Suit': 1.8,
    'Dress': 1.4,
    'Blouse': 1.1,
    'Lehenga': 2.0,
    'Sherwani': 2.2,
    'Dupatta': 0.6,
    'Scarf': 0.5,
    'Sweater': 1.6,
    'Coat': 2.5,
    'Shawl': 1.0,
    'Cardigan': 1.7,
    'Gloves': 0.8,
    'Hat': 0.7,
    'Socks': 0.4,
    'Skirt': 1.1,
    'Jacket': 2.0,
    'Vest': 1.0,
    'Bag': 1.5,
    'Jeans': 1.3,
    'Overall': 1.9,
    'Hoodie': 1.2,
    'Sweatshirt': 1.1,
    'Blanket': 1.0
}

def generate_brand_name(tier):
    """Generate realistic brand names based on tier"""
    if tier == 'luxury':
        return f"{fake.last_name()} Couture"
    elif tier == 'premium':
        return f"{fake.last_name()} & Co."
    elif tier == 'mid_range':
        return f"{fake.company()}"
    else:
        return f"{fake.company()} Basics"

def calculate_costs(product_type, fabric, brand_tier):
    """Calculate all cost components for a product"""
    # Base fabric cost adjusted for product type
    base_cost = base_fabric_costs[fabric] * product_complexity.get(product_type, 1.0)
    
    # Apply brand tier multipliers
    tier = brand_tiers[brand_tier]
    fabric_cost = base_cost * tier['cost_multiplier'] * random.uniform(0.9, 1.1)
    
    # Manufacturing cost (60-80% of fabric cost)
    manufacturing_cost = fabric_cost * random.uniform(0.6, 0.8) * product_complexity.get(product_type, 1.0)
    
    # Transportation (8-12% of fabric cost)
    transportation_cost = fabric_cost * random.uniform(0.08, 0.12)
    
    # Tax (10-15% of fabric + manufacturing)
    tax = (fabric_cost + manufacturing_cost) * random.uniform(0.10, 0.15)
    
    # Brand value (40-60% of fabric cost, multiplied by tier)
    brand_value = fabric_cost * random.uniform(0.4, 0.6) * tier['brand_value_multiplier']
    
    # Retailer margin (70-100% of total cost, multiplied by tier)
    total_cost = fabric_cost + manufacturing_cost + transportation_cost + tax + brand_value
    retailer_margin = total_cost * random.uniform(0.7, 1.0) * tier['margin_multiplier']
    
    # Selling price (total cost + retailer margin)
    selling_price = total_cost + retailer_margin
    
    return {
        'fabric_raw_cost': round(fabric_cost, 2),
        'manufacturing_and_labour': round(manufacturing_cost, 2),
        'transportation': round(transportation_cost, 2),
        'tax': round(tax, 2),
        'brand_value': round(brand_value, 2),
        'retailer_margin': round(retailer_margin, 2),
        'selling_price': round(selling_price, 2)
    }

def generate_dataset(num_entries_per_category=100):
    """Generate the complete dataset"""
    records = []
    
    for fabric, categories in fabric_categories.items():
        for category in categories:
            for _ in range(num_entries_per_category):
                # Randomly select brand tier with weighted probability
                tier = random.choices(
                    list(brand_tiers.keys()),
                    weights=[0.4, 0.3, 0.2, 0.1]  # More budget brands, fewer luxury
                )[0]
                
                brand_name = generate_brand_name(tier)
                
                # Generate product details
                product_name = f"{category}"
                if random.random() > 0.7:  # 30% chance to add style descriptor
                    styles = ['Classic', 'Modern', 'Traditional', 'Contemporary', 'Vintage', 'Casual', 'Formal']
                    product_name = f"{random.choice(styles)} {product_name}"
                
                # Calculate costs
                costs = calculate_costs(category, fabric, tier)
                
                # Create record
                record = {
                    'Product_type': product_name,
                    'Brand': f"{brand_name} ({tier})",
                    'fabric': fabric,
                    **costs
                }
                
                records.append(record)
    
    return pd.DataFrame(records)

# Generate the dataset
df = generate_dataset(num_entries_per_category=3000)  # 1200 entries per category

# Save to Excel
df.to_excel('textile_production_cost_dataset.xlsx', index=False)
df.to_csv('textile_production_cost_dataset.csv', index=False)

print(f"Dataset generated with {len(df)} entries.")
print("Files saved as:")
print("- textile_production_cost_dataset.xlsx")
print("- textile_production_cost_dataset.csv")