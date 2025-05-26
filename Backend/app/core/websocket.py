from typing import Dict, List
from fastapi import WebSocket
from app.schemas.chat import WebSocketMessage

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.user_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, group_id: int, user_id: str):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append(websocket)
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        self.user_connections[user_id].append(websocket)
    
    async def disconnect(self, websocket: WebSocket, group_id: int, user_id: str):
        if group_id in self.active_connections:
            self.active_connections[group_id].remove(websocket)
            if not self.active_connections[group_id]:
                del self.active_connections[group_id]
        
        if user_id in self.user_connections:
            self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
    
    async def broadcast_to_group(self, message: WebSocketMessage):
        if message.group_id in self.active_connections:
            for connection in self.active_connections[message.group_id]:
                await connection.send_json(message.dict())
    
    async def send_personal_message(self, message: WebSocketMessage, user_id: str):
        if user_id in self.user_connections:
            for connection in self.user_connections[user_id]:
                await connection.send_json(message.dict())
    
    async def broadcast_typing(self, group_id: int, user_id: str, is_typing: bool):
        message = WebSocketMessage(
            type="typing",
            group_id=group_id,
            sender_id=user_id,
            content=str(is_typing)
        )
        await self.broadcast_to_group(message)
    
    async def broadcast_read_receipt(self, group_id: int, user_id: str, message_id: int):
        message = WebSocketMessage(
            type="read",
            group_id=group_id,
            sender_id=user_id,
            content=str(message_id)
        )
        await self.broadcast_to_group(message)

# Create a global instance of the connection manager
manager = ConnectionManager() 