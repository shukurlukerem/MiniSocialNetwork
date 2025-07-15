from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.v1.schemas.post_schema import PostCreate, PostUpdate, PostResponse
from app.services.post_services import *
from app.core.config import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.post("/new-post", response_model=PostResponse)
def create_new_post(post_data: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_post(post_data, db, current_user.id)


@router.get("/all-posts", response_model=List[PostResponse])
def read_all_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def read_single_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_by_id(post_id, db)


@router.put("/update-post/{post_id}", response_model=PostResponse)
def edit_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_post(post_id, post_data, db, current_user.id)


@router.delete("/delete-post/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_post(post_id, db, current_user.id)


@router.post("/like/{post_id}")
def like(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return like_post(post_id, db, current_user.id)


@router.delete("/unlike/{post_id}")
def unlike(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return unlike_post(post_id, db, current_user.id)
