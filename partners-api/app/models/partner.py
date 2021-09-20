import json
from typing import Union, Optional

from pydantic import BaseModel, validator, StrictStr, Field, StrictInt
from shapely.validation import explain_validity
from marshmallow_geojson import GeoJSONSchema
from marshmallow.exceptions import ValidationError

from app.errors import AddressError, CoverageAreaError
from app.utils.geojson_converter import geojson2shp

geojson_schema = GeoJSONSchema()
        

class Partner(BaseModel):
    id: Optional[Union[StrictInt, StrictStr]] = Field(None, example="bf94964d-9d77-4fd6-88d7-54e2c0386c7c")
    tradingName: StrictStr = Field(..., example="Fala Zeze")
    ownerName: StrictStr = Field(..., example="Thiago Neves")
    document: StrictStr = Field(..., example="1432132123891/0001")
    coverageArea: dict = Field(..., example={"type":"MultiPolygon","coordinates":[[[[-67.83039,-9.95782],[-67.83176,-9.98487],[-67.78627,-9.98825],[-67.78885,-9.95105],[-67.83039,-9.95782]]]]})
    address: dict = Field(..., example={"type":"Point","coordinates":[-67.81702,-9.970223]})

    @validator("coverageArea")
    def validate_coverage_area(cls, value):
        str_value = json.dumps(value)

        try:
            geojson = geojson_schema.loads(str_value)
        except ValidationError:
            raise CoverageAreaError

        shapely_obj = geojson2shp(geojson)
        if not shapely_obj.is_valid:
            explanation = explain_validity(shapely_obj)
            if "Self-intersection" in explanation:
                print("Multipolygon self-intersection found")
                value["Self-intersection"] = True
                return value
            else:
                raise CoverageAreaError

        return value

    @validator("address")
    def validate_address(cls, value):
        str_value = json.dumps(value)

        try:
            geojson = geojson_schema.loads(str_value)
        except ValidationError:
            raise AddressError

        shapely_obj = geojson2shp(geojson)
        if not shapely_obj.is_valid:
            raise AddressError
        return value
