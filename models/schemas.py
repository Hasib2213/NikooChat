from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"

class MessageCreate(BaseModel):
    """Schema for creating a message"""
    content: str = Field(..., min_length=1, max_length=5000)
    
    class Config:
        example = {"content": "What are the app features?"}

class MessageResponse(BaseModel):
    """Schema for message response"""
    sender: str  # "user" or "ai"
    content: str

class MessageDetail(BaseModel):
    """Detailed message schema with ID"""
    id: int
    sender: str
    content: str

class ConversationResponse(BaseModel):
    """Schema for conversation in list"""
    id: int
    title: str
    message_count: int = 0

class ConversationList(BaseModel):
    """Schema for list of conversations"""
    conversations: List[ConversationResponse]