from datetime import datetime
from typing import List
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    bdate: Optional[str]
    online: int


class Message(BaseModel):
    id: int
    body: str
    user_id: str
    date: float
    read_state: int
    out: int
    attachments: Optional[list]


