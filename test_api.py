import pytest
import requests
import random
import string
import uuid

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture
def seller_id():
    # Generate a random seller ID between 111111 and 999999
    return random.randint(111111, 999999)

@pytest.fixture
def item_data(seller_id):
    return {
        "sellerID": seller_id,
        "name": f"Test Item {random.randint(1, 1000)}",
        "price": random.randint(100, 10000),
        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(0, 1000),
            "contacts": random.randint(0, 50)
        }
    }

def extract_id_from_response(response_json):
    """Extract ID from the 'status' field in the response."""
    # Response format: {"status": "Сохранили объявление - <UUID>"}
    status = response_json.get('status', '')
    if "Сохранили объявление -" in status:
        return status.split(" - ")[-1]
    return None

def test_create_item(item_data):
    """Test creating a new advertisement."""
    url = f"{BASE_URL}/api/1/item"
    response = requests.post(url, json=item_data)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
    
    data = response.json()
    print(f"Create Response: {data}")
    
    assert 'status' in data
    assert "Сохранили объявление" in data['status']
    
    item_id = extract_id_from_response(data)
    assert item_id is not None
    # Basic UUID validation
    assert len(item_id) > 20 

def test_get_item_by_id(item_data):
    """Test retrieving an advertisement by ID."""
    # 1. Create item
    create_url = f"{BASE_URL}/api/1/item"
    create_response = requests.post(create_url, json=item_data)
    assert create_response.status_code == 200
    
    create_data = create_response.json()
    item_id = extract_id_from_response(create_data)
    assert item_id is not None, f"Could not extract ID from response: {create_data}"

    # 2. Get item
    get_url = f"{BASE_URL}/api/1/item/{item_id}"
    get_response = requests.get(get_url)
    
    assert get_response.status_code == 200
    get_data = get_response.json()
    
    # Verify response fields
    # Note: The API might return the item directly or wrapped.
    # Based on Postman, it returns the item object.
    # But let's be careful.
    # If get_data is a list (which happened in one Postman example), we handle it.
    if isinstance(get_data, list):
        item = get_data[0]
    else:
        item = get_data
        
    assert item['id'] == item_id
    assert item['sellerId'] == item_data['sellerID']
    assert item['name'] == item_data['name']
    assert item['price'] == item_data['price']

def test_get_items_by_seller_id(seller_id, item_data):
    """Test retrieving all advertisements for a seller."""
    # 1. Create 2 items
    create_url = f"{BASE_URL}/api/1/item"
    requests.post(create_url, json=item_data)
    
    item_data_2 = item_data.copy()
    item_data_2['name'] = "Test Item 2"
    requests.post(create_url, json=item_data_2)
    
    # 2. Get items by seller ID
    get_url = f"{BASE_URL}/api/1/{seller_id}/item"
    response = requests.get(get_url)
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Verify the items belong to the seller
    for item in data:
        assert item['sellerId'] == seller_id

def test_get_statistic(item_data):
    """Test retrieving statistics for an item."""
    # 1. Create item
    create_url = f"{BASE_URL}/api/1/item"
    create_response = requests.post(create_url, json=item_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    item_id = extract_id_from_response(create_data)
    
    assert item_id is not None
    
    # 2. Get statistics
    stat_url = f"{BASE_URL}/api/1/statistic/{item_id}"
    response = requests.get(stat_url)
    
    assert response.status_code == 200
    data = response.json()
    
    # The API seems to return an array of stats based on Postman.
    if isinstance(data, list):
        assert len(data) > 0
        stats = data[0]
    else:
        stats = data
        
    # Verify stats match
    assert 'likes' in stats
    assert 'viewCount' in stats
    assert 'contacts' in stats
    
    # Note: The API might return strings for numbers.
    assert int(stats['likes']) == item_data['statistics']['likes']
    assert int(stats['viewCount']) == item_data['statistics']['viewCount']
    assert int(stats['contacts']) == item_data['statistics']['contacts']

def test_create_item_invalid_data():
    """Test creating item with invalid data (negative test)."""
    url = f"{BASE_URL}/api/1/item"
    invalid_data = {
        "sellerID": 123456,
        "name": "Invalid Item",
        "price": "not a number", # Invalid price
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
    }
    response = requests.post(url, json=invalid_data)
    assert response.status_code == 400

def test_get_item_not_found():
    """Test getting a non-existent item."""
    # Use a valid UUID format that is unlikely to exist
    non_existent_id = str(uuid.uuid4())
    url = f"{BASE_URL}/api/1/item/{non_existent_id}"
    response = requests.get(url)
    
    # Expect 404. If API returns 400 for valid UUIDs that don't exist, we might need to adjust.
    # But 404 is the correct status for "Not Found".
    assert response.status_code == 404
