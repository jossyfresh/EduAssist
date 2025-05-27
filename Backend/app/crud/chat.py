from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.chat import ChatGroup, GroupMember, Message, MessageRead
from app.schemas.chat import ChatGroupCreate, MessageCreate, MessageReadCreate

def create_chat_group(db: Session, group: ChatGroupCreate, creator_id: str) -> ChatGroup:
    db_group = ChatGroup(
        name=group.name,
        created_by=creator_id
    )
    db.add(db_group)
    db.flush()  # Flush to get the group ID
    
    # Add creator as a member
    member = GroupMember(
        group_id=db_group.id,
        user_id=creator_id
    )
    db.add(member)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_chat_group(db: Session, group_id: int) -> Optional[ChatGroup]:
    return db.query(ChatGroup).filter(ChatGroup.id == group_id).first()

def get_user_groups(db: Session, user_id: str) -> List[ChatGroup]:
    return db.query(ChatGroup).join(GroupMember).filter(GroupMember.user_id == user_id).all()

def add_group_member(db: Session, group_id: int, user_id: str) -> GroupMember:
    member = GroupMember(
        group_id=group_id,
        user_id=user_id
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def remove_group_member(db: Session, group_id: int, user_id: str) -> bool:
    result = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).delete()
    db.commit()
    return result > 0

def create_message(db: Session, message: MessageCreate, sender_id: str) -> Message:
    db_message = Message(
        group_id=message.group_id,
        sender_id=sender_id,
        content=message.content,
        file_url=message.file_url
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_group_messages(
    db: Session,
    group_id: int,
    skip: int = 0,
    limit: int = 50
) -> List[Message]:
    return db.query(Message).filter(
        Message.group_id == group_id
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()

def create_message_read(db: Session, message_read: MessageReadCreate) -> MessageRead:
    db_message_read = MessageRead(**message_read.dict())
    db.add(db_message_read)
    db.commit()
    db.refresh(db_message_read)
    return db_message_read

def get_message_reads(db: Session, message_id: int) -> List[MessageRead]:
    return db.query(MessageRead).filter(MessageRead.message_id == message_id).all()

def search_messages(
    db: Session,
    group_id: int,
    query: str,
    skip: int = 0,
    limit: int = 50
) -> List[Message]:
    return db.query(Message).filter(
        Message.group_id == group_id,
        Message.content.ilike(f"%{query}%")
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all() 