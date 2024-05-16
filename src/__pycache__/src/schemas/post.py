from http import HTTPStatus
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict

from src.schemas.base_response import ResponseSchema
from src.schemas.like import LikeSchema
from src.schemas.user import UserSchema
from src.utils.exeptions import CustomApiException


class PostInSchema(BaseModel):
    """
    Схема для входных данных при добавлении нового поста
    """

    post_data: str = Field()
    post_media_ids: Optional[list[int]]

    @field_validator("post_data", mode="before")
    @classmethod
    def check_len_post_data(cls, val: str) -> str | None:
        """
        Проверка длины поста с переопределением вывода ошибки в случае превышения
        """
        if len(val) > 280:
            raise CustomApiException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
                detail=f"The length of the tweet should not exceed 280 characters. "
                f"Current value: {len(val)}",
            )

        return val

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )


class PostResponseSchema(ResponseSchema):
    """
    Схема для вывода id поста после публикации
    """

    id: int = Field(alias="post_id")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )


class PostOutSchema(BaseModel):
    """
    Схема для вывода поста, автора, вложенных изображений и данных по лайкам
    """

    id: int
    post_data: str = Field(alias="content")
    user: UserSchema = Field(alias="author")
    likes: List[LikeSchema]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Использовать псевдоним вместо названия поля
    )


class PostListSchema(ResponseSchema):
    """
    Схема для вывода списка постов
    """

    posts: List[PostOutSchema]