from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Good, Parameter
from schemas import GoodBase

Base = declarative_base()

# TODO make it working with Pydantic models not dicts
def save_offers_to_db(db, offers: List[dict]):
    # TODO make versions for offers (probably by date)
    for offer in offers:
        vader_id = offer["vader_id"]
        good_orm = Good(vader_id=vader_id)
        parameters = [
            Parameter(good=good_orm, name=name, value=value)
            for name, value in offer["params"].items()
        ]
        good_orm.parameters = parameters
        db.add(good_orm)
    db.commit()


def read_offers_from_db(db, skip, limit) -> List[GoodBase]:
    db_offers = db.query(Good).offset(skip).limit(limit).all()
    return [GoodBase.from_orm(db_offer) for db_offer in db_offers]
