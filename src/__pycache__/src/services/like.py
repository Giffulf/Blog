from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from loguru import logger

from src.models.likes import Like
from src.services.post import PostsService
from src.utils.exeptions import CustomApiException


class LikeService:
    """
    Сервис для проставления лайков и дизлайков постам
    """

    @classmethod
    async def like(cls, post_id: int, user_id: int, session: AsyncSession) -> None:
        """
        Лайк поста
        :param post_id: id поста для лайка
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Лайк поста №{post_id}")

        # Поиск поста по id
        post = await PostsService.get_post(post_id=post_id, session=session)

        if not post:
            logger.error("Пост не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND, detail="Post not found"  # 404
            )

        if await cls.check_like_post(
            post_id=post_id, user_id=user_id, session=session
        ):
            logger.warning("Пользователь уже ставил лайк посту")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423
                detail="The user has already liked this post",
            )

        # TODO При реализации подсчета лайков
        # tweet.num_likes += 1  # Увеличиваем счетчик с лайками

        like_record = Like(user_id=user_id, post_id=post.id)

        session.add(like_record)
        await session.commit()

    @classmethod
    async def check_like_post(
        cls, post_id: int, user_id: int, session: AsyncSession
    ) -> Like | None:
        """
        Проверка лайка (метод возвращает запись о лайке, проверяя тем самым, ставил ли пользователь лайк
        указанному посту)
        :param post_id: id поста
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        """
        logger.debug("Поиск записи о лайке")

        query = select(Like).where(Like.user_id == user_id, Like.posts_id == post_id)
        like = await session.execute(query)

        return like.scalar_one_or_none()

    @classmethod
    async def dislike(cls, post_id: int, user_id: int, session: AsyncSession) -> None:
        """
        Удаление лайка
        :param tweet_id: id поста
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Дизлайк поста №{post_id}")

        # Поиск поста по id
        post = await PostsService.get_post(post_id=post_id, session=session)

        if not post:
            logger.error("Пост не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND, detail="Post not found"  # 404
            )

        # Ищем запись о лайке
        like_record = await cls.check_like_post(
            post_id=post_id, user_id=user_id, session=session
        )

        if like_record is None:
            logger.warning("Запись о лайке не найдена")

            raise CustomApiException(
                status_code=HTTPStatus.LOCKED,  # 423
                detail="The user has not yet liked this post",
            )

        await session.delete(like_record)  # Удаляем лайк

        await session.commit()