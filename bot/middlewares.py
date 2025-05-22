from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from users.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        telegram_id = None
        try:
            telegram_id = event.chat.id
        except AttributeError:
            pass
        try:
            telegram_id = event.from_user.id
        except AttributeError:
            pass
        try:
            telegram_id = event.message.from_user.id
        except AttributeError:
            pass

        if telegram_id:
            data["user"] = (
                await User.objects.filter(telegram_id=telegram_id)
                .select_related()
                .afirst()
            )
        return await handler(event, data)
