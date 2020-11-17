from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import schemas

import db
import auth

import initdb

app = FastAPI()


@app.get("/")
def index():
    return {"main": "ok"}

@app.get("/status")
def status():
    return {"status": "ok2"}

@app.get('/api/v1/auth/')
async def auth1():
    return db.test2()

@app.get('/api/v1/dbtest/')
async def dbtest():
    return db.testdb()

@app.get('/api/v1/getUserEmail/{userName}')
async def getUserEmail(userName: str):
    answer = db.getUserEmail(userName)
    if answer is None:
        output = {'Username': userName,
                'Email': '',
                'Failure': 'User not exist.'}
    else:
        output = {'Username': userName,
                'Email': answer[0],
                'Success': 'ok'}
    return output

@app.post('/api/v1/register/')
async def register_new_user(user: schemas.User):
    response = db.register_new_user(user)
    return response



@app.post("/api/v1/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/api/v1/users/me")
async def read_users_me(current_user: auth.User = Depends(auth.get_current_active_user)):
    return current_user

