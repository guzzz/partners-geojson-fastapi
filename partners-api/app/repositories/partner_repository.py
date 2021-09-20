from pymongo.errors import InvalidId, DuplicateKeyError
from structlog import get_logger

from app.config.db import mongoclient

log = get_logger()


class PartnerRepository:

    def __init__(self):
        database = mongoclient.local
        self._partners = database.partners

    def retrieve(self, id, uuid=True):
        try:
            log.info("[DB] Searching PARTNER...")
            if uuid:
                return self._partners.find_one({"id": id})
            else:
                return self._partners.find_one({"_id": id})
        except InvalidId:
            log.info("[DB] Invalid ID")
            return False

    def list(self, page, limit):
        log.info(f"[DB] Listing PARTNER page {page}, page_size: {limit}.")
        to_start = (page-1)*limit
        return self._partners.find().skip(to_start).limit(limit)

    def create(self, partner):
        log.info("[DB] Creating PARTNER...")
        try:
            return self._partners.insert_one(partner)
        except DuplicateKeyError:
            log.info("[DB] Document is an UNIQUE field!")
            return False

    def delete(self, id):
        log.info(f"[DB] Deleting USER: {id}")
        return self._partners.find_one_and_delete({"id": id})
