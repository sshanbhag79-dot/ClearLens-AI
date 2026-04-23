from backend.services.open_food_facts import get_calories

def test_conversion():
    # Case 1: Kcal present
    prod_kcal = {"nutriments": {"energy-kcal_100g": 100}}
    assert get_calories(prod_kcal) == 100.0, "Should favor kcal"
    
    # Case 2: Only kJ present (1000 kJ ~= 239 kcal)
    prod_kj = {"nutriments": {"energy_100g": 1000}}
    res = get_calories(prod_kj)
    assert res == 239.0, f"Should convert kJ. Got {res}"
    
    # Case 3: Mixed (Should favor kcal)
    prod_mixed = {"nutriments": {"energy-kcal_100g": 50, "energy_100g": 1000}}
    assert get_calories(prod_mixed) == 50.0, "Should prioritize kcal over kJ"
    
    # Case 4: No data
    prod_none = {"nutriments": {}}
    assert get_calories(prod_none) is None, "Should handle missing data"

    print("All calorie tests passed!")

if __name__ == "__main__":
    test_conversion()
