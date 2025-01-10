from types import MappingProxyType
from typing import TypeVar, Union, List, Dict

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    CallbackGame,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    WebAppInfo,
)

from .. import exceptions
from . import layout

A = TypeVar("A", bound=type[CallbackData])

POSSIBLE_BUTTON_PROPERTIES_VALUES = Union[  # https://core.telegram.org/bots/api#inlinekeyboardbutton
    str,
    WebAppInfo,
    LoginUrl,
    SwitchInlineQueryChosenChat,
    CallbackGame,
    bool,
    CallbackData
]
POSSIBLE_INPUT_ACTIONS_TYPES = Dict[str, POSSIBLE_BUTTON_PROPERTIES_VALUES]


class InlineConstructor:
    aliases = MappingProxyType(
        {
            "cb": "callback_data",
        },
    )
    required_properties = ("text",)
    additional_properties = (
        "callback_data",
        "url",
        "web_app",
        "login_url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
        "pay",
    )
    possible_properties = (*required_properties, *additional_properties)
    max_additional_properties = 1
    max_possible_properties = len(required_properties) + max_additional_properties

    @staticmethod
    def create_kb(
            actions: List[POSSIBLE_INPUT_ACTIONS_TYPES],
            schema: List[int],
    ) -> InlineKeyboardMarkup:
        buttons: List[InlineKeyboardButton] = []

        for cur_action in actions:
            data: Dict[str, POSSIBLE_BUTTON_PROPERTIES_VALUES] = {}

            if "text" in cur_action:
                cur_action["text"] = cur_action["text"]

            for k, v in InlineConstructor.aliases.items():
                if k in cur_action:
                    cur_action[v] = cur_action[k]
                    del cur_action[k]

            for k in cur_action:
                if k not in InlineConstructor.possible_properties:
                    raise exceptions.UnknownKeyboardButtonPropertyError(
                        unknown_property=k,
                        property_value=cur_action[k],
                        known_properties=InlineConstructor.possible_properties,
                    )
                if len(data) >= InlineConstructor.max_possible_properties:
                    raise exceptions.TooManyArgsToCreateButtonError(
                        provided_args=list(data.keys()),
                        max_args_amount=InlineConstructor.max_possible_properties,
                    )
                data[k] = cur_action[k]

            if not all(
                    added_property in data
                    for added_property in InlineConstructor.required_properties
            ):
                raise exceptions.NotEnoughArgsToCreateButtonError(
                    provided_args=list(data.keys()),
                    required_args=InlineConstructor.required_properties,
                )

            if "callback_data" in data and isinstance(data["callback_data"], CallbackData):
                data["callback_data"] = data["callback_data"].pack()

            if "pay" in data:
                if len(buttons) != 0 and data["pay"]:
                    raise exceptions.PaymentButtonMustBeFirstError
                data["pay"] = cur_action["pay"]

            buttons.append(InlineKeyboardButton(**data))

        kb = InlineKeyboardMarkup(
            inline_keyboard=layout.create_keyboard_layout(buttons, schema),
        )
        return kb
