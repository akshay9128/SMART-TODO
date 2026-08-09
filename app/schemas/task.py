from pydantic import BaseModel,Field,ConfigDict
from typing import Literal

class TaskCreate(BaseModel):
    title:str=Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title Of The Task"
    )
    category:str =Field(
            default="General",
            min_length=1,
            max_length=50,
            description="Category Of The Task")
    priority: Literal["low","medium","high"]="medium"

class TaskUpdate(BaseModel):
    title:str | None=None
    completed:bool | None=None
    category:str =Field(
        default="General",
        min_length=1,
        max_length=50
    )
    priority: Literal["low","medium","high"]="medium"

class TaskResponse(BaseModel):
    id:int
    title:str
    completed:bool
    category:str
    priority:str

    model_config=ConfigDict(from_attributes=True)