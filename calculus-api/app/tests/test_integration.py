import uuid

from fastapi.testclient import TestClient

from app.services.partner_service import PartnerService
from app.main import app

client = TestClient(app)
partner_service = PartnerService()


def create_partner():
    partner = {
        "id": str(uuid.uuid4()),
        "tradingName": "Reinight",
        "ownerName": "Vini Jr.",
        "document": str(uuid.uuid4()),
        "coverageArea": {"type":"MultiPolygon","coordinates":[[[[-44.04912,-19.87743],[-44.0493,-19.89438],[-44.04758,-19.90212],[-44.04346,-19.90922],[-44.03385,-19.91923],[-44.01891,-19.92165],[-44.01647,-19.92306],[-44.01436,-19.92319],[-44.01175,-19.92427],[-44.00724,-19.92585],[-43.99909,-19.9185],[-43.99432,-19.91403],[-43.99557,-19.90842],[-43.99582,-19.90285],[-43.99436,-19.89002],[-43.99316,-19.8792],[-43.99436,-19.87371],[-43.99951,-19.86532],[-44.01917,-19.85135],[-44.02801,-19.8545],[-44.03745,-19.85668],[-44.04397,-19.8608],[-44.04912,-19.87743]]]]},
        "address": {"type":"Point","coordinates":[-44.012478,-19.887215]}
    }
    result = partner_service.create(partner)
    return result

def delete_partner(id):
    partner_service.delete(id)

def test_find_nearest_success():
    creation_result = create_partner()
    location = { "lat": -44.012478, "long": -19.887215 }
    response = client.post("/v0/nearest", json=location)
    delete_partner(creation_result["id"])
    assert response.status_code == 200, response.text

def test_find_nearest_not_found():
    creation_result = create_partner()
    location = { "lat": -45.012478, "long": -21.887215 }
    response = client.post("/v0/nearest", json=location)
    delete_partner(creation_result["id"])
    assert response.status_code == 404, response.text
    data = response.json()
    assert "There is no partners near this location." == data.get("message")

def test_find_nearest_lat_bad_request():
    location = { "lataaaa": -45.012478, "long": -21.887215 }
    response = client.post("/v0/nearest", json=location)
    assert response.status_code == 400, response.text

def test_find_nearest_long_bad_request():
    location = { "lat": -45.012478, "longaaa": -21.887215 }
    response = client.post("/v0/nearest", json=location)
    assert response.status_code == 400, response.text

def test_find_nearest_bad_request_fields_required():
    response = client.post("/v0/nearest", json={})
    assert response.status_code == 400, response.text
