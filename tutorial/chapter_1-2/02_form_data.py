from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="tutorial_app/static"), name="static")


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
