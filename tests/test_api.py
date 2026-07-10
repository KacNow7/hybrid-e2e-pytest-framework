import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def test_create_booking_via_api():
    payload = {
        "firstname": "Kacper",
        "lastname": "Nowikiewicz",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-01",
            "checkout": "2026-10-10"
        },
        "additionalneeds": "Breakfast"
    }
    
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    
    # Asercje poziomu produkcyjnego
    assert response.status_code == 200
    response_data = response.json()
    assert "bookingid" in response_data
    assert response_data["booking"]["firstname"] == "Kacper"
    assert response_data["booking"]["totalprice"] == 250