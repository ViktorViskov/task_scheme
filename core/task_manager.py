# module for CRUD with task
from starlette.responses import JSONResponse
from core.db import Mysql_Connect

class Task_Controll:
    def __init__(self, db_config: object) -> None:
        self.db = Mysql_Connect(db_config["host"], db_config["user"], db_config["password"], db_config["db_name"])

    def Create_Task(self, title: str, description: str, user_id: int, start :str, stop: str):
        # create task
        task_id = self.db.I("INSERT INTO tasks (title, description, start, stop) VALUES (%s,%s,%s,%s)", title, description, start, stop)

        # create reations
        self.db.I("INSERT INTO user_task_relation (user_id, task_id) VALUES (%s,%s)" , user_id, task_id)

        return JSONResponse(content={"message":"Task Created"}, status_code=200)
    
    def Get_All_Tasks(self, user_id: int):
        tasks = self.db.O("SELECT tasks.id, tasks.title, tasks.description, tasks.start, tasks.stop FROM tasks, user_task_relation WHERE user_task_relation.user_id = %s AND user_task_relation.task_id = tasks.id", user_id)
        return tasks
    
    def Delete_Task(self, user_id:int, task_id: int):
        task_desc = self.db.O("SELECT user_task_relation.task_id FROM user_task_relation WHERE user_id = %s AND task_id = %s" , user_id, task_id)
        if (len(task_desc) > 0):
            task_to_delete = task_desc[0][0]
            # delete from relation
            self.db.I("DELETE FROM user_task_relation WHERE user_id = %s AND task_id = %s" ,user_id, task_to_delete)

            # delete from tasks
            self.db.I("DELETE FROM tasks WHERE id = %s" , task_to_delete)
            return {"message":"Deleting complete"}
        else:
            return JSONResponse({"detail":"Task not found"}, 400)
