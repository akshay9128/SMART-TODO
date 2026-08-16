from pydantic import BaseModel
class AgentRequest(BaseModel):
    text:str
    confirmed:bool=False

class AgentResponse(BaseModel):
    success:bool
    action:str
    message:str
    task_id:int|None=None