from datetime import datetime

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    memory_type: str
    key: str
    value: str


class MemoryUpdate(BaseModel):
    memory_type: str
    key: str
    value: str


class MemoryResponse(BaseModel):
    id: int
    memory_type: str
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PreferredReminderTime(BaseModel):
    time: str
