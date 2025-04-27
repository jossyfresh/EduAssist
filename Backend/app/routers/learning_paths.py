from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID
from ..models.learning_path import LearningPath, LearningPathCreate, LearningPathUpdate
from ..dependencies import get_current_user
from ..database import supabase

router = APIRouter(prefix="/learning-paths", tags=["learning_paths"])

@router.post("/", response_model=LearningPath)
async def create_learning_path(
    learning_path: LearningPathCreate,
    current_user: dict = Depends(get_current_user)
):
    data = learning_path.dict()
    data["user_id"] = current_user["id"]
    
    response = supabase.table("learning_paths").insert(data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create learning path")
    return response.data[0]

@router.get("/", response_model=List[LearningPath])
async def get_learning_paths(current_user: dict = Depends(get_current_user)):
    response = supabase.table("learning_paths").select("*").eq("user_id", current_user["id"]).execute()
    return response.data

@router.get("/{path_id}", response_model=LearningPath)
async def get_learning_path(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    response = supabase.table("learning_paths").select("*").eq("id", str(path_id)).eq("user_id", current_user["id"]).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return response.data[0]

@router.put("/{path_id}", response_model=LearningPath)
async def update_learning_path(
    path_id: UUID,
    learning_path: LearningPathUpdate,
    current_user: dict = Depends(get_current_user)
):
    # First verify the learning path exists and belongs to the user
    check_response = supabase.table("learning_paths").select("*").eq("id", str(path_id)).eq("user_id", current_user["id"]).execute()
    if not check_response.data:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Update the learning path
    response = supabase.table("learning_paths").update(learning_path.dict(exclude_unset=True)).eq("id", str(path_id)).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to update learning path")
    return response.data[0]

@router.delete("/{path_id}")
async def delete_learning_path(
    path_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    # First verify the learning path exists and belongs to the user
    check_response = supabase.table("learning_paths").select("*").eq("id", str(path_id)).eq("user_id", current_user["id"]).execute()
    if not check_response.data:
        raise HTTPException(status_code=404, detail="Learning path not found")
    
    # Delete the learning path
    response = supabase.table("learning_paths").delete().eq("id", str(path_id)).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to delete learning path")
    return {"message": "Learning path deleted successfully"} 