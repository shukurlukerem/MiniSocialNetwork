from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    desc: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    title: str
    desc: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True
