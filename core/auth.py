# lib
from starlette.responses import JSONResponse
from datetime import  datetime
from hashlib import sha256
from orm_db import DB_ORM



# class for auth
class Auth:
    # init
    def __init__(self, db_config: object) -> None:
        # self.db = Mysql_Connect(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])
        self.db_orm = DB_ORM(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])
    
    def Register(self, name: str, surname: str, login: str, password:str, password_confirm:str):
        # check for password
        if (password != password_confirm):
            return JSONResponse({"detail":"Passwords not same"}, 400)
        else:

            if self.db_orm.Register_User(name,surname,login,password):
                return JSONResponse(content={"message":"Created"}, status_code=200)
            else:
                return JSONResponse(content={"detail":"Login not available"},status_code=400)

    def Login(self, login:str, password: str):
        user_id = self.Create_Session(login, password)
        if user_id != -1:

            # create hash
            data_to_hash = "%s%s%s%s" % (login.lower(), password, "key", datetime.now().timestamp())
            hashed_string = sha256(data_to_hash.encode("utf-8")).hexdigest()

            # register token
            self.db_orm.Register_Token(user_id=user_id.id,token=hashed_string)

            # create response
            response = JSONResponse({"message":"Cookies enable"})
            response.set_cookie(key="token", value=hashed_string)
            return response
        else:
            return JSONResponse({"detail":"Login or password not correct"}, 401)

    
    def Create_Session(self, login: str, password: str):
        # create session in db
        db_response = self.db_orm.Check_Credentions(login,password)
        if db_response == None:
            return -1
        else:
            return db_response

    # check for user and return id
    def Get_User_Id(self, token: str):
        if token == None:
            return -1

        return self.db_orm.Get_User_Id(token=token)

    # Check for authorisation
    def Check_Auth(self, token: str):
        # check for token none
        if token == None or token == "":
            return False
        
        return self.db_orm.Check_Token(token)
    

    

