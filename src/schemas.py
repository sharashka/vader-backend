from typing import List
from pydantic import BaseModel, constr


class Parameter(BaseModel):

    id: int
    name: str
    value: str

    class Config:
        orm_mode = True


class GoodBase(BaseModel):
    id: int
    vader_id: constr(max_length=100)
    parameters: List[Parameter]

    class Config:
        orm_mode = True
