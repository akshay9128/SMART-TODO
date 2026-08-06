from pydantic import BaseModel,Field

class TaskCreate(BaseModel):
    title:str=Field(
        ...,
        min_lenth=1,
        max_length=200,
        description="Title Of The Task"
    )