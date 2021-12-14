from sqlalchemy import *
from sqlalchemy.sql.functions import current_timestamp


class DB_ORM:
    def __init__(self, host:str, user:str, password:str, db_name:str) -> None:
        # create engine
        # self.engine = create_engine('sqlite:///sqlite3.db', echo=True)
        # self.engine = create_engine('mysql+pymysql://root:dbnmjr031193@10.0.0.2/task_scheme_orm')
        self.engine = create_engine('mysql+pymysql://%s:%s@%s/%s' % (user,password, host, db_name))

        # create variable with metadata for db
        self.metadata = MetaData()

        # describe one table
        self.tasks = Table("tasks", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("title", String(64)), Column("description", String(512)), Column("start", DateTime(), default=current_timestamp())), Column("stop", DateTime())
        self.users = Table("users", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("name", String(64)), Column("surname", String(64)), Column("login", String(64), unique=True), Column("password", String(64)))
        self.user_sessions = Table("user_sessions", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("user_id", Integer(), ForeignKey('users.id')), Column("token", String(64)))
        self.user_task_relation = Table("user_task_relation", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("user_id", Integer(), ForeignKey('users.id')), Column("task_id", Integer(), ForeignKey("tasks.id")))

    # create table from metadata
    def Create_DataBase(self):
        # open connection
        self.connection = self.engine.connect()

        # request to create tables
        self.metadata.create_all(self.engine)

        # close connection
        self.connection.close()

    # Create user in db
    def Register_User(self, name: str, surname: str, login: str, password:str):
        # open connection
        connection = self.engine.connect()

        # preprocess login
        login = login.lower()

        # check for login is available and create
        data = connection.execute(self.users.select().where(self.users.c.login == login)).fetchone()
        if data == None:
            connection.execute(self.users.insert().values(name=name,surname=surname,login=login,password=password))
            return True
        else:
            return False

    # Check user credentions
    def Check_Credentions(self, login: str, password: str):
        # open connection
        connection = self.engine.connect()

        # request to get data
        result = connection.execute(self.users.select().where(and_(self.users.c.login == login.lower(), self.users.c.password == password)))
        result = result.fetchone()

        # close connection
        connection.close()

        return result

    # check user auth token
    def Check_Token(self, token: str):
        # open connection
        connection = self.engine.connect()

        # request to get data
        result = connection.execute(self.user_sessions.select().where(self.user_sessions.c.token == token)).fetchone()

        # close connection
        connection.close()

        return False if result == None else True

    # Method for register session token
    def Register_Token(self, user_id:int, token:str):
        # open connection
        connection = self.engine.connect()

        # delete all old users tokens
        connection.execute(self.user_sessions.delete().where(self.user_sessions.c.user_id == user_id))

        # create new token
        connection.execute(self.user_sessions.insert().values(user_id=user_id,token=token))

        # close connection
        connection.close()

    # Get user id
    def Get_User_Id(self, token:str):
        # open connection
        connection = self.engine.connect()

        # request to get data
        result = connection.execute(self.user_sessions.select().where(self.user_sessions.c.token == token)).fetchone()

        # close connection
        connection.close()
        print(result)

        return result.user_id if result != None else -1


class Note(object):
    def __init__(self, id, title, text) -> None:
        self.id = id
        self.title = title
        self.text = text
