from hashlib import sha256
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Depends, Response, status, HTTPException
import secrets
from pydantic import BaseModel

app = FastAPI()
app.ID = 0
app.patients = {}
app.session_tokens = []
app.secret_key = "very constant and random secret, best 64 characters, here it is."

security = HTTPBasic()



@app.post("/login")
def get_current_user(response: Response, user: str, password: str, credentials: HTTPBasicCredentials = Depends(security)):
    check = False
    for user, password in app.secret_key.items():
        check_user = secrets.compare_digest(credentials.user, user)
        check_password = secrets.compare_digest(credentials.password, password)
        if check_user and check_password:
            check = True
    if not check:
        raise HTTPException(status_code = 401, detail = "Unauthorized")
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.session_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND 
