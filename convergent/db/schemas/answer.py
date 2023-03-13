from convergent.db.schemas.base_model import BaseModel
import sqlalchemy as sa
from datetime import date


class Answer(BaseModel):
    answer_id: str
    date: date
    user_id: str
    answered: bool

    class Config:
        orm_mode = True
