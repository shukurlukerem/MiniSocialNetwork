from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import *
from app.core.config import get_db

def register_user(user_data, db: Session):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(first_name = user_data.first_name, last_name = user_data.last_name, username=user_data.username, email=user_data.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(user_data, db: Session):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}