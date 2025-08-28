from pydantic import BaseModel
from typing import List
class Chat(BaseModel):
    role:str
    content:str

class GeminiChatModel(BaseModel):
    messages:List[Chat]


chat = Chat(role = "user", content="Who is pablo escobar?")
messages = GeminiChatModel(messages=[chat])
