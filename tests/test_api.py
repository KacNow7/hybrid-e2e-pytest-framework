import requests
import os
from faker import Faker

fake = Faker()

def test_create_booking_with_dynamic_data():
    api_url = os.getenv("API_BASE_URL")
    
    # Generowanie dynamicznych danych dla każdego uruchomienia
    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=1000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-01",
            "checkout": "2026-10-10"
        }
    }
    
    response = requests.post(f"{api_url}/booking", json=payload)
    assert response.status_code == 200

# Ten test wstrzykuje naszą fixturę, która tworzy rezerwację i po teście ją usuwa
def test_get_booking_details(create_test_booking):
    api_url = os.getenv("API_BASE_URL")
    booking_id = create_test_booking # ID wygenerowane w fixturze
    
    response = requests.get(f"{api_url}/booking/{booking_id}")
    assert response.status_code == 200