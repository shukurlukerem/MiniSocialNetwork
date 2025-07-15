from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.post_model import Post
from app.api.v1.schemas.post_schema import PostCreate, PostUpdate
from datetime import datetime
from app.models.like_model import PostLike

def create_post(post_data: PostCreate, db: Session, current_user_id: int):
    post = Post(
        title=post_data.title,
        desc=post_data.desc,
        user_id=current_user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_posts(db: Session):
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post_by_id(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def update_post(post_id: int, post_data: PostUpdate, db: Session, current_user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only update your own posts")

    post.title = post_data.title or post.title
    post.desc = post_data.desc or post.desc
    post.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(post)
    return post


def delete_post(post_id: int, db: Session, current_user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}



def like_post(post_id: int, db: Session, current_user_id: int):
    existing_like = db.query(PostLike).filter_by(post_id=post_id, user_id=current_user_id).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="You have already liked this post.")

    like = PostLike(post_id=post_id, user_id=current_user_id)
    db.add(like)
    db.commit()
    return {"message": "Post liked"}


def unlike_post(post_id: int, db: Session, current_user_id: int):
    like = db.query(PostLike).filter_by(post_id=post_id, user_id=current_user_id).first()

    if not like:
        raise HTTPException(status_code=400, detail="You have not liked this post.")

    db.delete(like)
    db.commit()
    return {"message": "Post unliked"}


