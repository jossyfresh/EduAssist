from fastapi import APIRouter
from app.core.security_scheme import security

from app.api.v1.endpoints import auth, users, content, learning_paths, course, course_content, assessment, progress, youtube
from app.api.v1.endpoints import chat

# Create the main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning-paths"])
api_router.include_router(course.router, prefix="/courses", tags=["courses"])
api_router.include_router(course_content.router, prefix="/courses", tags=["courses-content"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])