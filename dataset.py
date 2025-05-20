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

# Brand tiers with cost multipliers
brand_tiers = {
    'budget': {'cost_multiplier': 1.0, 'margin_multiplier': 1.0, 'brand_value_multiplier': 1.0},
    'mid_range': {'cost_multiplier': 1.5, 'margin_multiplier': 1.8, 'brand_value_multiplier': 2.5},
    'premium': {'cost_multiplier': 3.5, 'margin_multiplier': 2.5, 'brand_value_multiplier': 3.0},
    'luxury': {'cost_multiplier': 6.0, 'margin_multiplier': 4.0, 'brand_value_multiplier': 7.0}
}

# Fabric base cost ranges per kg (INR)
base_fabric_cost_ranges = {
    'cotton': {'budget': (140, 250), 'mid_range': (300, 550), 'premium': (600, 900), 'luxury': (1000, 1800)},
    'silk': {'budget': (2000, 3500), 'mid_range': (4000, 6000), 'premium': (8000, 15000), 'luxury': (16000, 100000)},
    'wool': {'budget': (500, 1200), 'mid_range': (1500, 4000), 'premium': (5000, 10000), 'luxury': (14000, 100000)},
    'linen': {'budget': (300, 800), 'mid_range': (1000, 2000), 'premium': (2500, 5000), 'luxury': (6000, 25000)},
    'leather': {'budget': (800, 3000), 'mid_range': (4000, 8000), 'premium': (9000, 25000), 'luxury': (26000, 150000)},
    'denim': {'budget': (100, 200), 'mid_range': (250, 500), 'premium': (700, 1500), 'luxury': (2000, 6000)},
    'fleece': {'budget': (150, 350), 'mid_range': (400, 800), 'premium': (900, 2500), 'luxury': (3000, 8000)}
}

# Product complexity factors
product_complexity = {
    'Shirt': 1.0, 'T-shirt': 0.8, 'Pants': 1.2, 'Saree': 1.5, 'Dhoti': 0.7,
    'Kurta': 1.3, 'Shorts': 0.9, 'Salwar Suit': 1.8, 'Dress': 1.4, 'Blouse': 1.1,
    'Lehenga': 2.0, 'Sherwani': 2.2, 'Dupatta': 0.6, 'Scarf': 0.5, 'Sweater': 1.6,
    'Coat': 2.5, 'Shawl': 1.0, 'Cardigan': 1.7, 'Gloves': 0.8, 'Hat': 0.7, 'Socks': 0.4,
    'Skirt': 1.1, 'Jacket': 2.0, 'Vest': 1.0, 'Bag': 1.5, 'Jeans': 1.3, 'Overall': 1.9,
    'Hoodie': 1.2, 'Sweatshirt': 1.1, 'Blanket': 1.0
}

# Size multipliers
size_multipliers = {
    'S': 0.8, 'M': 1.0, 'L': 1.2, 'XL': 1.4, 'XXL': 1.7, 'XXXL': 2.0
}

def generate_brand_name(tier):
    if tier == 'luxury':
        return f"{fake.last_name()} Couture"
    elif tier == 'premium':
        return f"{fake.last_name()} & Co."
    elif tier == 'mid_range':
        return f"{fake.company()}"
    else:
        return f"{fake.company()} Basics"

def get_fabric_cost_per_kg(fabric, brand_tier):
    min_val, max_val = base_fabric_cost_ranges[fabric][brand_tier]
    return random.randint(min_val, max_val)

def calculate_gst(fabric, selling_price):
    synthetic_fabrics = {'fleece', 'polyester', 'nylon', 'acrylic'}
    if fabric in synthetic_fabrics:    
        return selling_price * 0.18
    elif selling_price < 1000:
        return selling_price * 0.05
    else:
        return selling_price * 0.12

def calculate_costs(product_type, fabric, brand_tier, size):
    cost_per_kg = get_fabric_cost_per_kg(fabric, brand_tier)
    tier = brand_tiers[brand_tier]

    random_variance = random.uniform(0.9, 1.1)
    size_factor = size_multipliers.get(size, 1.0)
    product_factor = product_complexity.get(product_type, 1.0)
    tier_multiplier = tier['cost_multiplier']

    fabric_cost = (cost_per_kg/3) * tier_multiplier * product_factor * size_factor * random_variance
    manufacturing_cost = fabric_cost * random.uniform(0.5, 0.7) * product_factor * random.uniform(1.0, 1.05)  # spoilage factor
    transportation_cost = fabric_cost * random.uniform(0.05, 0.08)
    brand_value = fabric_cost * random.uniform(0.3, 0.5) * tier['brand_value_multiplier']

    total_cost = fabric_cost + manufacturing_cost + transportation_cost + brand_value
    retailer_margin = total_cost * random.uniform(0.5, 0.7) * tier['margin_multiplier']
    selling_price = total_cost + retailer_margin
    tax = calculate_gst(fabric, selling_price)

    return {
        'fabric_cost_per_kg/meter/hide': cost_per_kg,
        'fabric_raw_cost': round(fabric_cost, 2),
        'manufacturing': round(manufacturing_cost, 2),
        'transportation': round(transportation_cost, 2),
        'tax': round(tax, 2),
        'brand_value': round(brand_value, 2),
        'retailer_margin': round(retailer_margin, 2),
        'selling_price': round(selling_price + tax, 2)
    }

def generate_dataset(num_entries_per_category=200):
    records = []
    for fabric, categories in fabric_categories.items():
        for category in categories:
            for _ in range(num_entries_per_category):
                tier = random.choices(list(brand_tiers.keys()), weights=[0.4, 0.3, 0.2, 0.1])[0]
                size = random.choice(list(size_multipliers.keys()))
                brand_name = generate_brand_name(tier)
                product_name = category
                if random.random() > 0.7:
                    styles = ['Classic', 'Modern', 'Traditional', 'Contemporary', 'Vintage', 'Casual', 'Formal']
                    product_name = f"{random.choice(styles)} {product_name}"
                costs = calculate_costs(category, fabric, tier, size)

                records.append({
                    'Product_type': product_name,
                    'Brand': f"{brand_name} ({tier})",
                    'Size': size,
                    'fabric': fabric,
                    **costs
                })
    return pd.DataFrame(records)

# Generate and save the dataset
df = generate_dataset(num_entries_per_category=3000)
df.to_excel('textile_production_dataset.xlsx', index=False)
df.to_csv('textile_production_dataset.csv', index=False)