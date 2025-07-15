from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.follow_model import user_followers
from fastapi.responses import JSONResponse



def get_my_account_information(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse(
        status_code=200,
        content={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username            
        }
    )



def get_user_by_id(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return JSONResponse(
            status_code=200,
            content={
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def follow_user(current_user_id: int, target_user_id: int, db: Session):
    try:
        if current_user_id == target_user_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself.")

        already_following = db.execute(
            user_followers.select().where(
                user_followers.c.follower_id == current_user_id,
                user_followers.c.following_id == target_user_id
            )
        ).first()

        if already_following:
            raise HTTPException(status_code=400, detail="Already following this user.")

        db.execute(
            user_followers.insert().values(
                follower_id=current_user_id,
                following_id=target_user_id
            )
        )
        db.commit()
        return {"message": "Followed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def unfollow_user(current_user_id: int, target_user_id: int, db: Session):
    try:
        if current_user_id == target_user_id:
            raise HTTPException(status_code=400, detail="Cannot unfollow yourself.")

        following = db.execute(
            user_followers.select().where(
                user_followers.c.follower_id == current_user_id,
                user_followers.c.following_id == target_user_id
            )
        ).first()

        if not following:
            raise HTTPException(status_code=400, detail="You are not following this user.")

        db.execute(
            user_followers.delete().where(
                user_followers.c.follower_id == current_user_id,
                user_followers.c.following_id == target_user_id
            )
        )
        db.commit()
        return {"message": "Unfollowed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
