from convergent.db.schemas.base_model import BaseModel


class Bible(BaseModel):
    Book: int = None
    Chapter: int = None
    Versecount: int = None
    verse: str = None

    class Config:
        orm_mode = True
