from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from loguru import logger

from src.models.likes import Like
from src.models.posts import Post
from src.models.users import User
from src.utils.exeptions import CustomApiException
from src.schemas.post import PostInSchema


class PostsService:
    """
    Сервис для добавления, удаления и вывода постов
    """

    @classmethod
    async def get_posts(cls, user: User, session: AsyncSession):
        """
        Вывод последних постов подписанных пользователей
        :param user: объект текущего пользователя
        :param session: объект асинхронной сессии
        :return: список с постами
        """
        logger.debug("Вывод постов")

        # FIXME По ТЗ возврат с сортировкой по популярности
        #  (сделать в модели подсчет лайков + сортировка по дате и лайкам)
        query = (
            select(Post)
            .filter(Post.user_id.in_(user.id for user in user.following))
            .options(
                joinedload(Post.user),
                joinedload(Post.likes).subqueryload(Like.user)
            )
            .order_by(Post.created_at.desc())
        )
        # joinedload - запрашиваем данные из связанных таблиц
        # subqueryload - запрашиваем связанные вложенные данные по автору лайка без доп.запроса к БД

        result = await session.execute(query)
        posts = result.unique().scalars().all()

        return posts

    @classmethod
    async def get_post(cls, post_id: int, session: AsyncSession) -> Post | None:
        """
        Возврат поста по переданному id
        :param post_id: id поста для поиска
        :param session: объект асинхронной сессии
        :return: объект поста
        """
        logger.debug(f"Поиск поста по id: {post_id}")

        query = select(Post).where(Post.id == post_id)
        post = await session.execute(query)

        return post.scalar_one_or_none()

    @classmethod
    async def create_post(
        cls, post: PostInSchema, current_user: User, session: AsyncSession
    ) -> Post:
        """
        Создание нового поста
        :param post: данные для нового поста
        :param current_user: объект текущего пользователя
        :param session: объект асинхронной сессии
        :return: объект нового поста
        """
        logger.debug("Добавление нового поста")

        new_post = Post(post_data=post.post_data, user_id=current_user.id)

        session.add(new_post)
        # Сохраняем в БД все изменения
        await session.commit()

        return new_post

    @classmethod
    async def delete_post(
        cls, user: User, post_id: int, session: AsyncSession
    ) -> None:
        """
        Удаление поста
        :param user: объект текущего пользователя
        :param post_id: id удаляемого поста
        :param session: объект асинхронной сессии
        :return: None
        """
        logger.debug(f"Удаление поста")

        # Поиск поста по id
        post = await cls.get_post(post_id=post_id, session=session)

        if not post:
            logger.error("Пост не найден")

            raise CustomApiException(
                status_code=HTTPStatus.NOT_FOUND, detail="Post not found"  # 404
            )

        else:
            if post.user_id != user.id:
                logger.error("Запрос на удаление чужого поста")

                raise CustomApiException(
                    status_code=HTTPStatus.LOCKED,  # 423
                    detail="The post that is being accessed is locked",
                )

            else:

                # Удаляем пост
                await session.delete(post)
                await session.commit()