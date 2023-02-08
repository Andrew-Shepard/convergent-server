from convergent.db.schemas.base_model import BaseModel
import datetime


class Question(BaseModel):
    date: datetime.date
    question: str

    class Config:
        orm_mode = True
