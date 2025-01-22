from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _


class InputTypeFilter(BaseFilter):
    def __init__(self, input_type: type):
        """
        :param input_type: Expected input type (example, int, str).
        """
        self.input_type = input_type

    async def __call__(self, obj: Message) -> bool:
        humanize_type = _("undefined")
        if self.input_type == int:
            humanize_type = _("number")
        elif self.input_type == str:
            humanize_type = _("text")

        try:
            self.input_type(obj.text)
            return True
        except (ValueError, TypeError):
            await obj.answer(text=_("invalid_type").format(expected=humanize_type))
            return False
