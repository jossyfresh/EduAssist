from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.crud.crud_content import crud_content
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse
from app.models.content import Content as ContentModel
from app.models.enums import ContentType
from fastapi import HTTPException
import json
import base64
from datetime import datetime

class ContentService:
    async def create_content(self, content: ContentCreate, user_id: str) -> ContentResponse:
        """Create new content."""
        try:
            from app.services.content_generator import ContentGenerator
            generator = ContentGenerator()
            
            # Handle AI-generated content types
            if content.content_type in ["QUIZ", "SUMMARY", "FLASHCARD", "YOUTUBE_SUGGESTIONS", 
                                      "COURSE", "EXERCISES", "CODE_EXAMPLES", "LEARNING_PATH"]:
                # Generate content using AI
                generated_data = await generator.generate_content(
                    content_type=content.content_type.lower(),
                    parameters=content.meta.get("parameters", {}),
                    provider=content.meta.get("generator", "openai")
                )
                
                # Create content in database based on type
                if content.content_type == "QUIZ":
                    parameters = {
                        **(content.meta or {}),
                        "title": generated_data.get("title", "Generated Quiz"),
                        "content": generated_data.get("content", "{}"),
                        "description": generated_data.get("description", "AI-generated quiz"),
                        "questions": generated_data.get("meta", {}).get("questions", []),
                        "num_questions": generated_data.get("meta", {}).get("num_questions", 0),
                        "difficulty": generated_data.get("meta", {}).get("difficulty", "beginner")
                    }
                    db_content = crud_content.create_quiz(
                        db=self.get_db(),
                        parameters=parameters,
                        user_id=user_id
                    )
                else:
                    # For other AI-generated content, store as TEXT
                    db_content = crud_content.create_text(
                        db=self.get_db(),
                        obj_in=ContentCreate(
                            title=content.title or f"Generated {content.content_type.title()}",
                            content_type="TEXT",
                            content=generated_data.get("content", ""),
                            description=content.description or f"AI-generated {content.content_type.lower()}",
                            meta={
                                **(content.meta or {}),
                                "generated_type": content.content_type,
                                "generated_data": generated_data
                            }
                        ),
                        user_id=user_id
                    )
            else:
                # Use the appropriate create method based on content type
                if content.content_type == "TEXT":
                    db_content = crud_content.create_text(
                        db=self.get_db(),
                        obj_in=content,
                        user_id=user_id
                    )
                elif content.content_type == "VIDEO":
                    db_content = crud_content.create_video(
                        db=self.get_db(),
                        obj_in=content,
                        user_id=user_id
                    )
                elif content.content_type == "FILE":
                    db_content = crud_content.create_file(
                        db=self.get_db(),
                        obj_in=content,
                        user_id=user_id
                    )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unsupported content type: {content.content_type}"
                    )
            
            return ContentResponse.from_orm(db_content)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_content(self, content_id: str) -> ContentResponse:
        """Get content by ID."""
        content = crud_content.get(db=self.get_db(), id=content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return ContentResponse.from_orm(content)

    async def update_content(self, content_id: str, content: ContentUpdate) -> ContentResponse:
        """Update existing content."""
        db_content = crud_content.get(db=self.get_db(), id=content_id)
        if not db_content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        updated_content = crud_content.update(
            db=self.get_db(),
            db_obj=db_content,
            obj_in=content
        )
        return ContentResponse.from_orm(updated_content)

    async def delete_content(self, content_id: str) -> bool:
        """Delete content."""
        content = crud_content.get(db=self.get_db(), id=content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        crud_content.remove(db=self.get_db(), id=content_id)
        return True

    async def get_batch(self, batch_id: str) -> Dict[str, Any]:
        """Get files in a batch."""
        files = crud_content.get_by_batch(db=self.get_db(), batch_id=batch_id)
        if not files:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        return {
            "batch_id": batch_id,
            "files": [ContentResponse.from_orm(file) for file in files]
        }

    async def add_files_to_batch(self, batch_id: str, files: List[Any]) -> Dict[str, Any]:
        """Add files to an existing batch."""
        # Verify batch exists
        existing_files = crud_content.get_by_batch(db=self.get_db(), batch_id=batch_id)
        if not existing_files:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        uploaded_contents = []
        for file in files:
            content = await file.read()
            content_b64 = base64.b64encode(content).decode('utf-8')
            
            content_obj = ContentCreate(
                title=file.filename,
                content_type=ContentType.FILE,
                content=content_b64,
                meta={
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": len(content),
                    "batch_id": batch_id
                },
                description=f"Uploaded file: {file.filename}"
            )
            
            content = crud_content.create_file(
                db=self.get_db(),
                obj_in=content_obj,
                user_id=existing_files[0].created_by
            )
            uploaded_contents.append(ContentResponse.from_orm(content))
        
        return {
            "batch_id": batch_id,
            "added_files": uploaded_contents
        }

    def get_db(self) -> Session:
        """Get database session."""
        from app.db.session import SessionLocal
        db = SessionLocal()
        try:
            return db
        finally:
            db.close() 