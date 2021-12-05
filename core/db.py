#
# class for open connection to mysql
#

# libs
from os import error
import mysql.connector


class Mysql_Connect:

    # constructor
    def __init__(self, host, user, password, db):

        self.host = host
        self.user = user
        self.password = password
        self.db = db

    # create connection
    def Connect(self):
        # connection
        self.connection = mysql.connector.connect(
            host=self.host, user=self.user, passwd=self.password, database=self.db)

        # io buffer cursor
        self.cursor = self.connection.cursor()

    # Close connection
    def Close(self):
        self.connection.close()

    # Input (not read server ansver)
    def I(self, sql_command):
        try:
            # exec command
            self.cursor.execute(sql_command)
            self.connection.commit()
            return self.cursor.lastrowid

        except error:
            print(sql_command)
            print(error)
            print("DB connection error")

    # Input and Outpur

    def IO(self, sql_command):
        try:
            # exec command
            self.cursor.execute(sql_command)
            # read result
            return self.cursor.fetchall()
        except:
            print("DB connection error")
            return None
