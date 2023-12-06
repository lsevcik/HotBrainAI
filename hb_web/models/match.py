from sqlalchemy import Column, ForeignKey, Identity, Integer, Float
from sqlalchemy.orm import mapped_column
from database import Base


class Match(Base):
    __tablename__ = "matches"
    id = Column("id", Integer, Identity(), primary_key=True)
    user1 = mapped_column(ForeignKey("users.id"))
    user2 = mapped_column(ForeignKey("users.id"))
    score = Column("score", Float)

    def __init__(self, user1=None, user2=None, score=0):
        self.user1 = user1
        self.user2 = user2
        self.score = score

    def __repr__(self):
        return f"<Match {self.id!r}>"
