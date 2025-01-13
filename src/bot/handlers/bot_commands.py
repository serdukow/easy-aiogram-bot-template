from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from src.bot.core import config
from src.bot.keyboards.calls import Action
from src.bot.keyboards.inline import ReplyMarkupConstructor
from src.bot.repositories.user import UserRepository

router = Router(name=__name__)

user_repo = UserRepository()

rm_constructor = ReplyMarkupConstructor()


async def cmd_start(obj: [CallbackQuery, Message]):

    msg = obj.message if isinstance(obj, CallbackQuery) else obj

    actions = [
        {"text": _("grant_admin"), "cb": Action(action="grant_admin")},
        {"text": _("get_me"), "cb": Action(action="get_me")},
    ]

    reply_markup = await rm_constructor.create_rm.from_template(actions=actions)

    await user_repo.get_or_create_user(
        telegram_id=obj.from_user.id,
        full_name=obj.from_user.full_name,
        username=obj.from_user.username,
        is_premium=obj.from_user.is_premium,
        is_bot=obj.from_user.is_bot,
        language=obj.from_user.language_code
    )

    if isinstance(obj, CallbackQuery):
        await msg.edit_text(
            text=_("hello").format(full_name=msg.from_user.full_name),
            reply_markup=reply_markup
        )
    else:
        await msg.answer(
            text=_("hello").format(full_name=msg.from_user.full_name),
            reply_markup=reply_markup
        )


@router.message(CommandStart())
async def handle_cmd_start(msg: Message):
    await cmd_start(msg)


@router.callback_query(Action.filter(F.action == "main"))
async def handle_call_cmd_start(call: CallbackQuery):
    await cmd_start(call)


@router.callback_query(Action.filter(F.action == "grant_admin"))
async def grant_admin(msg: Message):

    user = await user_repo.get_by_telegram_id(telegram_id=msg.from_user.id)

    if user.telegram_id in config.ADMINS_IDS:
        await msg.answer(text=_("already_admin").format(admin_id=user.telegram_id), show_alert=True)
        return

    reply_markup = await rm_constructor.back_button(solely=True)
    await msg.answer(
        text=_("how_to_grant_admin_rights"),
        reply_markup=reply_markup,
        show_alert=True
    )


@router.callback_query(Action.filter(F.action == "get_me"))
async def get_me(call: CallbackQuery):
    reply_markup = await rm_constructor.back_button(solely=True)
    await call.message.edit_text(
        text=_("me").format(from_user=call.from_user),
        reply_markup=reply_markup
    )
