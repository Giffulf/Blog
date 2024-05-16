import uvicorn
from fastapi import FastAPI
from src.urls import register_routers


app = FastAPI(title="Blogs", debug=True)

register_routers(app)

uvicorn.run(app, port=8000)
