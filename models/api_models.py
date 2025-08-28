from pydantic import BaseModel
from typing import Any
from enum import Enum

class Status(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class UserSchema(BaseModel):
    username:str
    password:str

class ResponseSchema(BaseModel):
    status:Status
    content:Any