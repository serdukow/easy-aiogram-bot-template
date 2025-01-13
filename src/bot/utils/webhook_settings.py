from functools import lru_cache

from fastapi import FastAPI
from pydantic.v1 import BaseSettings
from fastapi.middleware.cors import CORSMiddleware

from src.bot.core import config


class WEBHOOKSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 3001
    log_level: str = "debug"

    ALLOWED_CORS_ORIGINS: set = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "localhost",
        "localhost:5173",
        "127.0.0.1",
        "host.docker.internal",
    ]

    class Config:
        env_prefix = "WEBHOOK_SET_"

    @staticmethod
    def allow_cors_origins(
            app: FastAPI,
            cors_middleware: type(CORSMiddleware) = CORSMiddleware):
        app.add_middleware(
            cors_middleware,
            allow_origins=WEBHOOKSettings().ALLOWED_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return app


@lru_cache()
def get_webhook_settings() -> WEBHOOKSettings:
    return WEBHOOKSettings()
