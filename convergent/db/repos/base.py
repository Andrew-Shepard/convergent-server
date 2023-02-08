from aiopg.sa import Engine


class BaseRepository:
    def __init__(self, db: Engine) -> None:
        self.db = db
