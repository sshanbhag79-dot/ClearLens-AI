import requests
from typing import Optional
from typing import Optional
from backend.models import ProductData

def get_calories(product: dict) -> Optional[float]:
    """
    Extracts calories (kcal/100g) from product data.
    Handles kJ to kcal conversion if needed.
    """
    nutriments = product.get("nutriments", {})
    
    # 1. Try explicit kcal values
    kcal = nutriments.get("energy-kcal_100g") or nutriments.get("energy-kcal")
    if kcal is not None:
        try:
            return float(kcal)
        except ValueError:
            pass
            
    # 2. Try kJ values and convert (1 kJ = 0.239 kcal)
    kj = nutriments.get("energy_100g") or nutriments.get("energy-kj_100g") or nutriments.get("energy")
    if kj is not None:
        try:
            return float(kj) * 0.239
        except ValueError:
            pass
            
    return None

def get_product_by_barcode(barcode: str) -> Optional[ProductData]:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == 1:
            product = data.get("product", {})
            # Marketing labels are often in 'labels' or 'labels_tags'
            labels = product.get("labels", "")
            if not labels and product.get("labels_tags"):
                labels = ", ".join([t.replace("en:", "") for t in product.get("labels_tags", [])])

            return ProductData(
                code=barcode,
                product_name=product.get("product_name", "Unknown Product"),
                ingredients_text=product.get("ingredients_text", ""),
                marketing_claims=labels,
                image_url=product.get("image_url", None),
                nutriscore=product.get("nutriscore_grade", None),
                calories=get_calories(product),
                quantity_val=float(product.get("product_quantity")) if product.get("product_quantity") else None,
                quantity_unit=product.get("quantity", "").split(" ")[-1] if product.get("quantity") else "g" 
            )
        return None
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None
