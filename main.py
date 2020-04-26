from fastapi import FastAPI, Request, HTTPException, Response, Form, status, Query, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Dict
import secrets
from os import environ
from hashlib import sha256
from base64 import b64encode

from fastapi.templating import Jinja2Templates

USERS = "users"
security = HTTPBasic()

app = FastAPI()

hashed_passes = { b64encode("trudnY:PaC13Nt".encode('utf-8')) }
sessions = set()

app.secret_key = "very consta and random secret, best 64 characters" #environ.get("DAFT_SECRET_KEY")

templates = Jinja2Templates(directory="templates")


class HelloResp(BaseModel):
    message: str

class MethodResp(BaseModel):
    method: str

@app.post('/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    passes = b64encode(bytes(username + ':' + password, "utf-8"))

    if passes not in hashed_passes:  #db.smembers(USERS):
        raise HTTPException(status_code=401, detail="Unauthorized") 

    session_token = sha256(bytes(f"{username}{password}{app.secret_key}", 'utf-8')).hexdigest()
    #db.set(session_token, "session will expire in 5 minutes", ex=300)
    sessions.add(session_token)
    response = RedirectResponse(url="/welcome", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_token", value=session_token, expires=300)
    response.headers['Authorization'] = f"Basic {passes}" 
    return response


def if_logged_in(request: Request):
    # session_token = sha256(bytes(f"{username}{password}{app.secret_key}", 'utf-8')).hexdigest()
    print(request.headers)
    if request.headers["authorization"] not in sessions:
        raise HTTPException(status_code=401, detail="Session is dead") 
'''

@app.post('/logout')
def logout(request: Request, response: Response, username: str = Depends(login)):
    print(request.headers)
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("Authorization")
    session = request.cookies["session_token"]
    sessions.remove(session)
    response.delete_cookie("session_token")
    #  if request.headers["authorization"] not in sessions:
    #     raise HTTPException(status_code=401, detail="Session is dead") 

    return response
'''
