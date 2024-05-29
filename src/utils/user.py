from loguru import logger
import asyncio

from src.database import async_session_maker, engine, Base
from src.models.users import User
from src.models.posts import Post
from src.models.likes import Like

users = [
    {
        "username": "Юля",
        "api_key": "test",
    },
    {
        "username": "Катя",
        "api_key": "test2",
    },
    {
        "username": "Лёша",
        "api_key": "test3",
    },
]

posts = [
    {
        "post_data": "Как я устала от этой учёбы!",
        "user_id": 1,
    },
    {
        "post_data": "Кинофестиваль в Чите 31 мая - 2 июня",
        "user_id": 2,
    },
    {
        "post_data": "Новейшая разработка в медицине",
        "user_id": 3,
    },
    {
        "post_data": "Игра года 20-24!",
        "user_id": 2,
    },
    {
        "post_data": "Капец вы все веселые.. ха-ха.. где петля?",
        "user_id": 1,
    },
    {
        "post_data": "Да ладно, мне не жалко!",
        "user_id": 1,
    },
    {
        "post_data": "Угодовая косметика от Exile!",
        "user_id": 3,
    },
    {
        "post_data": "День рождения МИИГАиК 245 лет!",
        "user_id": 3,
    },
    {
        "post_data": "Как перебороть лень!",
        "user_id": 2,
    },
    {
        "post_data": "Как поднять мотивацию?",
        "user_id": 2,
    },
    {
        "post_data": "Новое обновление Геншина!!",
        "user_id": 2,
    },
    {
        "post_data": "Да-да, я Максим...",
        "user_id": 1,
    },
]

likes = [
    {
        "user_id": 1,
        "posts_id": 1,
    },
    {
        "user_id": 3,
        "posts_id": 1,
    },
    {
        "user_id": 2,
        "posts_id": 1,
    },
    {
        "user_id": 2,
        "posts_id": 2,
    },
    {
        "user_id": 3,
        "posts_id": 2,
    },
    {
        "user_id": 1,
        "posts_id": 3,
    },
    {
        "user_id": 2,
        "posts_id": 3,
    },
    {
        "user_id": 1,
        "posts_id": 4,
    },
    {
        "user_id": 1,
        "posts_id": 6,
    },
    {
        "user_id": 3,
        "posts_id": 6,
    },
    {
        "user_id": 2,
        "posts_id": 7,
    },
    {
        "user_id": 1,
        "posts_id": 9,
    },
    {
        "user_id": 2,
        "posts_id": 9,
    },
    {
        "user_id": 2,
        "posts_id": 11,
    },
    {
        "user_id": 3,
        "posts_id": 1,
    },
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
