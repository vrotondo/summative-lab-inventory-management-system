"""
Command-line interface for the Inventory Management System.
"""
import argparse
import json
import requests
import sys
import os

# Set the API base URL
API_BASE_URL = "http://127.0.0.1:5000"

def pretty_print(data):
    """Print data in a readable format."""
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2))
    else:
        print(data)

def list_inventory():
    """Fetch and display all inventory items."""
    try:
        response = requests.get(f"{API_BASE_URL}/inventory")
        response.raise_for_status()
        items = response.json()
        
        if not items:
            print("No items in inventory.")
            return
        
        print(f"Total items: {len(items)}")
        for item in items:
            print(f"ID: {item['id']} | {item['product_name']} | Brand: {item['brands']} | Qty: {item['quantity']} | Price: ${item['price']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def get_item(item_id):
    """Fetch and display a specific inventory item."""
    try:
        response = requests.get(f"{API_BASE_URL}/inventory/{item_id}")
        response.raise_for_status()
        item = response.json()
        print("Item details:")
        pretty_print(item)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Item with ID {item_id} not found.")
        else:
            print(f"Error: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def add_item():
    """Add a new item to inventory."""
    try:
        # Get product details from user
        product_name = input("Product name: ")
        
        # Option to fetch from OpenFoodFacts
        use_api = input("Look up product details from OpenFoodFacts? (y/n): ").lower() == 'y'
        
        if use_api:
            search_method = input("Search by (b)arcode or (n)ame?: ").lower()
            
            if search_method == 'b':
                barcode = input("Enter barcode: ")
                response = requests.get(f"{API_BASE_URL}/lookup/barcode/{barcode}")
                response.raise_for_status()
                data = response.json()
                
                if data.get("success"):
                    product = data.get("product", {})
                    brands = product.get("brands", "")
                    ingredients = product.get("ingredients_text", "")
                else:
                    print("Product not found in OpenFoodFacts database.")
                    brands = input("Brand: ")
                    ingredients = input("Ingredients: ")
            
            elif search_method == 'n':
                product_name = input("Enter product name: ")
                response = requests.get(f"{API_BASE_URL}/lookup/name/{product_name}")
                response.raise_for_status()
                data = response.json()
                
                if data.get("success") and data.get("products"):
                    # Display search results
                    print("Search results:")
                    for i, product in enumerate(data.get("products", [])):
                        print(f"{i+1}. {product.get('product_name')} - {product.get('brands')}")
                    
                    # Let user select a product
                    selection = int(input("Select a product (number) or 0 to enter manually: "))
                    if 1 <= selection <= len(data.get("products", [])):
                        selected_product = data.get("products")[selection-1]
                        product_name = selected_product.get("product_name")
                        brands = selected_product.get("brands")
                        ingredients = selected_product.get("ingredients_text")
                    else:
                        brands = input("Brand: ")
                        ingredients = input("Ingredients: ")
                else:
                    print("No products found.")
                    brands = input("Brand: ")
                    ingredients = input("Ingredients: ")
            else:
                brands = input("Brand: ")
                ingredients = input("Ingredients: ")
        else:
            brands = input("Brand: ")
            ingredients = input("Ingredients: ")
        
        # Get quantity and price
        while True:
            try:
                quantity = int(input("Quantity: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        while True:
            try:
                price = float(input("Price: $"))
                break
            except ValueError:
                print("Please enter a valid price.")
        
        # Create item data
        item_data = {
            "product_name": product_name,
            "brands": brands,
            "ingredients_text": ingredients,
            "quantity": quantity,
            "price": price
        }
        
        # Add barcode if available
        barcode = input("Barcode (optional): ")
        if barcode:
            item_data["barcode"] = barcode
        
        # Send to API
        response = requests.post(
            f"{API_BASE_URL}/inventory",
            json=item_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        print("Item added successfully:")
        pretty_print(response.json())
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def update_item(item_id):
    """Update an existing inventory item."""
    try:
        # First, get the current item
        response = requests.get(f"{API_BASE_URL}/inventory/{item_id}")
        response.raise_for_status()
        item = response.json()
        
        print("Current item details:")
        pretty_print(item)
        
        # Get updated values (or keep current)
        print("\nEnter new values (or press Enter to keep current):")
        
        product_name = input(f"Product name [{item.get('product_name')}]: ")
        brands = input(f"Brand [{item.get('brands')}]: ")
        ingredients = input(f"Ingredients [{item.get('ingredients_text')}]: ")
        
        quantity_str = input(f"Quantity [{item.get('quantity')}]: ")
        price_str = input(f"Price [${item.get('price')}]: ")
        
        # Build update data (only include fields that were changed)
        update_data = {}
        
        if product_name:
            update_data["product_name"] = product_name
        if brands:
            update_data["brands"] = brands
        if ingredients:
            update_data["ingredients_text"] = ingredients
        
        try:
            if quantity_str:
                update_data["quantity"] = int(quantity_str)
        except ValueError:
            print("Invalid quantity. This field will not be updated.")
        
        try:
            if price_str:
                update_data["price"] = float(price_str)
        except ValueError:
            print("Invalid price. This field will not be updated.")
        
        # Send update to API
        if update_data:
            response = requests.patch(
                f"{API_BASE_URL}/inventory/{item_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            print("Item updated successfully:")
            pretty_print(response.json())
        else:
            print("No changes made.")
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Item with ID {item_id} not found.")
        else:
            print(f"Error: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def delete_item(item_id):
    """Delete an inventory item."""
    try:
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").lower()
        
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        
        response = requests.delete(f"{API_BASE_URL}/inventory/{item_id}")
        response.raise_for_status()
        
        print("Item deleted successfully.")
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Item with ID {item_id} not found.")
        else:
            print(f"Error: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def lookup_product():
    """Look up a product from the OpenFoodFacts API."""
    try:
        search_type = input("Search by (b)arcode or (n)ame?: ").lower()
        
        if search_type == 'b':
            barcode = input("Enter barcode: ")
            response = requests.get(f"{API_BASE_URL}/lookup/barcode/{barcode}")
        elif search_type == 'n':
            name = input("Enter product name: ")
            response = requests.get(f"{API_BASE_URL}/lookup/name/{name}")
        else:
            print("Invalid option.")
            return
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            if search_type == 'b':
                print("Product found:")
                pretty_print(result.get("product"))
            else:
                print(f"Found {len(result.get('products', []))} products:")
                for product in result.get("products", []):
                    print(f"- {product.get('product_name')} ({product.get('brands')})")
                    print(f"  Barcode: {product.get('barcode')}")
                    print()
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Inventory Management System CLI")
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all inventory items")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get a specific inventory item")
    get_parser.add_argument("id", type=int, help="Item ID")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new inventory item")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update an inventory item")
    update_parser.add_argument("id", type=int, help="Item ID to update")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an inventory item")
    delete_parser.add_argument("id", type=int, help="Item ID to delete")
    
    # Lookup command
    lookup_parser = subparsers.add_parser("lookup", help="Look up a product in OpenFoodFacts")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == "list":
        list_inventory()
    elif args.command == "get":
        get_item(args.id)
    elif args.command == "add":
        add_item()
    elif args.command == "update":
        update_item(args.id)
    elif args.command == "delete":
        delete_item(args.id)
    elif args.command == "lookup":
        lookup_product()

if __name__ == "__main__":
    main()