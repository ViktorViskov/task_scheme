#
# class for open connection to mysql
#

# libs
import mysql.connector


class Mysql_Connect:

    # constructor
    def __init__(self, host, user, password, db):

        self.host = host
        self.user = user
        self.password = password
        self.db = db

    # Input (not read server answer)
    def I(self, sql_command, *data):
        try:
            # create connection and cursor
            connection = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
            cursor = connection.cursor()

            # exec command and accept changes
            cursor.execute(sql_command, data)
            connection.commit()

            # Last inputed id
            last_id = cursor.lastrowid

            # Close cursor and connection
            cursor.close()
            connection.close()

            return last_id
            
        except:
            print(sql_command)
            print("DB connection error I")
            return None

    # Output read server answer

    def O(self, sql_command, *data):
        try:
            # create connection and cursor
            connection = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.db)
            cursor = connection.cursor()

            # exec command and read result
            cursor.execute(sql_command, data)
            db_response = cursor.fetchall()

            # Close cursor and connection
            cursor.close()
            connection.close()

            return db_response

        except:
            print(sql_command)
            print("DB connection error O")
            return None
