from __future__ import annotations

import asyncio
import base64
import json
import logging
import time
from typing import Any, Callable, Awaitable

import aiohttp
import websockets
from websockets.exceptions import ConnectionClosed

from config import DISCORD_API, DISCORD_TOKEN, GATEWAY_URL, Settings, load_settings, save_settings

logger = logging.getLogger(__name__)

SettingsCallback = Callable[[Settings], Awaitable[None] | None]


class DiscordRest:
    def __init__(self, token: str) -> None:
        self._token = token
        self._session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": self._token,
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (compatible; DiscordClient/1.0)",
                }
            )

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        if not self._session:
            await self.start()
        assert self._session is not None
        url = f"{DISCORD_API}{path}"
        async with self._session.request(method, url, **kwargs) as resp:
            text = await resp.text()
            if resp.status >= 400:
                raise RuntimeError(f"Discord API {method} {path} -> {resp.status}: {text}")
            if not text:
                return None
            return json.loads(text)

    async def get_me(self) -> dict:
        return await self._request("GET", "/users/@me")

    async def get_profile(self) -> dict:
        return await self._request("GET", "/users/@me/profile")

    async def patch_me(self, payload: dict) -> dict:
        return await self._request("PATCH", "/users/@me", json=payload)

    async def set_avatar(self, image_bytes: bytes) -> dict:
        encoded = base64.b64encode(image_bytes).decode("ascii")
        mime = "image/png"
        if image_bytes[:3] == b"\xff\xd8\xff":
            mime = "image/jpeg"
        elif image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
            mime = "image/webp"
        data_uri = f"data:{mime};base64,{encoded}"
        return await self.patch_me({"avatar": data_uri})

    async def set_username(self, username: str) -> dict:
        return await self.patch_me({"username": username})

    async def set_global_name(self, global_name: str | None) -> dict:
        return await self.patch_me({"global_name": global_name})

    async def set_bio(self, bio: str) -> dict:
        return await self._request("PATCH", "/users/@me/profile", json={"bio": bio})

    async def set_custom_status(self, text: str | None, emoji_name: str | None = None) -> dict:
        custom_status: dict[str, Any] | None = None
        if text:
            custom_status = {"text": text}
            if emoji_name:
                custom_status["emoji_name"] = emoji_name
        return await self._request(
            "PATCH",
            "/users/@me/settings",
            json={"custom_status": custom_status},
        )

    async def send_message(self, channel_id: int, content: str) -> dict:
        return await self._request(
            "POST",
            f"/channels/{channel_id}/messages",
            json={"content": content},
        )


