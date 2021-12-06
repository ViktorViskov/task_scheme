# module for CRUD with task
from starlette.responses import JSONResponse
from core.db import Mysql_Connect
from core.lib import sql_inj_clean

class Task_Controll:
    def __init__(self, db_config: object) -> None:
        self.db = Mysql_Connect(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])

    def Create_Task(self, title: str, description: str, user_id: int):
        self.db.Connect()
        # create task
        task_id = self.db.I("INSERT INTO tasks (title, description) VALUES ('%s','%s')" % (sql_inj_clean(title), sql_inj_clean(description)))

        # create reations
        self.db.I("INSERT INTO user_task_relation (user_id, task_id) VALUES ('%s','%s')" % (user_id, task_id))


        self.db.Close()
        return JSONResponse(content={"message":"Task Created"}, status_code=200)
    
    def Get_All_Tasks(self, user_id: int):
        self.db.Connect()
        tasks = self.db.IO("SELECT tasks.id, tasks.title, tasks.description FROM tasks, user_task_relation WHERE user_task_relation.user_id = %s AND user_task_relation.task_id = tasks.id" % (user_id))
        self.db.Close()
        return tasks
    
    def Delete_Task(self, user_id:int, task_id: int):
        self.db.Connect()
        task_desc = self.db.IO("SELECT user_task_relation.task_id FROM user_task_relation WHERE user_id = '%s' AND task_id = '%s'" % (user_id, task_id))
        if (len(task_desc) > 0):
            task_to_delete = task_desc[0][0]
            # delete from relation
            self.db.I("DELETE FROM user_task_relation WHERE user_id = '%s' AND task_id = '%s'" % (user_id, task_to_delete))

            # delete from tasks
            self.db.I("DELETE FROM tasks WHERE id = '%s'" % (task_to_delete))
            return {"message":"Deleting complete"}
        else:
            return JSONResponse({"detail":"Task not found"}, 400)
