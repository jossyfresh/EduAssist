from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get multiple records."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, created_by: Optional[UUID] = None) -> ModelType:
        """Create a new record."""
        obj_in_data = obj_in.model_dump()
        if created_by:
            obj_in_data["created_by"] = created_by
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, id: UUID, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        """Update a record."""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> bool:
        """Delete a record."""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return False
        db.delete(db_obj)
        db.commit()
        return True 