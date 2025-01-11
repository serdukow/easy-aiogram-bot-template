from fastapi import FastAPI
from .user_controller import router as user_router


def register_controllers(app: FastAPI):
    app.include_router(user_router)
