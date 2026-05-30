DISCORD AUTO-ANSWER BOT
Auto-replies on Discord | Control via Telegram


########################################
# ENGLISH
########################################

GitHub description

Discord auto-reply bot with Telegram remote control. Manage profile,
auto-replies, whitelist and blacklist from your phone.


What it does

When you are away, the bot replies on Discord for you. Full account
and auto-reply settings are available through a Telegram bot.


Features

  - Auto-reply in DMs and on mentions (toggle)
  - Custom reply text, delay, per-channel cooldown
  - Whitelist / blacklist by Discord user ID
  - Profile: username, display name, bio, status, avatar
  - Single config file: connection.py


Quick start

  1. Edit connection.py:

     DISCORD_TOKEN = "..."
     TELEGRAM_BOT_TOKEN = "..."
     TELEGRAM_ADMIN_IDS = [123456789]

  2. Install and run:

     pip install -r requirements.txt
     python main.py


Warning

Requires a Discord user token. May violate Discord ToS. Use at your own risk.


########################################
# RUSSIAN
########################################

Описание для GitHub

Discord-бот с автоответом и управлением через Telegram. Профиль,
автоответы, whitelist и blacklist - с телефона.


Для чего

Бот отвечает в Discord, пока ты офлайн. Управление через Telegram.


Возможности

  - Автоответ в ЛС и при упоминаниях
  - Свой текст, задержка, кулдаун
  - Whitelist / blacklist
  - Профиль и аватарка
  - connection.py для токенов


Быстрый старт

  pip install -r requirements.txt
  python main.py


Важно

User token Discord. Может нарушать ToS. На свой риск.


More commands: commands.txt
