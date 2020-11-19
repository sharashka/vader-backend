from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Good(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, nullable=False)
    vader_id = Column(String(100), index=True, nullable=False)

    parameters = relationship("Parameter", back_populates="good")


class Parameter(Base):
    __tablename__ = "parameters"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    value = Column(String(500), index=True, nullable=False)
    good_id = Column(Integer, ForeignKey("goods.id"))
    good = relationship("Good", back_populates="parameters")
