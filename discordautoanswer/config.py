from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).resolve().parent / "data"
SETTINGS_PATH = DATA_DIR / "settings.json"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

_raw_admin_ids = os.getenv("TELEGRAM_ADMIN_IDS", "")
TELEGRAM_ADMIN_IDS: set[int] = {
    int(item.strip())
    for item in _raw_admin_ids.split(",")
    if item.strip().isdigit()
}

DISCORD_API = "https://discord.com/api/v10"
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"


@dataclass
class Settings:
    auto_reply_enabled: bool = True
    auto_reply_message: str = "Hey, I am away right now. I will get back to you soon."
    auto_reply_delay_sec: float = 1.5
    reply_in_dms: bool = True
    reply_on_mention: bool = False
    whitelist: list[int] = field(default_factory=list)
    blacklist: list[int] = field(default_factory=list)
    cooldown_sec: float = 60.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Settings:
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    ensure_data_dir()
    if not SETTINGS_PATH.exists():
        settings = Settings()
        save_settings(settings)
        return settings
    with SETTINGS_PATH.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return Settings.from_dict(raw)


def save_settings(settings: Settings) -> None:
    ensure_data_dir()
    with SETTINGS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(settings.to_dict(), fh, indent=2, ensure_ascii=False)


def validate_env() -> list[str]:
    errors: list[str] = []
    if not DISCORD_TOKEN:
        errors.append("DISCORD_TOKEN is missing")
    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is missing")
    if not TELEGRAM_ADMIN_IDS:
        errors.append("TELEGRAM_ADMIN_IDS is missing or invalid")
    return errors
