from fastapi import FastAPI, Cookie, Response, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256 

app = FastAPI()
app.secret_key = {"trudnY": "PaC13Nt"}
security = HTTPBasic()

#------------------------------------------------------------------------------------------------------------------------------------------
#Zad.1.

@app.get('/')
def hello_world():
    return{"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome_app():
    return{"message": "Welcome to my app."}

#------------------------------------------------------------------------------------------------------------------------------------------
#Zad.2.

def check_cookie(session_token: str = Cookie(None)):
    if session_token not in app.tokens:
        session_token = None
    return session_token

@app.post('/login')
def log_on(user: str, password: str, credentials: HTTPBasicCredentials = Depends(security)):
    check = False
    for user, password in app.secret_key.items():
        check_user = secrets.compare_digest(credentials.user, user)
        check_password = secrets.compare_digest(credentials.password, password)
        if check_user and check_password:
            check = True
    if not check:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    
    session_token = sha256(bytes(f"{credentials.user}{credentials.password}{app.secret_key}")).hexdigest() 
    sessions.add(session_token)
    response = RedirectResponse(url = '/welcome', status_code = status.HTTP_302_FOUND)
    response.set_cookie(key="session_token", value = session_token)
    response.headers['Authorization'] = f"Basic {passes}" 
    return response


