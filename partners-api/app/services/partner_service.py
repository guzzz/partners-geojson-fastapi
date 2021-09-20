import json
import uuid

from structlog import get_logger
from fastapi.encoders import jsonable_encoder

from app.serializers.partner_serializer import partner_serializer, partners_serializer
from app.repositories.partner_repository import PartnerRepository
from app.services.redis_service import RedisService
from app.producer import publish
from app.utils.dates import now

partner_repository = PartnerRepository()
redis_service = RedisService()
log = get_logger()


class PartnerService:

    def __init__(self):
        self.database = partner_repository
        self.mem_database = redis_service

    def retrieve(self, partner_id):
        log.info("[RETRIEVE - partner] Started retrieve service...")
        log.info("[CACHE - partner] Searching in cache...")
        obj_from_mem = self.mem_database.get_value(str(partner_id))
        if obj_from_mem:
            partner = json.loads(obj_from_mem.decode("UTF-8"))
        else:
            log.info("[CACHE - partner] Not found...")
            partner = self.retrieve_from_db(partner_id)
        return partner

    def retrieve_from_db(self, id, partner_id=True):
        log.info("[DB - partner] Searching in database...")
        obj_from_db = self.database.retrieve(id, partner_id)
        if obj_from_db:
            partner = partner_serializer(obj_from_db)
            partner_to_store = json.dumps(partner).encode('utf-8')
            self.mem_database.set_value(partner["id"], partner_to_store)
        else:
            log.info("[DB - partner] Not found...")
            partner = None
        return partner

    def list(self, page, limit):
        log.info("[LIST - partner] Started list service...")
        return partners_serializer(self.database.list(page, limit))

    def create(self, partner_obj):
        log.info("[CREATE - partner] Started creation service...")
        partner = jsonable_encoder(partner_obj)

        partner_id = partner["id"]
        if not partner_id:
            partner["id"] = str(uuid.uuid4())
        else:
            partner["id"] = str(partner_id)

        partner["created_at"] = now()
        partner["updated_at"] = now()
        result = self.database.create(partner)
        if result:
            del partner["_id"]
            publish(action="create", body=partner)
            return self.retrieve_from_db(result.inserted_id, partner_id=False)
        else:
            log.info("[CREATE - partner] Failure...")
            return False

    def delete(self, id):
        log.info("[DELETE - partner] Started delete service...")
        self.database.delete(id)
        self.mem_database.delete_value(id)
        publish(action="delete", body={"id": id})
