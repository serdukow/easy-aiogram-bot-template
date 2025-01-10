from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from src.bot.keyboards.calls import Action
from src.bot.keyboards.constructor import InlineConstructor


class ReplyMarkupConstructor:
    """
    A utility class for creating reply markups, including default buttons and dynamic keyboard generation.

    Features:
        - `back_button`: Creates a default "Back" button, either as a standalone or as part of a keyboard.
        - `CreateReplyMarkup`: A nested class for generating inline keyboards based on templates.

    Methods:
        - back_button(back_to, solely): Creates a "Back" button with optional callback data.
        - CreateReplyMarkup.from_template(actions, back_button): Generates a keyboard using a list of actions
          and optionally appends a "Back" button.

    Example:
        constructor = ReplyMarkupConstructor()
        markup = await constructor.create_rm.from_template(actions=[...], back_button="mainMenu")
    """
    def __init__(self):
        self.create_rm = self.CreateReplyMarkup(self)

    @staticmethod
    async def back_button(
            back_to: str = "main",
            solely: Optional[bool] = False,
    ) -> [dict, InlineKeyboardMarkup]:
        """
        Creates a default "Back" button.

        Args:
            back_to (str): The callback action for the button.
            solely (bool): If True, returns a button as a single-item keyboard.

        Returns:
            dict | InlineKeyboardMarkup: Button data or a keyboard with the button.
        """
        action = {
            "text": _('Back ←'),
            "cb": Action(action=f"{back_to}")
        }
        if solely:
            return InlineConstructor.create_kb([action], [1])
        return action

    class CreateReplyMarkup:
        """
        Handles creating inline keyboards based on templates.

        Methods:
            - from_template: Generates a keyboard from a list of actions, optionally adding a "Back" button.
        """
        def __init__(self, parent: 'ReplyMarkupConstructor'):
            self.parent = parent

        async def from_template(
                self,
                actions: list,
                back_button: str = None,
        ):
            """
            Creates an inline keyboard from a template.

            Args:
                actions (list): List of buttons to include.
                back_button (str): Callback action for the optional "Back" button.

            Returns:
                InlineKeyboardMarkup: The constructed keyboard.
            """
            if back_button:
                back_button = await self.parent.back_button(back_to=back_button)
                actions.append(back_button)

            schema = [1] * len(actions)

            return InlineConstructor.create_kb(actions, schema)
