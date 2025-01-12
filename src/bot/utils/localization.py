from aiogram.utils.i18n import I18n

i18n = I18n(path="../../locales", default_locale="en", domain="messages")


def get_i18n() -> I18n:
    return i18n
