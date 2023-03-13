from convergent.db.schemas.base_model import BaseModel
import datetime
from typing import Optional


class User(BaseModel):
    user_id: str
    password: Optional[str]
    partner_id: Optional[str]

    class Config:
        orm_mode = True
