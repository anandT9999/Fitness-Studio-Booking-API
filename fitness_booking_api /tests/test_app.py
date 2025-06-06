from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_booking_flow():
    # Check existing classes
    classes = client.get("/classes").json()
    class_id = classes[0]["id"]

    # Book a class
    payload = {
        "class_id": class_id,
        "client_name": "anand",
        "client_email": "anandtorati@gmail.com"
    }
    response = client.post("/book", json=payload)
    assert response.status_code == 200
    assert response.json()["client_email"] == "anandtorati@gmail.com"

    # Fetch bookings
    bookings = client.get(f"/bookings?email={payload['client_email']}")
    assert bookings.status_code == 200
    assert len(bookings.json()) >= 1
