"""
Mock database for storing inventory items.
This simulates a database using an in-memory array.
"""

# Initial inventory items
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "quantity": 25,
        "price": 3.99,
        "barcode": "003766200063"
    },
    {
        "id": 2,
        "product_name": "Whole Grain Bread",
        "brands": "Nature's Own",
        "ingredients_text": "Whole wheat flour, water, honey, yeast, wheat gluten",
        "quantity": 15,
        "price": 2.49,
        "barcode": "007225002035"
    }
]

def get_all_items():
    """Return all inventory items."""
    return inventory

def get_item_by_id(item_id):
    """
    Return an item by its ID.
    
    Args:
        item_id (int): ID of the item to retrieve
        
    Returns:
        dict or None: Inventory item if found, None otherwise
    """
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def add_item(item):
    """
    Add a new item to the inventory.
    
    Args:
        item (dict): Item to add
        
    Returns:
        dict: The added item with assigned ID
    """
    # Generate new ID (max ID + 1)
    new_id = max([item["id"] for item in inventory], default=0) + 1
    item["id"] = new_id
    inventory.append(item)
    return item

def update_item(item_id, updated_data):
    """
    Update an existing item.
    
    Args:
        item_id (int): ID of the item to update
        updated_data (dict): New data for the item
        
    Returns:
        dict or None: Updated item if found, None otherwise
    """
    item = get_item_by_id(item_id)
    if item:
        for key, value in updated_data.items():
            if key != "id":  # Prevent ID from being changed
                item[key] = value
        return item
    return None

def delete_item(item_id):
    """
    Delete an item from the inventory.
    
    Args:
        item_id (int): ID of the item to delete
        
    Returns:
        bool: True if item was deleted, False otherwise
    """
    global inventory
    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            del inventory[i]
            return True
    return False