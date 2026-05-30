from __future__ import annotations

import io
import logging
from typing import TYPE_CHECKING

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import TELEGRAM_ADMIN_IDS, Settings, load_settings, save_settings

if TYPE_CHECKING:
    from discord_client import DiscordGateway, DiscordRest

logger = logging.getLogger(__name__)
router = Router()


def _is_admin(user_id: int | None) -> bool:
    return user_id is not None and user_id in TELEGRAM_ADMIN_IDS


def _deny(message: Message) -> bool:
    if not _is_admin(message.from_user.id if message.from_user else None):
        return True
    return False


def _fmt_settings(settings: Settings) -> str:
    return (
        f"auto_reply: {'on' if settings.auto_reply_enabled else 'off'}\n"
        f"message: {settings.auto_reply_message}\n"
        f"delay: {settings.auto_reply_delay_sec}s\n"
        f"cooldown: {settings.cooldown_sec}s\n"
        f"dms: {'on' if settings.reply_in_dms else 'off'}\n"
        f"mentions: {'on' if settings.reply_on_mention else 'off'}\n"
        f"whitelist: {len(settings.whitelist)} ids\n"
        f"blacklist: {len(settings.blacklist)} ids"
    )


class TelegramController:
    def __init__(self, rest: DiscordRest, gateway: DiscordGateway) -> None:
        self.rest = rest
        self.gateway = gateway

    async def apply_settings(self, settings: Settings) -> None:
        self.gateway.update_settings(settings)


