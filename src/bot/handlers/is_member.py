from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import ChatMemberUpdated

from src.bot.repositories.user import UserRepository

router = Router(name=__name__)

user_repo = UserRepository()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    """
    Updates the status of a route who blocked the bot in the chat.

    :param event: The ChatMemberUpdated event object containing information about the chat member and their status.
    """
    await user_repo.update(telegram_id=event.from_user.id, is_active=False)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    """
    Updates the status of a route who unblocked the bot and rejoined the chat.

    :param event: The ChatMemberUpdated event object containing information about the chat member and their status.
    """
    await user_repo.update(telegram_id=event.from_user.id, is_active=True)
