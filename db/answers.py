from sqlalchemy import Column, String

from db.base import Base


class Answers(Base):
    __tablename__ = "answers"
    __table_args__ = {"extend_existing": True}

    command = Column(String(length=50), primary_key=True, index=True)
    message = Column(String(length=3000), nullable=True)
    photo_id = Column(String(500))
    file_id = Column(String(500))
