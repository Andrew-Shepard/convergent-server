from convergent.db.schemas.base_model import BaseModel
import datetime


class Answer(BaseModel):
    user_id: str
    answered: bool

    class Config:
        orm_mode = True
