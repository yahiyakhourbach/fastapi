from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id          = Column(Integer, nullable=False, primary_key=True)
    title       = Column(String, nullable=False)
    content     = Column(String, nullable=False)
    created_at  = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    published   = Column(Boolean, server_default='TRUE',nullable=False)
    owner_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)

    user        = relationship("User")

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, nullable=False, primary_key=True)
    username    = Column(String, nullable=False,unique=True)
    email       = Column(String, nullable=False,unique=True)
    password    = Column(String,nullable=False)
    created_at  = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)