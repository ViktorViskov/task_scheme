from sqlalchemy import *

class DB_ORM:
    def __init__(self) -> None:
        # create engine
        self.engine = create_engine('sqlite:///sqlite3.db', echo=True)

        # open connection
        self.connection = self.engine.connect()

        # create variable with metadata for db
        self.metadata = MetaData()

        # describe one table
        self.notes = Table("notes", self.metadata, Column("id", Integer(), primary_key=True, autoincrement=True), Column("title", String(32)), Column("text", String(512))) 

    # create table from metadata
    def Create_DataBase(self):
        self.metadata.create_all(self.engine)

    # get data from db
    def Get_All(self):
        result = self.connection.execute(self.notes.select())
        return result.fetchall()

    # get data from db
    def Create_Note(self, title: str, text:str):
        result = self.connection.execute(self.notes.insert().values(title = title, text = text))
        return result.inserted_primary_key


class Note(object):
    def __init__(self, id, title, text) -> None:
        self.id = id
        self.title = title
        self.text = text