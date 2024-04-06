from fastapi import FastAPI, Depends
from src.urls import register_routers


app = FastAPI(title="Twitter", debug=True, dependencies=[Depends()])

register_routers(app)
