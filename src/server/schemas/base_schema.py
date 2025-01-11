from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from src.bot.models.base import BaseOrm


class BaseSchema(BaseModel):
    __orm__ = None
    __transient_fields__ = ["id", "created_at", "updated_at"]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    id: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_orm(self):
        if not self.__orm__:
            raise NotImplementedError("Error __orm__ class not set")

        orm = self.__orm__()

        def set_val(key, data):
            if (isinstance(data, BaseOrm) or isinstance(data, list)) and key not in self.__transient_fields__:
                setattr(orm, key, data)
            else:
                for key, value in data:
                    try:
                        if isinstance(value, list):
                            set_val(key, [item.to_orm() for item in value if isinstance(item, BaseSchema)])
                        elif isinstance(value, BaseSchema) and key not in self.__transient_fields__:
                            setattr(orm, key, value.to_orm())
                        elif value is not None and key not in self.__transient_fields__:
                            setattr(orm, key, value)
                    except AttributeError:
                        pass

        set_val(None, self)

        return orm
