from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from app.services.calculus_service import CalculusService
from app.schemas.locations import Location

router = InferringRouter()
calculus_service = CalculusService()


@cbv(router)
class CalculusController:

    @router.post("/nearest", status_code=200)
    def find_nearest(self, location: Location):
        partner = calculus_service.find_nearest(location)
        if partner:
            return partner
        else:
            return JSONResponse(status_code=404, content={"message": "There is no partners near this location."})
