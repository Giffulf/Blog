from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.users import User
from src.services.like import LikeService
from src.services.post import PostsService
from src.utils.user import get_current_user
from src.schemas.post import PostResponseSchema, PostInSchema, PostListSchema
from src.schemas.base_response import (
    ResponseSchema,
    UnauthorizedResponseSchema,
    ValidationResponseSchema,
    LockedResponseSchema,
    ErrorResponseSchema,
)


router = APIRouter(
    prefix="/api/posts", tags=["posts"]  # URL  # Объединяем URL в группу
)


@router.get(
    "",
    response_model=PostListSchema,
    responses={401: {"model": UnauthorizedResponseSchema}},
    status_code=200,
)
async def get_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Вывод ленты постов (выводятся посты людей, на которых подписан пользователь)
    """
    posts = await PostsService.get_posts(user=current_user, session=session)

    return {"posts": posts}


@router.post(
    "",
    response_model=PostResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        422: {"model": ValidationResponseSchema},
    },
    status_code=201,
)
async def create_post(
    post: PostInSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Добавление поста
    """
    post = await PostsService.create_post(
        post=post, current_user=current_user, session=session
    )

    return {"post_id": post.id}


@router.delete(
    "/{post_id}",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200,
)
async def delete_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление поста
    """
    await PostsService.delete_post(
        user=current_user, post_id=post_id, session=session
    )

    return {"result": True}


@router.post(
    "/{post_id}/likes",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=201,
)
async def create_like(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Лайк поста
    """
    await LikeService.like(post_id=post_id, user_id=current_user.id, session=session)

    return {"result": True}


@router.delete(
    "/{post_id}/likes",
    response_model=ResponseSchema,
    responses={
        401: {"model": UnauthorizedResponseSchema},
        404: {"model": ErrorResponseSchema},
        422: {"model": ValidationResponseSchema},
        423: {"model": LockedResponseSchema},
    },
    status_code=200,
)
async def delete_like(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удаление лайка
    """
    await LikeService.dislike(
        post_id=post_id, user_id=current_user.id, session=session
    )

    return {"result": True}