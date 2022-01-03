from typing import cast
from pydantic import BaseModel
from datetime import  datetime, timedelta

from starlette.responses import JSONResponse

# Model for Task
class Task(BaseModel):
    id: int
    title: str
    desc: str
    start: datetime
    stop: datetime

    def from_array(values):
        root_obj = Task(id = values[0], title = values[1], desc = values[2], start = values[3],stop = values[4])
        return root_obj