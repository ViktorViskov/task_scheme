# module for CRUD with task
from core.db import Mysql_Connect
from core.lib import sql_inj_clean

class Task_Controll:
    def __init__(self) -> None:
        self.db = Mysql_Connect("10.0.0.2", "root", "dbnmjr031193", "task_scheme")

    def Create_Task(self, title: str, description: str, user_id: int):
        self.db.Connect()
        # create task
        task_id = self.db.I("INSERT INTO tasks (title, description) VALUES ('%s','%s')" % (sql_inj_clean(title), sql_inj_clean(description)))

        # create reations
        self.db.I("INSERT INTO user_task_relation (user_id, task_id) VALUES ('%s','%s')" % (user_id, task_id))
        