from __future__ import annotations

import asyncio
import logging
import sys

from config import DISCORD_TOKEN, TELEGRAM_BOT_TOKEN, validate_env
from discord_client import DiscordGateway, DiscordRest
from telegram_bot import TelegramController, run_telegram_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("main")


async def main() -> None:
    errors = validate_env()
    if errors:
        for item in errors:
            logger.error(item)
        sys.exit(1)

    rest = DiscordRest(DISCORD_TOKEN)
    gateway = DiscordGateway(DISCORD_TOKEN, rest)
    controller = TelegramController(rest, gateway)

    gateway_task = asyncio.create_task(gateway.start(), name="discord-gateway")
    telegram_task = asyncio.create_task(
        run_telegram_bot(TELEGRAM_BOT_TOKEN, controller),
        name="telegram-bot",
    )

    try:
        done, pending = await asyncio.wait(
            {gateway_task, telegram_task},
            return_when=asyncio.FIRST_EXCEPTION,
        )
        for task in done:
            exc = task.exception()
            if exc:
                raise exc
    except KeyboardInterrupt:
        logger.info("Shutting down")
    finally:
        await gateway.stop()
        await rest.close()
        for task in (gateway_task, telegram_task):
            task.cancel()
        await asyncio.gather(gateway_task, telegram_task, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
