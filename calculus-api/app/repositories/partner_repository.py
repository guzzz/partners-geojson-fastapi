from structlog import get_logger

from app.config.db import mongoclient
from bson.son import SON

log = get_logger()


class PartnerRepository:

    def __init__(self):
        database = mongoclient.local
        self._partners = database.partners

    def find_nearest(self, location):
        result = self._partners.find_one(
            { "$and" : 
                [
                    { "coverageArea": SON([("$geoIntersects",  { "$geometry" : SON(location)})])},
                    { "address": SON([("$nearSphere",  { "$geometry" : SON(location) })])}
                ]
            }
        )
        return result

    def create(self, partner):
        log.info("[DB] Creating PARTNER...")
        return self._partners.insert_one(partner)

    def delete(self, id):
        log.info(f"[DB] Deleting USER: {id}")
        return self._partners.find_one_and_delete({"id": id})
