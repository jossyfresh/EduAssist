from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from sqlalchemy.orm import Session
import os
from app.api import deps
from app.crud import chat as chat_crud
from app.schemas.chat import (
    ChatGroupCreate,
    ChatGroup,
    MessageCreate,
    Message,
    MessageReadCreate,
    MessageRead
)
from app.core.websocket import ConnectionManager
from app.models.user import User
import aiofiles
from datetime import datetime

router = APIRouter()
manager = ConnectionManager()

# File upload configuration
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/groups", response_model=ChatGroup)
def create_group(
    group: ChatGroupCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Create a new chat group"""
    try:
        db_group = chat_crud.create_chat_group(db, group, current_user.email)
        return {
            "id": db_group.id,
            "name": db_group.name,
            "created_by": db_group.created_by,
            "created_at": db_group.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/groups", response_model=List[ChatGroup])
def get_groups(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get all chat groups for the current user"""
    groups = chat_crud.get_user_groups(db, current_user.email)
    return [
        {
            "id": group.id,
            "name": group.name,
            "created_by": group.created_by,
            "created_at": group.created_at
        }
        for group in groups
    ]

@router.get("/groups/{group_id}", response_model=ChatGroup)
def get_group(
    group_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a specific chat group"""
    group = chat_crud.get_chat_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return {
        "id": group.id,
        "name": group.name,
        "created_by": group.created_by,
        "created_at": group.created_at
    }

@router.post("/groups/{group_id}/members/{user_id}", response_model=dict)
def add_member(
    group_id: int,
    user_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Add a member to a chat group"""
    group = chat_crud.get_chat_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if group.created_by != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to add members")
    chat_crud.add_group_member(db, group_id, user_id)
    return {"message": "Member added successfully"}

@router.delete("/groups/{group_id}/members/{user_id}", response_model=dict)
def remove_member(
    group_id: int,
    user_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Remove a member from a chat group"""
    group = chat_crud.get_chat_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if group.created_by != current_user.email and user_id != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to remove members")
    success = chat_crud.remove_group_member(db, group_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member removed successfully"}

@router.post("/messages", response_model=Message)
def create_message(
    message: MessageCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Create a new message"""
    db_message = chat_crud.create_message(db, message, current_user.email)
    return {
        "id": db_message.id,
        "group_id": db_message.group_id,
        "sender_id": db_message.sender_id,
        "content": db_message.content,
        "file_url": db_message.file_url,
        "created_at": db_message.created_at
    }

@router.get("/groups/{group_id}/messages", response_model=List[Message])
def get_messages(
    group_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get messages for a chat group"""
    messages = chat_crud.get_group_messages(db, group_id, skip, limit)
    return [
        {
            "id": msg.id,
            "group_id": msg.group_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "file_url": msg.file_url,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@router.post("/messages/{message_id}/read", response_model=MessageRead)
def mark_message_read(
    message_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Mark a message as read"""
    message_read = MessageReadCreate(
        message_id=message_id,
        user_id=current_user.email
    )
    db_message_read = chat_crud.create_message_read(db, message_read)
    return {
        "id": db_message_read.id,
        "message_id": db_message_read.message_id,
        "user_id": db_message_read.user_id,
        "read_at": db_message_read.read_at
    }

@router.get("/messages/{message_id}/reads", response_model=List[MessageRead])
def get_message_reads(
    message_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get read receipts for a message"""
    reads = chat_crud.get_message_reads(db, message_id)
    return [
        {
            "id": read.id,
            "message_id": read.message_id,
            "user_id": read.user_id,
            "read_at": read.read_at
        }
        for read in reads
    ]

@router.get("/groups/{group_id}/search", response_model=List[Message])
def search_messages(
    group_id: int,
    query: str,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Search messages in a chat group"""
    messages = chat_crud.search_messages(db, group_id, query, skip, limit)
    return [
        {
            "id": msg.id,
            "group_id": msg.group_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "file_url": msg.file_url,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@router.websocket("/ws/{group_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    group_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    await manager.connect(websocket, group_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = MessageCreate(
                group_id=group_id,
                content=data
            )
            db_message = chat_crud.create_message(db, message, current_user.email)
            await manager.broadcast(
                group_id,
                {
                    "type": "message",
                    "data": {
                        "id": db_message.id,
                        "content": db_message.content,
                        "sender_id": db_message.sender_id,
                        "created_at": db_message.created_at.isoformat()
                    }
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id)

# File upload endpoint
@router.post("/groups/{group_id}/files")
async def upload_file(
    group_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
    
    # Reset file pointer
    await file.seek(0)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as out_file:
        while chunk := await file.read(chunk_size):
            await out_file.write(chunk)
    
    # Create message with file URL
    message = MessageCreate(
        group_id=group_id,
        content=f"Shared file: {file.filename}",
        file_url=f"/uploads/{filename}"
    )
    db_message = chat_crud.create_message(db, message, current_user.email)
    return {
        "id": db_message.id,
        "group_id": db_message.group_id,
        "sender_id": db_message.sender_id,
        "content": db_message.content,
        "file_url": db_message.file_url,
        "created_at": db_message.created_at
    } 