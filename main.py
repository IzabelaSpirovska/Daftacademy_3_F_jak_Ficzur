from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, Response, Cookie, status
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from hashlib import sha256
import secrets
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
 
class Patient_Name(BaseModel):
    name: str
    surname: str
 
class Patient_Data(BaseModel):
    id: int
    patient: dict
 
app = FastAPI()
app.ID = 0
app.patients = {}
 
app.secret_key = "very constant and random secret, best 64 characters, here it is."
app.session_tokens = []
templates = Jinja2Templates(directory="templates")

#--- TASK 1 -----------------------------------------------------------
 
@app.get('/')
def hello_world():
    return {'message': 'Hello World during the coronavirus pandemic!'}


@app.get('/welcome')
def hello_world2():
    return {'message': 'Hello World during the coronavirus pandemic vol.2!'}
 
#--- TASK 2 -----------------------------------------------------------
 
@app.post('/login')
def path_login(response: Response, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    Valid_username = secrets.compare_digest(credentials.username, 'trudnY')
    Valid_password = secrets.compare_digest(credentials.password, 'PaC13Nt')
    if not (Valid_username and Valid_password):
        raise HTTPException(status_code=401, detail='Invalid login or password')
    session_token = sha256(bytes(f'{credentials.username}{credentials.password}{app.secret_key}', encoding='utf8')).hexdigest()
    app.session_tokens.append(session_token)
    response.set_cookie(key='session_token', value=session_token)
    response.headers["Location"] = '/welcome'
    response.status_code = status.HTTP_302_FOUND
 
#--- TASK 3 -----------------------------------------------------------
 
 
@app.post('/logout')
def path_logout(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorized')
    app.session_tokens.remove(session_token)
    return RedirectResponse('/')

#--- TASK 4 -----------------------------------------------------------
 
 
@app.get('/welcome')
def path_welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorized')
    return templates.TemplateResponse('item.html', {'request': request, 'user': 'trudnY'})
 
#--- TASK 5 -----------------------------------------------------------
 
 
@app.post('/patient')
def next_patient(response: Response, patient: Patient_Name, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorized')
    if app.ID not in app.patients.keys():
        app.patients[app.ID] = patient.dict()
        app.ID += 1
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = f"/patient/{app.ID-1}"
    response.status_code = status.HTTP_302_FOUND
 
@app.get('/patient')
def get_patients(response: Response, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorised')
    return app.patients
   
 
@app.get('/patient/{id}')
def get_patient_id(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorized')
    response.set_cookie(key='session_token', value=session_token)
    if id in app.patients.keys():
        return app.patients[id]
   
 
@app.delete('/patient/{id}')
def delete_patient(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail='Unathorized')
    app.patients.pop(id, None)     
    response.status_code = status.HTTP_204_NO_CONTENT
