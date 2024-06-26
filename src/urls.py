from fastapi import FastAPI

from src.routes.user import router as user_router
from src.routes.posts import router as posts_router


def register_routers(app: FastAPI) -> FastAPI:
    """
    Регистрация роутов для API
    """

    app.include_router(user_router)  # Вывод информации о пользователе
    app.include_router(posts_router)  # Добавление, удаление и вывод постов

    return app