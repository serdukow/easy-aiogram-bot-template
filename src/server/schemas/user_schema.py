from typing import Optional

from src.bot.models.user import UserOrm
from src.server.schemas.base_schema import BaseSchema


class UserSchema(BaseSchema):
    __orm__ = UserOrm

    telegram_id: int
    full_name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_premium: Optional[bool] = False
    is_bot: Optional[bool] = False
    language: Optional[str] = "en"
