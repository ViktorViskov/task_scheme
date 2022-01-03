# lib
import jwt
from starlette.responses import JSONResponse
from core.db import Mysql_Connect
from datetime import  date, datetime
from hashlib import sha256



# class for auth
class Auth:
    # init
    def __init__(self, db_config: object) -> None:
        # variables
        self.token_secret = ".sufKwpF3vAH-4Xv1KLc1wVefQzfqj18Wi83vXK6TeiM'½"
        self.additional_password_str = "Password1!"
        self.additional_hashing_str = "key"
        self.session_period = 3600 * 12 # session period in sec (default 12 hours)

        # init modules
        self.db = Mysql_Connect(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])
    
    def Register(self, name: str, surname: str, login: str, password:str, password_confirm:str):
        # check for password
        if (password != password_confirm):
            return JSONResponse({"detail":"Passwords not same"}, 400)
        else:
            # check for user not created 
            result = self.db.O("SELECT id FROM users WHERE login = %s" , login)
            if len(result) == 0:
                password += self.additional_password_str
                hashed_password = sha256(password.encode("utf-8")).hexdigest()
                self.db.I("INSERT INTO users (name,surname,login,password) VALUES (%s,%s,%s,%s)" , name, surname, login.lower(), hashed_password)
                return JSONResponse(content={"message":"Created"}, status_code=200)
            else:
                return JSONResponse(content={"detail":"Login not awailable"},status_code=400)

    def Login(self, login:str, password: str):
        password += self.additional_password_str
        hashed_password = sha256(password.encode("utf-8")).hexdigest()
        jsw_token = self.Create_Session(login, hashed_password).decode("UTF-8")
        if jsw_token != "":
            response = JSONResponse({"message":"Cookies enable"})
            response.set_cookie(key="token", value=jsw_token, expires= self.session_period,)
            return response
        else:
            return JSONResponse({"detail":"Login or password not correct"}, 401)

    def Create_Session(self, login: str, password: str):
        # create str to hash
        data_to_hash = "%s%s%s" % (login.lower(), password, self.additional_hashing_str)
        hashed_string = sha256(data_to_hash.encode("utf-8")).hexdigest()
        token_data = {
            "token" : hashed_string,
            "exp_date": int(datetime.now().timestamp() + self.session_period)
        }
        jwt_token = jwt.encode(token_data, self.token_secret, algorithm='HS256')

        db_response = self.db.O("SELECT id FROM users WHERE login = %s AND password = %s" ,login.lower(), password)
        if len(db_response) > 0:
            # get user id
            user_id = db_response[0][0]

            self.Check_Tokens(user_id)
            
            # create session record
            self.db.I("INSERT INTO user_sessions (user_id, token) VALUES (%s,%s)" ,user_id, jwt_token)
            return jwt_token
        else:
            return b''
    

    # check for user and return id
    def Get_User_Id(self, token: str):
        if token == None or token == "" or (not self.Check_Token(token)):
            return -1

        result = self.db.O("SELECT user_id FROM user_sessions WHERE token = %s" ,token)
        return result[0][0] if len(result) > 0 else -1

    # Check for authorisation
    def Check_Auth(self, token: str):
        # check for token none
        if token == None or token == "" or not self.Check_Token(token):
            return False
        
        # check session
        result = self.db.O("SELECT user_id FROM user_sessions WHERE token = %s" ,token)
        return True if len(result) > 0 else False

    # Check one token logick
    def Check_Token(self, token:str, timestamp: int = int(datetime.now().timestamp())):
        try:
            token_data = jwt.decode(token, self.token_secret, algorithms=['HS256'])
            if (token_data["exp_date"] < timestamp):
                # delete token
                self.Delete_Token(token)
                return False

            else:
                return True
        
        # token corrupt
        except:
            return False

    # Check all users tokens and delete with expiried date
    def Check_Tokens(self, user_id:int):
        current_timestamp = int(datetime.now().timestamp())
        tokens = self.db.O("SELECT token FROM user_sessions WHERE user_id = %s" ,user_id)
        for token in tokens:
            token_data = jwt.decode(token[0], self.token_secret, algorithms=['HS256'])
            if (token_data["exp_date"] < current_timestamp):
                # delete token
                self.Delete_Token(token[0])
    
    # Delete token from db
    def Delete_Token(self, token:str):
        self.db.I("DELETE FROM user_sessions WHERE token = %s" , token)        
    

    

