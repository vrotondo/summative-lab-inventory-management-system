"""
Unit tests for the API endpoints.
"""
import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    """Test GET /inventory endpoint."""
    response = client.get("/inventory")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_item(client):
    """Test GET /inventory/<id> endpoint."""
    # First, ensure we have at least one item
    response = client.get("/inventory")
    data = json.loads(response.data)
    
    if data:
        item_id = data[0]["id"]
        response = client.get(f"/inventory/{item_id}")
        assert response.status_code == 200
        item = json.loads(response.data)
        assert item["id"] == item_id
    
    # Test with non-existent ID
    response = client.get("/inventory/9999")
    assert response.status_code == 404

def test_create_item(client):
    """Test POST /inventory endpoint."""
    new_item = {
        "product_name": "Test Product",
        "brands": "Test Brand",
        "ingredients_text": "Test ingredients",
        "quantity": 10,
        "price": 9.99
    }
    
    response = client.post(
        "/inventory",
        data=json.dumps(new_item),
        content_type="application/json"
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "id" in data
    assert data["product_name"] == new_item["product_name"]

def test_update_item(client):
    """Test PATCH /inventory/<id> endpoint."""
    # First, get an existing item
    response = client.get("/inventory")
    data = json.loads(response.data)
    
    if data:
        item_id = data[0]["id"]
        update_data = {"price": 12.99}
        
        response = client.patch(
            f"/inventory/{item_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        updated_item = json.loads(response.data)
        assert updated_item["price"] == update_data["price"]

def test_delete_item(client):
    """Test DELETE /inventory/<id> endpoint."""
    # First, create an item to delete
    new_item = {
        "product_name": "Delete Test Product",
        "quantity": 1,
        "price": 1.99
    }
    
    response = client.post(
        "/inventory",
        data=json.dumps(new_item),
        content_type="application/json"
    )
    
    created_item = json.loads(response.data)
    item_id = created_item["id"]
    
    # Now delete it
    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 404