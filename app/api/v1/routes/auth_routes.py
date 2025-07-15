from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_services import register_user, login_user
from fastapi_limiter.depends import RateLimiter
from app.core.config import get_db

router = APIRouter()

@router.post("/register", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login", dependencies=[Depends(RateLimiter(times=100, seconds=600))])
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)