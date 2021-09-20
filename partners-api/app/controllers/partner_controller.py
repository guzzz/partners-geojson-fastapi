from typing import Optional, List

from fastapi_utils.cbv import cbv
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, status, Response, Header
from fastapi_utils.inferring_router import InferringRouter

from app.models.partner import Partner
from app.schemas.pdv import InitialData
from app.services.partner_service import PartnerService

router = InferringRouter()
partner_service = PartnerService()


@cbv(router)
class PartnerController:

    @router.get("/")
    def find_all_partners(self, page: Optional[int] = Header(1), limit: Optional[int] = Header(10)):
        return partner_service.list(page, limit)

    @router.get("/{id}", status_code=200)
    def find_one_partner(self, id: str, response: Response):
        search_result = partner_service.retrieve(id)
        if search_result:
            return search_result
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"It was not possible to find the partner_id: {id}"}

    @router.post("/", status_code=201)
    def create_partner(self, partner: Partner, response: Response):
        partner = partner_service.create(partner)
        if partner:
            return partner
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Invalid input": f"Verify your input data. Remember that the document and the id are unique for each partner and that we need valid GeoJSONs!"}

 
    @router.post("/import-data", status_code=201, include_in_schema=False)
    def create_test_base(self, body: InitialData, response: Response):
        partners_list  = body.pdvs
        for partner_obj in partners_list:
            partner = jsonable_encoder(partner_obj)
            result = partner_service.create(partner)
        return
