"""
Integration with the OpenFoodFacts API to fetch product details.
"""
import requests

OPENFOODFACTS_API_URL = "https://world.openfoodfacts.org/api/v0/product/"

def fetch_product_by_barcode(barcode):
    """
    Fetch product details from OpenFoodFacts API by barcode.
    
    Args:
        barcode (str): Product barcode
        
    Returns:
        dict: Product details or error message
    """
    try:
        response = requests.get(f"{OPENFOODFACTS_API_URL}{barcode}.json")
        data = response.json()
        
        if data.get("status") == 1:
            return {
                "success": True,
                "product": {
                    "product_name": data.get("product", {}).get("product_name", "Unknown"),
                    "brands": data.get("product", {}).get("brands", "Unknown"),
                    "ingredients_text": data.get("product", {}).get("ingredients_text", ""),
                    "image_url": data.get("product", {}).get("image_url", ""),
                    "nutriscore_grade": data.get("product", {}).get("nutriscore_grade", ""),
                    "categories": data.get("product", {}).get("categories", "")
                }
            }
        else:
            return {
                "success": False,
                "message": "Product not found"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"API request failed: {str(e)}"
        }

def search_products_by_name(product_name):
    """
    Search products by name using OpenFoodFacts API.
    
    Args:
        product_name (str): Product name to search for
        
    Returns:
        dict: Search results or error message
    """
    try:
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl", 
            params={
                "search_terms": product_name,
                "json": 1,
                "page_size": 5  # Limit results to 5 products
            }
        )
        data = response.json()
        
        if data.get("products"):
            results = []
            for product in data.get("products", []):
                results.append({
                    "product_name": product.get("product_name", "Unknown"),
                    "brands": product.get("brands", "Unknown"),
                    "barcode": product.get("code", ""),
                    "ingredients_text": product.get("ingredients_text", "")
                })
            return {
                "success": True,
                "products": results
            }
        else:
            return {
                "success": False,
                "message": "No products found"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"API request failed: {str(e)}"
        }