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


@router.message(CommandStart())
async def cmd_start(msg: Message):
    """
    Handles the /start command, which introduces the main easy-aiogram-bot features to the user.

    :param msg: Incoming message object from the user.

    Functionality:
    1. **Action Buttons**:
       - Generates a base keyboard with action buttons for user interaction:
         - "grant_admin": Initiates the process to grant admin rights.
         - "get_me": Fetches and displays user information.

    2. **User Data Management**:
       - Checks if the user exists in the database by their Telegram ID.
       - If the user does not exist:
         - Creates a new user in the database.
       - If the user exists:
         - Updates their data if it has changed (e.g., username or premium status).

    3. **Personalized Greeting**:
       - Sends a localized greeting message to the user, including their full name.

    4. **Reply Markup**:
       - Attaches an inline keyboard to the greeting message for additional actions.

    Example Usage:
    1. User sends the /start command.
    2. Bot replies with:
       - Greeting message: "Hello, John Doe!"
       - Inline keyboard with localized buttons for "Grant Admin" and "Get Me".
    """

    actions = [
        {"text": _("grant_admin"), "cb": Action(action="grant_admin")},
        {"text": _("get_me"), "cb": Action(action="get_me")},
    ]

    reply_markup = await rm_constructor.create_rm.from_template(actions=actions)

    await user_repo.get_or_create_user(
        telegram_id=msg.from_user.id,
        full_name=msg.from_user.full_name,
        username=msg.from_user.username,
        is_premium=msg.from_user.is_premium,
        is_bot=msg.from_user.is_bot,
        language=msg.from_user.language_code
    )
    await msg.answer(
        text=_("hello").format(full_name=msg.from_user.full_name),
        reply_markup=reply_markup
    )


@router.callback_query(Action.filter(F.action == "grant_admin"))
async def grant_admin(msg: Message):

    user = await user_repo.get_by_telegram_id(telegram_id=msg.from_user.id)

    if user and user.telegram_id in config.ADMINS_IDS:
        await msg.answer(text=_("already_admin").format(admin_id=user.telegram_id), show_alert=True)
        return

    reply_markup = await rm_constructor.back_button()
    await msg.answer(
        text=_("how_to_grant_admin_rights"),
        reply_markup=reply_markup,
        show_alert=True
    )


@router.callback_query(Action.filter(F.action == "get_me"))
async def get_me(call: CallbackQuery):
    reply_markup = await rm_constructor.back_button()
    await call.message.edit_text(
        text=_("me").format(from_user=call.from_user),
        reply_markup=reply_markup
    )
