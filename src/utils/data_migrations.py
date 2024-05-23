from loguru import logger
import asyncio

from src.database import async_session_maker, engine, Base
from src.models.users import User
from src.models.posts import Post
from src.models.likes import Like

users = [
    {
        "username": "Юля",
        "api_key": "test1",
    },
    {
        "username": "Катя",
        "api_key": "test2",
    }
]

posts = [
    {
        "post_data": "Всем привет!! Я Юля!!!",
        "user_id": 1,
    },
    {
        "post_data": "Всем привет!! Я Катя!!!",
        "user_id": 2,
    }
]

likes = [
    {
        "user_id": 1,
        "posts_id": 1,
    },
    {
        "user_id": 2,
        "posts_id": 1,
    }
]


async def re_creation_db():
    """
    Удаление и создание БД
    """
    logger.debug("Создание БД")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Удаление всех таблиц
        await conn.run_sync(Base.metadata.create_all)  # Создание всех таблиц


async def migration_data():
    """
    Функция для наполнения БД демонстрационными данными
    """
    logger.debug("Загрузка демонстрационных данных")

    await re_creation_db()

    async with async_session_maker() as session:
        # Инициализируем и добавляем пользователей
        initial_users = [User(**user) for user in users]
        session.add_all(initial_users)

        # Подписки пользователей
        initial_users[0].following.extend([initial_users[1], initial_users[2]])
        initial_users[1].following.append(initial_users[0])
        initial_users[2].following.extend([initial_users[1], initial_users[0]])

        # Посты
        initial_posts = [Post(**post) for post in posts]
        session.add_all(initial_posts)

        # Лайки
        initial_likes = [Like(**like) for like in likes]
        session.add_all(initial_likes)

        await session.commit()

        logger.debug("Данные успешно добавлены")


if __name__ == "__main__":
    asyncio.run(migration_data())
