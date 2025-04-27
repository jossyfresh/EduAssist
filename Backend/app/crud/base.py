from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from supabase import Client

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], table_name: str):
        """Initialize CRUD base with model and table name."""
        self.model = model
        self.table_name = table_name

    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize data before sending to Supabase."""
        serialized = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, UUID):
                serialized[key] = str(value)
            elif isinstance(value, list):
                serialized[key] = [self._serialize_data(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                serialized[key] = self._serialize_data(value)
            else:
                serialized[key] = value
        return serialized

    def get(self, supabase: Client, id: Union[str, UUID]) -> Optional[ModelType]:
        """Get a single record by id."""
        try:
            result = supabase.table(self.table_name).select("*").eq("id", str(id)).execute()
            if result.data:
                return self.model(**result.data[0])
            return None
        except Exception as e:
            print(f"Error getting record: {str(e)}")
            return None

    def get_multi(
        self, supabase: Client, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        try:
            result = supabase.table(self.table_name).select("*").range(skip, skip + limit - 1).execute()
            return [self.model(**item) for item in result.data]
        except Exception as e:
            print(f"Error getting multiple records: {str(e)}")
            return []

    def create(self, supabase: Client, *, obj_in: CreateSchemaType, created_by: Optional[UUID] = None) -> ModelType:
        """Create a new record."""
        try:
            data = self._serialize_data(obj_in.model_dump())
            if created_by and "created_by" in self.model.model_fields:
                data["created_by"] = str(created_by)
            result = supabase.table(self.table_name).insert(data).execute()
            return self.model(**result.data[0])
        except Exception as e:
            print(f"Error creating record: {str(e)}")
            raise

    def update(
        self, supabase: Client, *, id: Union[str, UUID], obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """Update a record."""
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            update_data = self._serialize_data(update_data)
            result = supabase.table(self.table_name).update(update_data).eq("id", str(id)).execute()
            if result.data:
                return self.model(**result.data[0])
            return None
        except Exception as e:
            print(f"Error updating record: {str(e)}")
            return None

    def remove(self, supabase: Client, *, id: Union[str, UUID]) -> bool:
        """Remove a record."""
        try:
            result = supabase.table(self.table_name).delete().eq("id", str(id)).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error removing record: {str(e)}")
            return False 