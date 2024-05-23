import pytest

from typing import Tuple, Dict
from http import HTTPStatus

from src.models.posts import Post
from src.models.users import User
from tests.database import async_session_maker


@pytest.fixture(scope="session")
async def posts(users: Tuple[User]):
    """
    Посты для тестирования
    """
    async with async_session_maker() as session:
        post_1 = Post(post_data="Тестовый пост 1", user_id=users[0].id)
        post_2 = Post(post_data="Тестовый пост 2", user_id=users[1].id)
        post_3 = Post(post_data="Тестовый пост 3", user_id=users[2].id)

        session.add_all([post_1, post_2, post_3])
        await session.commit()

        return post_1, post_2


@pytest.fixture(scope="session")
async def headers():
    """
    Параметр в header для выполнения запросов
    """
    return {"api-key": "test-user1"}


@pytest.fixture(scope="session")
async def good_response():
    """
    Успешный ответ
    """
    return {"result": True}


@pytest.fixture(scope="session")
async def bad_response():
    """
    Неуспешный ответ
    """
    return {"result": False}


@pytest.fixture(scope="session")
async def response_not_found(bad_response: Dict):
    """
    Ответ с кодом 404
    """
    not_found_resp = bad_response.copy()
    not_found_resp["error_type"] = f"{HTTPStatus.NOT_FOUND}"

    return not_found_resp


@pytest.fixture(scope="session")
async def response_locked(bad_response: Dict):
    """
    Ответ с кодом 423
    """
    locked_resp = bad_response.copy()
    locked_resp["error_type"] = f"{HTTPStatus.LOCKED}"

    return locked_resp


@pytest.fixture(scope="session")
async def response_tweet_not_found(response_not_found: Dict):
    """
    Ответ с текстом ошибки, что твит не найден
    """
    tweet_not_found_resp = response_not_found.copy()
    tweet_not_found_resp["error_message"] = "Tweet not found"

    return tweet_not_found_resp