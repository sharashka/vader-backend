from typing import List
from fastapi import FastAPI, File, UploadFile
from xmlparse import parse_xml_string
from sqlalchemy import create_engine
from db import SessionLocal, engine
from fastapi import Depends
from sqlalchemy.orm import Session
import schemas
import models
import goods

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/status")
def status():
    return {"status": "ok"}


@app.post("/api/v1/uploadfiles/")
async def create_upload_files(
    db: Session = Depends(get_db), files: List[UploadFile] = File(...)
):
    # TODO test create - remove

    file = files[0]
    content = file.file.read()
    parsed_results = parse_xml_string(content)
    offers = parsed_results["offers"]
    goods.save_offers_to_db(db, offers)

    return {"filenames": [file.filename for file in files]}


@app.get("/api/v1/offers/")
async def read_offers(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
) -> List[schemas.GoodBase]:
    return goods.read_offers_from_db(db, skip, limit)
