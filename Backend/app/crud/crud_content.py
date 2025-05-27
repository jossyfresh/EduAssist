from typing import Any, Dict, Optional, List, Union
from sqlalchemy.orm import Session
from app.models.enums import ContentType
from app.schemas.content import ContentCreate, ContentUpdate
from app.models.content import Content as ContentModel
from uuid import uuid4
import datetime
from app.crud.base import CRUDBase

class ContentCRUD(CRUDBase[ContentModel, ContentCreate, ContentUpdate]):
    def create_text(self, db: Session, *, obj_in: ContentCreate, user_id: str) -> ContentModel:
        db_obj = ContentModel(
            title=obj_in.title,
            content_type=ContentType.TEXT,
            content=obj_in.content,
            meta=obj_in.meta or {},
            description=getattr(obj_in, 'description', None),
            created_by=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_video(self, db: Session, *, obj_in: ContentCreate, user_id: str) -> ContentModel:
        db_obj = ContentModel(
            title=obj_in.title,
            content_type=ContentType.VIDEO,
            content=obj_in.content,
            meta=obj_in.meta or {},
            description=getattr(obj_in, 'description', None),
            created_by=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_file(self, db: Session, *, obj_in: ContentCreate, user_id: str) -> ContentModel:
        db_obj = ContentModel(
            title=obj_in.title,
            content_type=ContentType.FILE,
            content=obj_in.content,
            meta=obj_in.meta or {},
            description=getattr(obj_in, 'description', None),
            created_by=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: str) -> Optional[ContentModel]:
        return db.query(ContentModel).filter(ContentModel.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ContentModel]:
        return db.query(ContentModel).offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: ContentModel, obj_in: Union[ContentUpdate, Dict[str, Any]]
    ) -> ContentModel:
        data = obj_in.dict(exclude_unset=True) if not isinstance(obj_in, dict) else obj_in
        for field in data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, data[field])
        db_obj.updated_at = datetime.datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> ContentModel:
        obj = db.query(ContentModel).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_combined_content(self, db: Session) -> Dict[str, List[ContentModel]]:
        text_content = db.query(ContentModel).filter(ContentModel.content_type == ContentType.TEXT).all()
        video_content = db.query(ContentModel).filter(ContentModel.content_type == ContentType.VIDEO).all()
        file_content = db.query(ContentModel).filter(ContentModel.content_type == ContentType.FILE).all()
        
        return {
            "text": text_content,
            "video": video_content,
            "file": file_content
        }

    def get_youtube_metadata(self, video_url: str) -> Dict[str, str]:
        # This is a stub: Replace with actual YouTube metadata fetching
        return {
            "title": "Sample YouTube Title",
            "description": "Sample YouTube Description",
            "duration": "10:00",
            "thumbnail": "https://example.com/thumbnail.jpg"
        }

    def create_quiz(self, db: Session, parameters: Dict[str, Any], user_id: Any) -> ContentModel:
        db_obj = ContentModel(
            id=str(uuid4()),
            title="Generated Quiz",
            content_type=ContentType.QUIZ,
            content="Quiz content here",
            meta=parameters,
            created_by=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_course(self, db: Session, course_id: str) -> List[ContentModel]:
        """Get all content associated with a course."""
        return db.query(ContentModel).filter(ContentModel.course_id == course_id).all()

crud_content = ContentCRUD(ContentModel) 