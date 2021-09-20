from typing import List
from pydantic import BaseModel

from app.models.partner import Partner


class InitialData(BaseModel):
    pdvs: List[Partner]
