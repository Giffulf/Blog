from fastapi import FastAPI


def register_routers(app: FastAPI) -> FastAPI:


    app.include_router()
    app.include_router()

    return app