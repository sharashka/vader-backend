from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, constr

Base = declarative_base()


class GoodsOrm(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, nullable=False)
    vader_id = Column(String(100), index=True, nullable=False)


class GoodsModel(BaseModel):
    id: int
    vader_id: constr(max_length=100)

    class Config:
        orm_mode = True


def init_db(engine):
    GoodsOrm.__table__.create(engine)


# TODO make it working with Pydantic models not dicts
def save_offers_to_db(engine, offers):
    # TODO make versions for offers (probably by date)
    Session = sessionmaker(bind=engine)
    session = Session()

    for offer in offers:
        vader_id = offer["top_level"]["vader_id"]
        good_orm = GoodsOrm(vader_id=vader_id)
        session.add(good_orm)

    session.commit()


def read_offers_from_db(engine) -> List[GoodsModel]:
    Session = sessionmaker(bind=engine)
    session = Session()

    db_offers = session.query(GoodsOrm).all()

    return [GoodsModel.from_orm(db_offer) for db_offer in db_offers]
