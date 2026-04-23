def verify_pepsi_calculation():
    # Pepsi Max Data (from reproduce_issue.py)
    product_name = "Pepsi Max"
    cal_per_100g = 0.4
    product_quantity = 330.0 # ml
    quantity_unit = "ml"
    
    # User Input
    user_quantity = 5.0 # "5 cans"
    
    print(f"--- Verification for {product_name} ---")
    print(f"Calories per 100g: {cal_per_100g} kcal")
    print(f"Unit Size: {product_quantity} {quantity_unit}")
    print(f"User Quantity: {user_quantity} units")
    
    # OLD LOGIC (Quantity = 100g servings)
    # user_quantity 5 was treated as 5 * 100g = 500g
    old_total_grams = user_quantity * 100
    old_total_cals = (old_total_grams / 100) * cal_per_100g
    print(f"\n[OLD LOGIC] Total Cals: {old_total_cals:.2f} kcal (Assumed 500g)")
    
    # NEW LOGIC (Quantity = Units)
    # user_quantity 5 is treated as 5 * 330ml = 1650ml
    new_total_grams = user_quantity * product_quantity
    new_total_cals = (new_total_grams / 100) * cal_per_100g
    print(f"\n[NEW LOGIC] Total Cals: {new_total_cals:.2f} kcal (Assumed {new_total_grams}g/ml)")
    
    print(f"\nDifference: +{new_total_cals - old_total_cals:.2f} kcal")
    print("NOTE: Pepsi Max is nearly 0 calories, so the absolute number remains small.")
    print("      For confirmed 'Standard Coke' (42kcal/100g):")
    
    # Comparison for Regular Coke
    coke_cals = 42.0
    coke_old = (user_quantity * 100 / 100) * coke_cals
    coke_new = (user_quantity * 330 / 100) * coke_cals
    print(f"      Old Logic (500g): {coke_old:.1f} kcal")
    print(f"      New Logic (5 cans): {coke_new:.1f} kcal")

if __name__ == "__main__":
    verify_pepsi_calculation()
