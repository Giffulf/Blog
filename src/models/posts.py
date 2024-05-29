import datetime

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from src.database import Base
from src.models.likes import Like

class Post(Base):
    """
    Модель для хранения твитов
    """

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    post_data: Mapped[str] = mapped_column(String(280))
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    likes: Mapped[List["Like"]] = relationship(
        backref="post", cascade="all, delete-orphan"
    )

    __mapper_args__ = {"confirm_deleted_rows": False}
