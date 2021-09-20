import uuid
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.models.partner import Partner
from app.errors import CoverageAreaError, AddressError

client = TestClient(app)


def test_partner_obj():
    partner = Partner(
        id = str(uuid.uuid4()),
        tradingName = "Boate do Romário",
        ownerName = "Ronaldinho Gaúcho",
        document = str(uuid.uuid4()),
        coverageArea = {"type": "MultiPolygon", "coordinates": [ [ [ [107, 7], [108, 7], [108, 8], [107, 8], [107, 7] ] ], [ [ [100, 0], [101, 0], [101, 1], [100, 1], [100, 0] ] ] ]},
        address = {"type": "Point","coordinates": [-46.57421, -21.785741]}
    )
    assert partner.tradingName == "Boate do Romário"
    assert partner.ownerName == "Ronaldinho Gaúcho"

def test_partner_obj_error_address():
    with pytest.raises(AddressError) as excinfo:

        def f():
            error = Partner(
                id = str(uuid.uuid4()),
                tradingName = "Boate do Romário",
                ownerName = "Ronaldinho Gaúcho",
                document = str(uuid.uuid4()),
                coverageArea = {"type": "MultiPolygon", "coordinates": [ [ [ [107, 7], [108, 7], [108, 8], [107, 8], [107, 7] ] ], [ [ [100, 0], [101, 0], [101, 1], [100, 1], [100, 0] ] ] ]},
                address = {"type": "Point","coordinates": [-4116.57421, -2111.785741]}
            )

        f()
    assert "address - Invalid GeoJSON" == str(excinfo.value)

def test_partner_obj_error_coverage_area():
    with pytest.raises(CoverageAreaError) as excinfo:

        def f():
            error = Partner(
                id = str(uuid.uuid4()),
                tradingName = "Boate do Romário",
                ownerName = "Ronaldinho Gaúcho",
                document = str(uuid.uuid4()),
                coverageArea = {"type": "MultiPolygon", "coordinates": [ [ [ [11111111107, 11111111117], [108, 7], [108, 8], [107, 8], [107, 7] ] ], [ [ [100, 0], [101, 0], [101, 1], [100, 1], [100, 0] ] ] ]},
                address = {"type": "Point","coordinates": [-46.57421, -21.785741]}
            )

        f()
    assert "coverageArea - Invalid GeoJSON" == str(excinfo.value)
