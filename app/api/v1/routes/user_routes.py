from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_services import *
from app.core.config import get_db
from app.core.security import get_current_user
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.get("/me", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def account(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_my_account_information(current_user.id, db)


@router.post("/follow/{id}", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def follow(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return follow_user(current_user.id, id, db)

@router.delete("/unfollow/{id}", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def follow(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return unfollow_user(current_user.id, id, db)


@router.get("/user/{id}", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def user (id:int, db: Session = Depends(get_db)):
    return get_user_by_id(id,db)