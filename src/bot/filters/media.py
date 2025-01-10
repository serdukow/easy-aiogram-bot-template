from aiogram.filters import BaseFilter
from aiogram.types import Message, ContentType


class MediaFilter(BaseFilter):
    """
    MediaFilter is a custom filter that checks if a message contains specific types of media.

    This filter inspects the `content_type` of the incoming `Message` object and returns `True`
    if it matches one of the allowed media types. Otherwise, it returns `False`.

    Supported media types:
        - ANIMATION
        - AUDIO
        - DOCUMENT
        - PHOTO
        - VIDEO
        - VOICE

    Usage:
        Apply this filter to message handlers where you want to process only media messages.

    Example:
        @router.message(MediaFilter())
        async def handle_media(message: Message):
            await message.answer("You sent a valid media type!")
    """
    async def __call__(self, message: Message) -> bool:
        return message.content_type in (
            ContentType.ANIMATION, ContentType.AUDIO, ContentType.DOCUMENT,
            ContentType.PHOTO, ContentType.VIDEO, ContentType.VOICE
        )
