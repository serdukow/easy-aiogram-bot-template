from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


class TextLengthFilter(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        if msg.text and len(msg.text) > 4000:
            await msg.answer(text=_("too_much_char").format(length=len(msg.text)))
            return False
        if msg.caption and len(msg.caption) > 1000:
            await msg.answer(text="too_much_char_in_caption").format(length=len(msg.caption))
            return False
        return True
