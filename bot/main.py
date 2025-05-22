from urllib.parse import urljoin  # noqa

import asyncio
import logging
import os.path

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import (
    Message,
)
from redis.asyncio.client import Redis


src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa

django.setup()
from django.conf import settings  # noqa


from users.models import User  # noqa

logger = logging.getLogger("django")


router = Router()

bot = Bot(token=settings.BOT_TOKEN)
from .middlewares import UserMiddleware  # noqa

storage = RedisStorage(
    Redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1"),
    # in case of redis you need to configure key builder
    key_builder=DefaultKeyBuilder(with_destiny=True),
)
dp = Dispatcher(storage=storage)


@router.message(CommandStart())
async def start_command(message: Message, user: User):
    logger.info(f"User {user} /start {message.text}")
    ref = message.text.replace("/start ", "").strip()
    if not user:
        user = await User.objects.from_tg(message.from_user, ref and ref)
        logger.info(f"User {user} was created")
        await message.reply("Welcome")
    else:
        logger.info(f"User {user} was found")
        if ref:
            user.referral_id = ref
            await user.asave(update_fields=["referral_id"])
        await message.reply("Welcome back")


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.include_router(router)

    dp.message.middleware(UserMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
