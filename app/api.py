"""
Flask API endpoints for the inventory management system.
"""
from flask import Blueprint, jsonify, request
from app.db import (
    get_all_items, get_item_by_id, add_item, 
    update_item, delete_item
)
from app.external_api import fetch_product_by_barcode, search_products_by_name

# Create Blueprint for API routes
api_bp = Blueprint('api', __name__)

# GET /inventory - Fetch all items
@api_bp.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(get_all_items())

# GET /inventory/<id> - Fetch a single item
@api_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# POST /inventory - Add a new item
@api_bp.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('product_name'):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create new item
    new_item = add_item(data)
    return jsonify(new_item), 201

# PATCH /inventory/<id> - Update an item
@api_bp.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    updated_item = update_item(item_id, data)
    if updated_item:
        return jsonify(updated_item)
    return jsonify({"error": "Item not found"}), 404

# DELETE /inventory/<id> - Remove an item
@api_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    success = delete_item(item_id)
    if success:
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404

# GET /lookup/barcode/<barcode> - Lookup product by barcode
@api_bp.route('/lookup/barcode/<barcode>', methods=['GET'])
def lookup_by_barcode(barcode):
    result = fetch_product_by_barcode(barcode)
    if result.get("success"):
        return jsonify(result)
    return jsonify(result), 404

# GET /lookup/name/<name> - Search products by name
@api_bp.route('/lookup/name/<name>', methods=['GET'])
def lookup_by_name(name):
    result = search_products_by_name(name)
    if result.get("success"):
        return jsonify(result)
    return jsonify(result), 404