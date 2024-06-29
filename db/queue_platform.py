from sqlalchemy import Column, Integer

from db.base import Base


class Queue_platform(Base):
    __tablename__ = "queue_platform"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    service = Column(Integer)