def setup_handlers(controller: TelegramController) -> Router:
    @router.message(Command("start", "help"))
    async def cmd_help(message: Message) -> None:
        if _deny(message):
            return
        text = (
            "Discord remote control\n\n"
            "/status - show config\n"
            "/profile - show discord profile\n"
            "/autoreply on|off\n"
            "/setmessage <text>\n"
            "/setdelay <seconds>\n"
            "/setcooldown <seconds>\n"
            "/dms on|off\n"
            "/mentions on|off\n"
            "/username <name>\n"
            "/displayname <name|clear>\n"
            "/bio <text>\n"
            "/customstatus <text|clear>\n"
            "/avatar - send a photo with this command or reply to one\n"
            "/whitelist add|remove|list [id]\n"
            "/blacklist add|remove|list [id]"
        )
        await message.answer(text)

    @router.message(Command("status"))
    async def cmd_status(message: Message) -> None:
        if _deny(message):
            return
        settings = load_settings()
        await message.answer(_fmt_settings(settings))

    @router.message(Command("profile"))
    async def cmd_profile(message: Message) -> None:
        if _deny(message):
            return
        try:
            user = await controller.rest.get_me()
            try:
                bio_data = await controller.rest.get_profile()
            except Exception:
                bio_data = {}
            lines = [
                f"id: {user.get('id')}",
                f"username: {user.get('username')}",
                f"display: {user.get('global_name')}",
                f"bio: {bio_data.get('bio', '')}",
            ]
            await message.answer("\n".join(lines))
        except Exception as exc:
            await message.answer(f"error: {exc}")

    @router.message(Command("autoreply"))
    async def cmd_autoreply(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        arg = (command.args or "").strip().lower()
        settings = load_settings()
        if arg == "on":
            settings.auto_reply_enabled = True
        elif arg == "off":
            settings.auto_reply_enabled = False
        else:
            await message.answer("usage: /autoreply on|off")
            return
        save_settings(settings)
        await controller.apply_settings(settings)
        await message.answer(_fmt_settings(settings))

    @router.message(Command("setmessage"))
    async def cmd_setmessage(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        text = (command.args or "").strip()
        if not text:
            await message.answer("usage: /setmessage <text>")
            return
        settings = load_settings()
        settings.auto_reply_message = text
        save_settings(settings)
        await controller.apply_settings(settings)
        await message.answer("message updated")

    @router.message(Command("setdelay"))
    async def cmd_setdelay(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        raw = (command.args or "").strip()
        try:
            value = float(raw)
        except ValueError:
            await message.answer("usage: /setdelay <seconds>")
            return
        settings = load_settings()
        settings.auto_reply_delay_sec = max(0.0, value)
        save_settings(settings)
        await controller.apply_settings(settings)
        await message.answer(f"delay: {settings.auto_reply_delay_sec}s")

    @router.message(Command("setcooldown"))
    async def cmd_setcooldown(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        raw = (command.args or "").strip()
        try:
            value = float(raw)
        except ValueError:
            await message.answer("usage: /setcooldown <seconds>")
            return
        settings = load_settings()
        settings.cooldown_sec = max(0.0, value)
        save_settings(settings)
        await controller.apply_settings(settings)
        await message.answer(f"cooldown: {settings.cooldown_sec}s")

    async def _toggle_flag(
        message: Message, command: CommandObject, field: str, usage: str
    ) -> None:
        if _deny(message):
            return
        arg = (command.args or "").strip().lower()
        settings = load_settings()
        if arg == "on":
            setattr(settings, field, True)
        elif arg == "off":
            setattr(settings, field, False)
        else:
            await message.answer(f"usage: {usage}")
            return
        save_settings(settings)
        await controller.apply_settings(settings)
        await message.answer(_fmt_settings(settings))

    @router.message(Command("dms"))
    async def cmd_dms(message: Message, command: CommandObject) -> None:
        await _toggle_flag(message, command, "reply_in_dms", "/dms on|off")

    @router.message(Command("mentions"))
    async def cmd_mentions(message: Message, command: CommandObject) -> None:
        await _toggle_flag(message, command, "reply_on_mention", "/mentions on|off")

    @router.message(Command("username"))
    async def cmd_username(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        name = (command.args or "").strip()
        if not name:
            await message.answer("usage: /username <name>")
            return
        try:
            user = await controller.rest.set_username(name)
            await message.answer(f"username: {user.get('username')}")
        except Exception as exc:
            await message.answer(f"error: {exc}")

    @router.message(Command("displayname"))
    async def cmd_displayname(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        name = (command.args or "").strip()
        if not name:
            await message.answer("usage: /displayname <name|clear>")
            return
        value = None if name.lower() == "clear" else name
        try:
            user = await controller.rest.set_global_name(value)
            await message.answer(f"display: {user.get('global_name')}")
        except Exception as exc:
            await message.answer(f"error: {exc}")

    @router.message(Command("bio"))
    async def cmd_bio(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        bio = (command.args or "").strip()
        if not bio:
            await message.answer("usage: /bio <text>")
            return
        try:
            await controller.rest.set_bio(bio)
            await message.answer("bio updated")
        except Exception as exc:
            await message.answer(f"error: {exc}")

    @router.message(Command("customstatus"))
    async def cmd_customstatus(message: Message, command: CommandObject) -> None:
        if _deny(message):
            return
        text = (command.args or "").strip()
        status = None if text.lower() == "clear" else text
        try:
            await controller.rest.set_custom_status(status)
            await message.answer("custom status updated" if status else "custom status cleared")
        except Exception as exc:
            await message.answer(f"error: {exc}")

    @router.message(Command("avatar"))
    async def cmd_avatar(message: Message, bot: Bot) -> None:
        if _deny(message):
            return
        photo = None
        if message.photo:
            photo = message.photo[-1]
        elif message.reply_to_message and message.reply_to_message.photo:
            photo = message.reply_to_message.photo[-1]
        if not photo:
            await message.answer("send /avatar with a photo or reply to one")
            return
        try:
            file = await bot.get_file(photo.file_id)
            assert file.file_path
            buffer = io.BytesIO()
            await bot.download_file(file.file_path, buffer)
            await controller.rest.set_avatar(buffer.getvalue())
            await message.answer("avatar updated")
        except Exception as exc:
            await message.answer(f"error: {exc}")

    async def _list_handler(
        message: Message,
        command: CommandObject,
        field: str,
        label: str,
    ) -> None:
        if _deny(message):
            return
        parts = (command.args or "").strip().split()
        settings = load_settings()
        items: list[int] = getattr(settings, field)

        if not parts or parts[0] == "list":
            if not items:
                await message.answer(f"{label}: empty")
                return
            await message.answer(f"{label}:\n" + "\n".join(str(i) for i in items))
            return

        action = parts[0].lower()
        if action in {"add", "remove"} and len(parts) < 2:
            await message.answer(f"usage: /{label} {action} <discord_user_id>")
            return
        if len(parts) >= 2 and not parts[1].isdigit():
            await message.answer("id must be numeric")
            return

        if action == "add":
            uid = int(parts[1])
            if uid not in items:
                items.append(uid)
            save_settings(settings)
            await controller.apply_settings(settings)
            await message.answer(f"added {uid}")
        elif action == "remove":
            uid = int(parts[1])
            if uid in items:
                items.remove(uid)
            save_settings(settings)
            await controller.apply_settings(settings)
            await message.answer(f"removed {uid}")
        else:
            await message.answer(f"usage: /{label} add|remove|list [id]")

    @router.message(Command("whitelist"))
    async def cmd_whitelist(message: Message, command: CommandObject) -> None:
        await _list_handler(message, command, "whitelist", "whitelist")

    @router.message(Command("blacklist"))
    async def cmd_blacklist(message: Message, command: CommandObject) -> None:
        await _list_handler(message, command, "blacklist", "blacklist")

    @router.message(F.text)
    async def ignore_unknown(message: Message) -> None:
        if _deny(message):
            return

    return router


async def run_telegram_bot(token: str, controller: TelegramController) -> None:
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(setup_handlers(controller))
    await dp.start_polling(bot)
