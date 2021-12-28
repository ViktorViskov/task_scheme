# libs
from fastapi import FastAPI, Cookie
from fastapi.param_functions import Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from starlette.responses import JSONResponse
from core.auth import Auth
from core.task_manager import Task_Controll

# web server
web_server = FastAPI()

# static files
web_server.mount("/static", StaticFiles(directory="static"), name="static")

# db config
db_config = {}
db_config["host"] = "10.0.0.2"
db_config["user"] = "root"
db_config["password"] = "dbnmjr031193"
db_config["db_name"] = "task_scheme"

# auth
auth = Auth(db_config)

# task controll
tc = Task_Controll(db_config)

# 
# CORS
# 
web_server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 
# Routes
# 

# VUE js app
@web_server.get("/")
async def main_page():
    return HTMLResponse(content=open("src/index.html").read(),status_code=200)

# register page
@web_server.get("/register")
async def register_page():
    return HTMLResponse(content=open("src/register.html").read(),status_code=200)

# register request
@web_server.post("/register")
async def register_user(name:str = Form(...), surname:str = Form(...), login:str = Form(...) , password: str = Form(...), password_confirm: str = Form(...)):
    return auth.Register(name, surname, login, password, password_confirm)

# login request
@web_server.post("/login")
async def login_user(login:str = Form(...), password:str = Form(...)):
    return auth.Login(login, password)    

# create task
@web_server.post("/create")
async def create_task(token: Optional[str] = Cookie(None), title:str = Form(...), description: str = Form(...), start: str = Form(...), stop: str = Form(...)):
    user_id = auth.Get_User_Id(token)
    if user_id != -1:
        return tc.Create_Task(title, description, user_id, start, stop)
    else:
        return HTMLResponse("Not auth", 401)

# get all tasks
@web_server.get("/tasks")
async def get_tasks(token: Optional[str] = Cookie(None)):
    user_id = auth.Get_User_Id(token)
    if user_id != -1:
        return tc.Get_All_Tasks(user_id)
    else:
        return HTMLResponse("Not auth", 401)

# get tasks from date
@web_server.post("/date_tasks")
async def get_date_tasks(token: Optional[str] = Cookie(None), date_start:str = Form(...), date_stop:str = Form(...)):
    user_id = auth.Get_User_Id(token)
    if user_id != -1:
        return tc.Get_Tasks_From_Date(user_id, date_start, date_stop)
    else:
        return HTMLResponse("Not auth", 401)

# Delete task
@web_server.delete("/delete")
async def delete_task(token: Optional[str] = Cookie(None), task_id :int = Form(...)):
    user_id = auth.Get_User_Id(token)
    if user_id != -1:
        return tc.Delete_Task(user_id, task_id)
    else:
        return HTMLResponse("Not auth", 401)


# panel
@web_server.get("/is_auth")
async def is_auth(token: Optional[str] = Cookie(None)):
    if token != None and auth.Check_Auth(token):
        return JSONResponse({"status":True}, 200)
    else:
        return JSONResponse({"status":False}, 200)
