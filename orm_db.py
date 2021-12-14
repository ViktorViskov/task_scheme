from sqlalchemy import *
from sqlalchemy.sql.functions import current_timestamp


class DB_ORM:
    def __init__(self) -> None:
        # create engine
        # self.engine = create_engine('sqlite:///sqlite3.db', echo=True)

        self.engine = create_engine('mysql+pymysql://root:dbnmjr031193@10.0.0.2/task_scheme_orm')
        # open connection
        self.connection = self.engine.connect()

        # create variable with metadata for db
        self.metadata = MetaData()

        # describe one table
        self.tasks = Table("tasks", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("title", String(64)), Column("description", String(512)), Column("start", DateTime(), default=current_timestamp())), Column("stop", DateTime())
        self.users = Table("users", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("name", String(64)), Column("surname", String(64)), Column("login", String(64), unique=True), Column("password", String(64)))
        self.user_sessions = Table("user_sessions", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("user_id", Integer(), ForeignKey('users.id')), Column("token", String(64)))
        self.user_task_relation = Table("user_task_relation", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("user_id", Integer(), ForeignKey('users.id')), Column("task_id", Integer(), ForeignKey("tasks.id")))

    # create table from metadata
    def Create_DataBase(self):
        self.metadata.create_all(self.engine)

    # get data from db
    def Get_All(self):
        result = self.connection.execute(self.notes.select())
        return result.fetchall()

    # get data from db
    def Create_Note(self, title: str, text: str):
        result = self.connection.execute(
            self.notes.insert().values(title=title, text=text))
        return result.inserted_primary_key


class Note(object):
    def __init__(self, id, title, text) -> None:
        self.id = id
        self.title = title
        self.text = text
