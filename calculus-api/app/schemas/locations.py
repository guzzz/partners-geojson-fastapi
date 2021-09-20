from pydantic import BaseModel, Field


class Location(BaseModel):
    lat: float = Field(..., example="-67.81702")
    long: float = Field(..., example="-9.970223")
