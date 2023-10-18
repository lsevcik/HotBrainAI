from sqlalchemy import Column, Identity, Integer
from database import Base


class Result(Base):
    __tablename__ = "results"
    id = Column("id", Integer, Identity(), primary_key=True)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Result {self.id!r}>"