from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    username: str
    name: str
    email: str
    password: str
    phone: str
    created_date: date
