from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from marshmallow.exceptions import ValidationError

from app.controllers import partner_controller
from app.errors import CustomError, AddressError, CoverageAreaError


app = FastAPI()
app.include_router(
    partner_controller.router,
    prefix="/v0/partners",
    tags=["Partners"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return CustomError.get_error(exc)

@app.exception_handler(AddressError)
async def validation_address_handler(request, exc):
    return AddressError.get_error()

@app.exception_handler(CoverageAreaError)
async def validation_coverage_area_handler(request, exc):
    return CoverageAreaError.get_error()

