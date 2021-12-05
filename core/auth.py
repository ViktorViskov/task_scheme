# lib
from base64 import encode

from starlette.responses import HTMLResponse, JSONResponse
from core.db import Mysql_Connect
from core.lib import sql_inj_clean
from datetime import  datetime
from hashlib import sha256



# class for auth
class Auth:
    # init
    def __init__(self) -> None:
        self.db = Mysql_Connect("10.0.0.2", "root", "dbnmjr031193", "task_scheme")
    
    def Register(self, name: str, surname: str, login: str, password:str, password_confirm:str):
        # check for password
        if (password != password_confirm):
            return JSONResponse({"detail":"Passwords not same"}, 400)
        else:
            # connect to db
            self.db.Connect()
            # check for user not created 
            result = self.db.IO("SELECT id FROM users WHERE login = '%s'" % sql_inj_clean(login))
            if len(result) == 0:
                self.db.I("INSERT INTO users (name,surname,login,password) VALUES ('%s','%s','%s','%s');" % (sql_inj_clean(name), sql_inj_clean(surname), sql_inj_clean(login.lower()), sql_inj_clean(password)))
                self.db.Close()
                return JSONResponse(content={"message":"Created"}, status_code=200)
            else:
                self.db.Close()
                return JSONResponse(content={"detail":"Login not awailable"},status_code=400)

    def Login(self, login:str, password: str):
        hash_string = self.Create_Session(login, password)
        if hash_string != "":
            response = JSONResponse({"message":"Cookies enable"})
            response.set_cookie(key="token", value=hash_string)
            return response
        else:
            return JSONResponse({"detail":"Login or password not correct"}, 401)

    
    def Create_Session(self, login: str, password: str):
        # create str to hash
        data_to_hash = "%s%s%s%s" % (login.lower(), password, "key", datetime.now().timestamp())
        hashed_string = sha256(data_to_hash.encode("utf-8")).hexdigest()

        # create session in db
        self.db.Connect()
        db_response = self.db.IO("SELECT id FROM users WHERE login = '%s' AND password = '%s'" % (login.lower(), password))
        if len(db_response) > 0:
            # get user id
            user_id = db_response[0][0]
            # delete all old session
            self.db.I("DELETE FROM user_sessions WHERE user_id = '%s'" % (user_id))
            self.db.I("INSERT INTO user_sessions (user_id, token) VALUES ('%s','%s')" % (user_id, hashed_string))
            self.db.Close()
            return hashed_string
        else:
            return ""

    # check for user and return id
    def Get_User_Id(self, token: str):
        self.db.Connect()
        result = self.db.IO("SELECT user_id FROM user_sessions WHERE token = '%s'" % (sql_inj_clean(token)))
        self.db.Close()
        return result[0][0] if len(result) > 0 else -1

    # Check for authorisation
    def Check_Auth(self, token: str):
        # check for token none
        if token == None:
            return False
        
        # check session
        self.db.Connect()
        result = self.db.IO("SELECT user_id FROM user_sessions WHERE token = '%s'" % (sql_inj_clean(token)))
        self.db.Close()
        return True if len(result) > 0 else False
    

    

