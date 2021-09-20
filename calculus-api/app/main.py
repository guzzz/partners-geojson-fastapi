from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.controllers import calculus_controller
from app.errors import CustomError


app = FastAPI()
app.include_router(
    calculus_controller.router,
    prefix="/v0",
    tags=["Calculus"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return CustomError.get_error(exc)
