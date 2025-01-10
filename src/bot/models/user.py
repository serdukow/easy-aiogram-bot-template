from sqlalchemy import Column, String, Boolean, BigInteger

from src.bot.models.base import BaseOrm


class UserOrm(BaseOrm):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, nullable=False)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    is_bot = Column(Boolean)
    language = Column(String(5), nullable=False, default="en")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
