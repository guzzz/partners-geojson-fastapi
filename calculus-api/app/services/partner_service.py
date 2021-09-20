import json

from structlog import get_logger
from fastapi.encoders import jsonable_encoder

from app.repositories.partner_repository import PartnerRepository
from app.services.redis_service import RedisService

partner_repository = PartnerRepository()
redis_service = RedisService()
log = get_logger()


class PartnerService:

    def __init__(self):
        self.database = partner_repository
        self.mem_database = redis_service

    def create(self, partner_obj):
        log.info("[CREATE - partner] Started creation service...")
        partner = jsonable_encoder(partner_obj)
        self.database.create(partner)
        self.mem_database.clear()
        return partner

    def delete(self, id):
        log.info("[DELETE - partner] Started delete service...")
        self.database.delete(id)
        self.mem_database.delete_value(id)
