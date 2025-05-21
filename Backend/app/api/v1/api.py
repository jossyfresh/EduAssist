from fastapi import APIRouter
from app.core.security_scheme import security

from app.api.v1.endpoints import auth, users, content, learning_paths

# Create the main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning-paths"]) 