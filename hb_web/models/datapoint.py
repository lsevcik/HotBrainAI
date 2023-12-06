from sqlalchemy import Column, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import mapped_column
from database import Base


class DataPoint(Base):
    __tablename__ = "datapoints"
    id = Column("id", Integer, Identity(), primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"))
    video_slug = Column(String)
    sample_no = Column(Integer)
    O1 = Column(Integer)
    O2 = Column(Integer)
    T3 = Column(Integer)
    T4 = Column(Integer)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<DataPoint {self.id!r}>"