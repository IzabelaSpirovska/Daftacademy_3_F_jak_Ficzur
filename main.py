from fastapi import FastAPI, Response, Request, HTTPException, Depends, Cookie
from hashlib import sha256
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.num = 0
app.count = 0
app.users = {"trudnY": "PaC13Nt", "admin": "admin"}
app.secret = "secret"
app.tokens = []
patlist = []

template = Jinja2Templates(directory="templates")

@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_to_the_jungle(request: Request, s_token = Cookie(None)):
	if s_token not in app.tokens:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	return template.TemplateResponse("template1.html", {"request": request, "user": "trudnY"})


@app.post("/login")
def login_to_app(response: Response, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
	if credentials.username in app.users and credentials.password == app.users[credentials.username]:
		s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret}", encoding='utf8')).hexdigest()
		response.set_cookie(key="session_token", value=s_token)
		app.tokens.append(s_token)
		response.status_code = 307
		response.headers['Location'] = "/welcome"
		RedirectResponse(url='/welcome')
		return response
	else:
		raise HTTPException(status_code=401, detail="Niepoprawny login lub hasło")


@app.post("/logout")
def byebye(response: Response):
	response.delete_cookie(key="session_token",path="/")
	response.status_code = 307
	RedirectResponse(url='/')
	response.headers['Location'] = "/"
	return response
