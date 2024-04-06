from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models.posts import Post
from src.models.like import Like

user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("followers_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(
        String(60), nullable=False, unique=True, index=True
    )
    api_key: Mapped[str] = mapped_column()
    tweets: Mapped[List["Post"]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        backref="user",
        cascade="all, delete-orphan",
    )

    following = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.followers_id,
        secondaryjoin=id == user_to_user.c.following_id,
        backref="followers",
        lazy="selectin",
    )

    __mapper_args__ = {"confirm_deleted_rows": False}