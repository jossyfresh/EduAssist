from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    MESSAGE = "message"
    TYPING = "typing"
    READ = "read"
    FILE = "file"
    INVITE = "invite"

class ChatGroupBase(BaseModel):
    name: str

class ChatGroupCreate(ChatGroupBase):
    pass

class ChatGroup(ChatGroupBase):
    id: int
    created_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class GroupMemberBase(BaseModel):
    group_id: int
    user_id: str

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMember(GroupMemberBase):
    id: int
    joined_at: datetime
    
    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    file_url: Optional[str] = None

class MessageCreate(MessageBase):
    group_id: int

class Message(MessageBase):
    id: int
    group_id: int
    sender_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageReadCreate(BaseModel):
    message_id: int
    user_id: str

class MessageRead(MessageReadCreate):
    id: int
    read_at: datetime
    
    class Config:
        from_attributes = True

class WebSocketMessage(BaseModel):
    type: MessageType
    group_id: int
    sender_id: str
    content: Optional[str] = None
    file_url: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class GroupInvite(BaseModel):
    group_id: int
    invited_user_id: str
    invited_by: str 