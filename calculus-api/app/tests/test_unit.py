import uuid
import pytest

from fastapi.testclient import TestClient

from app.services.partner_service import PartnerService
from app.main import app

client = TestClient(app)
partner_service = PartnerService()


def create_partner():
    partner = {
        "id": str(uuid.uuid4()),
        "tradingName": "Boate do Romário",
        "ownerName": "Ronaldinho Gaúcho",
        "document": str(uuid.uuid4()),
        "coverageArea": {"type": "MultiPolygon", "coordinates": [ [ [ [107, 7], [108, 7], [108, 8], [107, 8], [107, 7] ] ], [ [ [100, 0], [101, 0], [101, 1], [100, 1], [100, 0] ] ] ]},
        "address": {"type": "Point","coordinates": [-46.57421, -21.785741]}
    }
    response = partner_service.create(partner)
    return response

def delete_partner(id):
    partner_service.delete(id)

def test_create_partner_service_success():
    partner = create_partner()
    delete_partner(partner.get("id"))
    assert partner.get("tradingName") == "Boate do Romário"
    assert partner.get("ownerName") == "Ronaldinho Gaúcho"
