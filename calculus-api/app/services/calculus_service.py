import json

from structlog import get_logger

from app.services.redis_service import RedisService
from app.serializers.partner_serializer import partner_serializer
from app.repositories.partner_repository import PartnerRepository

partner_repository = PartnerRepository()
redis_service = RedisService()
log = get_logger()


class CalculusService:

    def __init__(self):
        self.database = partner_repository
        self.mem_database = redis_service

    def find_nearest(self, location):
        key = f"{location.lat}|{location.long}"

        data_in_mem = self.find_in_memory(key, location)
        if data_in_mem:
            return data_in_mem
        else:
            return self.find_in_db(key, location)

    def find_in_memory(self, key, location):
        result_from_mem = self.mem_database.get_value(key)
        if result_from_mem:
            log.info("[CACHE - calculus] Found in cache...")
            return json.loads(result_from_mem.decode("UTF-8"))
        else:
            log.info("[CACHE - calculus] Not found...")
            return False

    def find_in_db(self, key, location):
        point = [ ("type", "Point"),("coordinates", [location.lat, location.long]) ]
        data_in_db = self.database.find_nearest(point)

        if data_in_db:
            log.info("[DB - calculus] Found in DB...")
            data_in_db = partner_serializer(data_in_db)
            self.store_found_data_in_mem(key, data_in_db)
            return data_in_db
        else:
            log.info("[DB - calculus] Not found...")
            return False

    def store_found_data_in_mem(self, key, data):
        data_to_store = json.dumps(data).encode('utf-8')
        log.info("[CACHE - calculus] Trying to save in cache...")
        self.mem_database.set_value(key, data_to_store)
