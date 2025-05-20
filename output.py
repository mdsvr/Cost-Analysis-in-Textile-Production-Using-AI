import joblib
import numpy as np
import matplotlib.pyplot as plt

# Valid fabric to product mapping from dataset generator
fabric_categories = {
    'cotton': ['Formal Shirt', 'T-shirt', 'Pants', 'Saree', 'Dhoti', 'Kurta', 'Shorts', 'Salwar Suit', 'Dress', 'Blouse'],
    'silk': ['Saree', 'Dhoti', 'Lehenga', 'Sherwani', 'Blouse', 'Dupatta', 'Kurta', 'Scarf'],
    'wool': ['Sweater', 'Coat', 'Scarf', 'Shawl', 'Cardigan', 'Gloves', 'Hat', 'Socks'],
    'linen': ['Kurta', 'Dress', 'Shirt', 'Pants', 'Skirt', 'Blouse', 'Jacket'],
    'leather': ['Jacket', 'Pants', 'Skirt', 'Vest', 'Gloves', 'Bag'],
    'denim': ['Jeans', 'Jacket', 'Shirt', 'Skirt', 'Shorts', 'Overall'],
    'fleece': ['Jacket', 'Hoodie', 'Sweatshirt', 'Pants', 'Blanket', 'Scarf']
}

def main():
    print("\U0001F50D ML-Based Textile Cost Estimator")

    # === Load models and encoders ===
    artifacts = joblib.load("xgb_rf_ga_models.pkl")
    clf = artifacts['classifier']
    cost_model = artifacts['multi_regressor']
    encoders = artifacts['encoders']

    # === User input ===
    fabric_options = list(fabric_categories.keys())
    fabric = input(f"Enter fabric type {fabric_options}: ").strip().lower()
    if fabric not in fabric_categories:
        print(f" Invalid fabric type. Choose from: {fabric_options}")
        return

    product_options = fabric_categories[fabric]
    print(f"Available product types for {fabric}: {product_options}")
    product = input("Enter product type: ").strip().title()
    if product not in product_options:
        print(f" Invalid product type for {fabric}. Choose from: {product_options}")
        return

    size = input("Enter size (S, M, L, XL, XXL, XXXL): ").strip().upper()
    brand_tier = input("Enter brand tier (budget, mid_range, premium, luxury): ").strip().lower()

    try:
        selling_price = float(input("Enter selling price (in ₹): ").strip())
        if selling_price <= 0:
            raise ValueError("Price must be positive.")
    except ValueError as e:
        print(f" Invalid price input: {e}")
        return

    try:
        fabric_enc = encoders['fabric'].transform([fabric])[0]
        product_enc = encoders['product_category'].transform([product])[0]
        size_enc = encoders['Size'].transform([size])[0]
        brand_enc = encoders['brand_tier'].transform([brand_tier])[0]
    except ValueError as e:
        print(f" Invalid input: {e}")
        return

    input_array = np.array([[fabric_enc, brand_enc, product_enc, size_enc]])

    # === Classification Prediction ===
    pred_class = clf.predict(input_array)[0]
    if hasattr(clf, "predict_proba"):
        prob = clf.predict_proba(input_array)[0]
        confidence = round(prob[pred_class] * 100, 2)
    else:
        confidence = "N/A"

    category = "High Price" if pred_class == 1 else "Low Price"

    # === Predict cost breakdown ===
    raw_breakdown = cost_model.predict(input_array)[0]
    raw_breakdown = np.clip(raw_breakdown, 0, None)
    raw_total = sum(raw_breakdown)

    scaling_factor = selling_price / raw_total if raw_total > 0 else 1.0
    scaled_breakdown = [max(0, x * scaling_factor) for x in raw_breakdown]

    labels = ['Fabric Cost', 'Manufacturing', 'Transportation', 'Brand Value', 'Retailer Margin', 'Tax']
    cost_dict = dict(zip(labels, scaled_breakdown))
    total_cost = sum(scaled_breakdown)
    discrepancy = abs(total_cost - selling_price)

    # === Output ===
    print("Prediction Result:")
    print(f"Predicted Price Category: {category}")
    print(f"Confidence: {confidence}%")

    print(f" Entered Selling Price: ₹{round(selling_price, 2)}")
    print(" Cost Breakdown (ML-predicted, scaled):")
    for label, value in cost_dict.items():
        print(f"   {label}: ₹{round(value, 2)}")

    print(f"\n Total (from breakdown): ₹{round(total_cost, 2)}")
    print(f" Difference from input price: ₹{round(discrepancy, 2)}")

    # === Pie Chart ===
    if total_cost > 0:
        plt.figure(figsize=(8, 6))
        plt.pie(scaled_breakdown, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(" Cost Contribution Breakdown", fontsize=14)
        plt.tight_layout()
        plt.show()
    else:
        print("\n Cannot plot pie chart because the breakdown values are all zero.")

if __name__ == "__main__":
    main()
