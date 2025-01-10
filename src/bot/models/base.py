import typing
from typing import Optional
from datetime import datetime

import orjson
import pydantic
import pytz
from pydantic import ConfigDict
from sqlalchemy import Column, BigInteger, DateTime
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def orjson_dumps(
    v: typing.Any,
    *,
    default: Optional[typing.Callable[[typing.Any], typing.Any]],
) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict()


class BaseOrm(Base):
    """
    Provides primary key column, created and updated timestamps
    """

    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.now(pytz.UTC),
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )
