import uuid
import json

from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from app.services.partner_service import PartnerService
from app.models.partner import Partner
from app.main import app

client = TestClient(app)
partner_service = PartnerService()


def create_partner():
    partner = {
        "id": str(uuid.uuid4()),
        "tradingName": "Boate do Romário",
        "ownerName": "Ronaldinho Gaúcho",
        "document": str(uuid.uuid4()),
        "coverageArea": {"type":"MultiPolygon","coordinates":[[[[-44.04912,-19.87743],[-44.0493,-19.89438],[-44.04758,-19.90212],[-44.04346,-19.90922],[-44.03385,-19.91923],[-44.01891,-19.92165],[-44.01647,-19.92306],[-44.01436,-19.92319],[-44.01175,-19.92427],[-44.00724,-19.92585],[-43.99909,-19.9185],[-43.99432,-19.91403],[-43.99557,-19.90842],[-43.99582,-19.90285],[-43.99436,-19.89002],[-43.99316,-19.8792],[-43.99436,-19.87371],[-43.99951,-19.86532],[-44.01917,-19.85135],[-44.02801,-19.8545],[-44.03745,-19.85668],[-44.04397,-19.8608],[-44.04912,-19.87743]]]]},
        "address": {"type":"Point","coordinates":[-44.012478,-19.887215]}
    }
    response = client.post("/v0/partners/", json=partner)
    return response

def delete_partner(id):
    partner_service.delete(id)

def test_create_partner():
    response = create_partner()
    data = response.json()
    delete_partner(data["id"])
    assert response.status_code == 201, response.text
    assert data["tradingName"] == "Boate do Romário"
    assert "id" in data

def test_list_partners():
    response = client.get(f"/v0/partners")
    assert response.status_code == 200

def test_retrieve_partner_not_found_error():
    response = client.get("/v0/partners/8621bd75-bb20-4978-bf63-02575fe3468c")
    assert response.status_code == 404

def test_retrieve_valid_id():
    response = create_partner()
    data = response.json()
    id = data["id"]
    response = client.get(f"/v0/partners/{id}")
    delete_partner(data["id"])
    assert response.status_code == 200
