from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.config import Base
from app.models.follow_model import user_followers

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="author", cascade="all, delete")
    
    following = relationship(
        "User",
        secondary=user_followers,
        primaryjoin=id == user_followers.c.follower_id,
        secondaryjoin=id == user_followers.c.following_id,
        backref="followers"
    )

