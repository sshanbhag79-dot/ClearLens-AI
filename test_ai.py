import os
from dotenv import load_dotenv

load_dotenv()

from backend.services.ai_analyzer import analyze_safety
from backend.models import ProductData, UserProfile

# Mock Data
mock_product = ProductData(
    code="123456",
    product_name="Honey Nut Granola",
    ingredients_text="Oats, Honey, Almonds, Palm Oil, Sugar",
    image_url=None,
    nutriscore="D"
)

mock_profile = UserProfile(
    allergies=["Nuts"],
    diets=["Vegan"],
    strictness="Strict"
)

print("--- TESTING AI ANALYSIS (End-to-End) ---")
print(f"Product: {mock_product.product_name}")
print(f"Ingredients: {mock_product.ingredients_text}")
print(f"Profile: Allergies={mock_profile.allergies}, Diets={mock_profile.diets}")
print("---------------------------")

try:
    result = analyze_safety(mock_product, mock_profile)
    print("\n--- RESULT ---")
    print(f"Status: {result.status}")
    print(f"Reason: {result.reason}")
    print(f"Alternative: {result.alternative}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