class DiscordGateway:
    def __init__(self, token: str, rest: DiscordRest) -> None:
        self._token = token
        self._rest = rest
        self._settings = load_settings()
        self._reply_cooldown: dict[int, float] = {}
        self._running = False
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._heartbeat_task: asyncio.Task | None = None
        self._sequence: int | None = None
        self._session_id: str | None = None
        self._on_settings_change: SettingsCallback | None = None

    @property
    def settings(self) -> Settings:
        return self._settings

    def update_settings(self, settings: Settings) -> None:
        self._settings = settings
        save_settings(settings)

    def on_settings_change(self, callback: SettingsCallback) -> None:
        self._on_settings_change = callback

    async def reload_settings(self) -> None:
        self._settings = load_settings()
        if self._on_settings_change:
            result = self._on_settings_change(self._settings)
            if asyncio.iscoroutine(result):
                await result

    async def start(self) -> None:
        self._running = True
        await self._rest.start()
        while self._running:
            try:
                await self._connect_loop()
            except ConnectionClosed as exc:
                logger.warning("Gateway closed: %s", exc)
            except Exception:
                logger.exception("Gateway error")
            if self._running:
                await asyncio.sleep(5)

    async def stop(self) -> None:
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._ws:
            await self._ws.close()

    async def _connect_loop(self) -> None:
        async with websockets.connect(GATEWAY_URL, max_size=2**24) as ws:
            self._ws = ws
            await self._handle_connection(ws)

    async def _handle_connection(self, ws: websockets.WebSocketClientProtocol) -> None:
        while self._running:
            raw = await ws.recv()
            payload = json.loads(raw)
            op = payload.get("op")
            event = payload.get("t")
            data = payload.get("d")
            seq = payload.get("s")
            if seq is not None:
                self._sequence = seq

            if op == 10:
                await self._on_hello(ws, data)
            elif op == 0 and event == "READY":
                self._session_id = data.get("session_id")
                user = data.get("user", {})
                logger.info("Logged in as %s", user.get("username"))
            elif op == 0 and event == "MESSAGE_CREATE":
                await self._on_message(data)
            elif op == 7:
                logger.info("Reconnect requested")
                break
            elif op == 9:
                logger.warning("Invalid session")
                self._session_id = None
                await self._identify(ws)
            elif op == 11:
                pass

    async def _on_hello(self, ws: websockets.WebSocketClientProtocol, data: dict) -> None:
        interval_ms = data["heartbeat_interval"]
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop(ws, interval_ms))
        if self._session_id:
            await self._resume(ws)
        else:
            await self._identify(ws)

    async def _heartbeat_loop(
        self, ws: websockets.WebSocketClientProtocol, interval_ms: int
    ) -> None:
        try:
            while True:
                await asyncio.sleep(interval_ms / 1000)
                await ws.send(json.dumps({"op": 1, "d": self._sequence}))
        except asyncio.CancelledError:
            return

    async def _identify(self, ws: websockets.WebSocketClientProtocol) -> None:
        await ws.send(
            json.dumps(
                {
                    "op": 2,
                    "d": {
                        "token": self._token,
                        "capabilities": 16381,
                        "properties": {
                            "os": "Windows",
                            "browser": "Discord Client",
                            "device": "",
                            "system_locale": "en-US",
                        },
                        "presence": {
                            "status": "online",
                            "since": 0,
                            "activities": [],
                            "afk": False,
                        },
                        "compress": False,
                        "client_state": {
                            "guild_versions": {},
                            "highest_last_message_id": "0",
                            "read_state_version": 0,
                            "user_guild_settings_version": -1,
                            "user_settings_version": -1,
                            "private_channels_version": "0",
                        },
                    },
                }
            )
        )

    async def _resume(self, ws: websockets.WebSocketClientProtocol) -> None:
        await ws.send(
            json.dumps(
                {
                    "op": 6,
                    "d": {
                        "token": self._token,
                        "session_id": self._session_id,
                        "seq": self._sequence,
                    },
                }
            )
        )

    async def _on_message(self, data: dict) -> None:
        author_id = int(data["author"]["id"])
        if data.get("author", {}).get("bot"):
            return

        me = await self._rest.get_me()
        if str(author_id) == me["id"]:
            return

        channel_id = int(data["channel_id"])
        guild_id = data.get("guild_id")
        is_dm = guild_id is None
        content = data.get("content", "")
        mentioned = f"<@{me['id']}>" in content

        if not self._settings.auto_reply_enabled:
            return
        if is_dm and not self._settings.reply_in_dms:
            return
        if not is_dm and self._settings.reply_on_mention and not mentioned:
            return
        if not is_dm and not self._settings.reply_on_mention:
            return

        if self._settings.whitelist and author_id not in self._settings.whitelist:
            return
        if author_id in self._settings.blacklist:
            return

        now = time.monotonic()
        last = self._reply_cooldown.get(channel_id, 0.0)
        if now - last < self._settings.cooldown_sec:
            return

        self._reply_cooldown[channel_id] = now
        if self._settings.auto_reply_delay_sec > 0:
            await asyncio.sleep(self._settings.auto_reply_delay_sec)

        try:
            await self._rest.send_message(channel_id, self._settings.auto_reply_message)
            logger.info("Auto-replied in channel %s", channel_id)
        except Exception:
            logger.exception("Failed to send auto-reply")
