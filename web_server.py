# libs
from fastapi import FastAPI, Cookie
from fastapi.param_functions import Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Optional
from core.auth import Auth
from core.lib import *
from core.task_manager import Task_Controll

# web server
web_server = FastAPI()

# static files
web_server.mount("/static", StaticFiles(directory="static"), name="static")

# auth
auth = Auth()

# task controll
tc = Task_Controll()

# 
# Routes
# 

# main page
@web_server.get("/")
async def main_page():
    return HTMLResponse(content=open("src/index.html").read(),status_code=200)

# register page
@web_server.get("/register")
async def register_page():
    return HTMLResponse(content=open("src/register.html").read(),status_code=200)

@web_server.post("/register")
async def register_user(name:str = Form(...), surname:str = Form(...), login:str = Form(...) , password: str = Form(...), password_confirm: str = Form(...)):
    return auth.Register(name, surname, login, password, password_confirm)

# login page
@web_server.get("/login")
async def login_page():
    return HTMLResponse(content=open("src/login.html").read(),status_code=200)

@web_server.get("/create")
async def create_page():
    return HTMLResponse(content=open("src/task_create.html").read(),status_code=200)
    

# create task
@web_server.post("/create")
async def create_task(token: Optional[str] = Cookie(None), title:str = Form(...), description: str = Form(...)):
    user_id = auth.Get_User_Id(token)
    if user_id != -1:
        return tc.Create_Task(title, description, user_id)
    else:
        return HTMLResponse("Not auth", 401)


# panel
@web_server.get("/panel")
async def user_panel(token: Optional[str] = Cookie(None)):
    if token != None or auth.Check_Auth(token):
        return HTMLResponse("Auth", 200)
    else:
        return HTMLResponse("Not auth", 401)
