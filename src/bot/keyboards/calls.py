from typing import Optional

from aiogram.filters.callback_data import CallbackData


class Action(CallbackData, prefix="act"):
    """
    Represents the actions of the button.

    Attributes:
        action (Optional[str]): Name of action.
    """
    action: str
