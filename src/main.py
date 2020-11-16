from typing import List
from fastapi import FastAPI, File, UploadFile
import bs4
import pdb
from xmlparse import parse_xml_string
import goods as goods
from sqlalchemy import create_engine

app = FastAPI()
engine = create_engine("sqlite:///:memory:", echo=True)


@app.get("/api/v1/status")
def status():
    return {"status": "ok"}


@app.post("/api/v1/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    # TODO test create - remove
    goods.init_db(engine)

    file = files[0]
    content = file.file.read()
    parsed_results = parse_xml_string(content)
    offers = parsed_results["offers"]
    goods.save_offers_to_db(engine, offers)

    return {"filenames": [file.filename for file in files]}


@app.get("/api/v1/offers/")
async def read_offers() -> List[goods.GoodsModel]:
    return goods.read_offers_from_db(engine)
