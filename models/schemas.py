from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    sender: str  # "user" or "ai"
    content: str

class ConversationResponse(BaseModel):
    id: int
    title: str
    message_count: int = 0

class ConversationList(BaseModel):
    conversations: List[ConversationResponse]