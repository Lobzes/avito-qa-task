import requests
import random

BASE_URL = "https://qa-internship.avito.com"

def debug_create():
    seller_id = random.randint(111111, 999999)
    item_data = {
        "sellerID": seller_id,
        "name": f"Test Item {random.randint(1, 1000)}",
        "price": random.randint(100, 10000),
        "statistics": {
            "likes": random.randint(0, 100),
            "viewCount": random.randint(0, 1000),
            "contacts": random.randint(0, 50)
        }
    }
    url = f"{BASE_URL}/api/1/item"
    response = requests.post(url, json=item_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

if __name__ == "__main__":
    debug_create()
