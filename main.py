from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return{"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome_app():
    return{"message": "Welcome to my app."}
