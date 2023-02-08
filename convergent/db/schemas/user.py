from convergent.db.schemas.base_model import BaseModel
import datetime


class User(BaseModel):
    user_id: str

    class Config:
        orm_mode = True
