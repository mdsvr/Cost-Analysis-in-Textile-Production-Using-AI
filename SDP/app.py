import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

class FashionCostPredictor:
    def __init__(self, model_path='textile_predictor_fixed.pkl'):
        artifacts = joblib.load(model_path)
        self.model = artifacts['model']
        self.scaler = artifacts['scaler']  # Now properly loaded
        self.fabric_types = artifacts['fabric_types']
        self.brand_tiers = artifacts['brand_tiers']
        
        # Initialize encoders
        self.fabric_encoder = LabelEncoder().fit(self.fabric_types)
        self.brand_encoder = LabelEncoder().fit(self.brand_tiers)
    
    def predict(self, inputs):
        """Make prediction from input dictionary"""
        try:
            # Calculate cost components (ratios can be adjusted)
            fabric_cost = inputs['selling_price'] * 0.35
            manuf_cost = inputs['selling_price'] * 0.25
            transport_cost = inputs['selling_price'] * 0.05
            tax = inputs['selling_price'] * 0.10
            brand_value = inputs['selling_price'] * 0.25
            
            # Prepare features array
            features = np.array([[
                fabric_cost,
                manuf_cost,
                transport_cost,
                tax,
                brand_value,
                self.fabric_encoder.transform([inputs['fabric']])[0],
                self.brand_encoder.transform([inputs['brand_tier']])[0],
                hash(inputs['product_type'].split()[0]) % 100
            ]])
            
            # Scale and predict
            features_scaled = self.scaler.transform(features)
            return {
                'predicted_price': float(self.model.predict(features_scaled)[0]),
                'cost_components': {
                    'Fabric': fabric_cost,
                    'Manufacturing': manuf_cost,
                    'Transport': transport_cost,
                    'Tax': tax,
                    'Brand Value': brand_value
                }
            }
            
        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")

def get_valid_input(prompt, valid_options=None, input_type=str):
    """Helper function for validated input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if input_type == float:
                return float(user_input)
            if valid_options and user_input.lower() not in [v.lower() for v in valid_options]:
                raise ValueError(f"Must be one of: {', '.join(valid_options)}")
            return user_input
        except ValueError as e:
            print(f"Invalid input: {e}\nPlease try again.")

def main():
    print("\n=== Fashion Cost Predictor ===")
    predictor = FashionCostPredictor()
    
    while True:
        try:
            print("\nAvailable Fabric Types:", ", ".join(predictor.fabric_types))
            print("Available Brand Tiers:", ", ".join(predictor.brand_tiers))
            
            inputs = {
                'fabric': get_valid_input(
                    "Enter fabric type: ",
                    valid_options=predictor.fabric_types
                ).lower(),
                'brand_tier': get_valid_input(
                    "Enter brand tier: ",
                    valid_options=predictor.brand_tiers
                ).lower(),
                'product_type': get_valid_input(
                    "Enter product type (e.g., 'Formal Shirt'): ",
                    input_type=str
                ),
                'selling_price': get_valid_input(
                    "Enter selling price (₹): ",
                    input_type=float
                )
            }
            
            result = predictor.predict(inputs)
            
            print("\n" + " COST BREAKDOWN ".center(50, "="))
            print(f"\nPredicted Selling Price: ₹{result['predicted_price']:,.2f}")
            print("\nCost Components:")
            for name, value in result['cost_components'].items():
                print(f"- {name}: ₹{value:,.2f}")
            print("\n" + "=" * 50)
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            
        if input("\nPredict another product? (y/n): ").lower() != 'y':
            print("Exiting predictor...")
            break

if __name__ == "__main__":
    main()