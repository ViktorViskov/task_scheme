# lib
from base64 import encode

from starlette.responses import JSONResponse
from core.db import Mysql_Connect
from datetime import  datetime
from hashlib import sha256



# class for auth
class Auth:
    # init
    def __init__(self, db_config: object) -> None:
        self.db = Mysql_Connect(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])
    
    def Register(self, name: str, surname: str, login: str, password:str, password_confirm:str):
        # check for password
        if (password != password_confirm):
            return JSONResponse({"detail":"Passwords not same"}, 400)
        else:
            # check for user not created 
            result = self.db.O("SELECT id FROM users WHERE login = %s" , login)
            if len(result) == 0:
                password += "Password1!"
                hashed_password = sha256(password.encode("utf-8")).hexdigest()
                self.db.I("INSERT INTO users (name,surname,login,password) VALUES (%s,%s,%s,%s)" , name, surname, login.lower(), hashed_password)
                return JSONResponse(content={"message":"Created"}, status_code=200)
            else:
                return JSONResponse(content={"detail":"Login not awailable"},status_code=400)

    def Login(self, login:str, password: str):
        password += "Password1!"
        hashed_password = sha256(password.encode("utf-8")).hexdigest()
        hash_string = self.Create_Session(login, hashed_password)
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

        db_response = self.db.O("SELECT id FROM users WHERE login = %s AND password = %s" ,login.lower(), password)
        if len(db_response) > 0:
            # get user id
            user_id = db_response[0][0]
            # delete all old session
            self.db.I("DELETE FROM user_sessions WHERE user_id = %s" ,user_id)
            self.db.I("INSERT INTO user_sessions (user_id, token) VALUES (%s,%s)" ,user_id, hashed_string)
            return hashed_string
        else:
            return ""

    # check for user and return id
    def Get_User_Id(self, token: str):
        if token == None:
            return -1
        result = self.db.O("SELECT user_id FROM user_sessions WHERE token = %s" ,token)
        return result[0][0] if len(result) > 0 else -1

    # Check for authorisation
    def Check_Auth(self, token: str):
        # check for token none
        if token == None or token == "":
            return False
        
        # check session
        result = self.db.O("SELECT user_id FROM user_sessions WHERE token = %s" ,token)
        return True if len(result) > 0 else False
    

    

