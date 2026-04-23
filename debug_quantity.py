from backend.services.open_food_facts import get_product_by_barcode

def debug_pepsi_quantity():
    barcode = "4060800104045" # Pepsi Max
    print(f"Fetching product for barcode: {barcode}")
    
    product = get_product_by_barcode(barcode)
    
    if product:
        print("\n--- Product Data Object ---")
        print(f"Name: {product.product_name}")
        print(f"Calories: {product.calories}")
        print(f"Quantity Val: {product.quantity_val}")
        print(f"Quantity Unit: {product.quantity_unit}")
        
        if product.quantity_val:
            print("[SUCCESS] Quantity detected.")
        else:
            print("[FAIL] Quantity NOT detected (None).")
            
    else:
        print("Product not found.")

if __name__ == "__main__":
    debug_pepsi_quantity()
