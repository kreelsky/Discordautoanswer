================================================================================
                         DISCORD AUTO-ANSWER BOT
                    Discord Auto-Answer + Telegram Control
================================================================================


--------------------------------------------------------------------------------
  ENGLISH
--------------------------------------------------------------------------------

  SHORT DESCRIPTION
  -------------------------------
  Discord auto-reply bot with Telegram remote control. Manage profile,
  auto-replies, whitelist/blacklist from your phone.


  ABOUT
  -----
  This bot automates Discord replies when you are away and lets you manage
  your account from Telegram.

  Features
    * Auto-reply     — custom message in DMs and on mentions (optional)
    * Delay          — wait before sending a reply
    * Cooldown       — limit how often the same channel gets a reply
    * Telegram panel — enable/disable auto-reply, edit message, lists
    * Profile        — username, display name, bio, status, avatar
    * Access control — whitelist and blacklist by Discord user ID
    * Easy setup     — all tokens in one file: connection.py

  Use case
    You are offline but want Discord to answer for you. Change settings
    and profile from Telegram without opening the Discord client.


  CONNECTION
  ----------
  Edit connection.py:

    DISCORD_TOKEN       — your Discord user token
    TELEGRAM_BOT_TOKEN  — token from @BotFather
    TELEGRAM_ADMIN_IDS  — Telegram user IDs allowed to control the bot

  Run:

    pip install -r requirements.txt
    python main.py


  NOTE
  ----
  Uses a Discord user token. This may violate Discord Terms of Service.
  Use at your own risk.


--------------------------------------------------------------------------------
  РУССКИЙ
--------------------------------------------------------------------------------

  ------------------------------
  Discord-бот с автоответом и управлением через Telegram. Профиль,
  автоответы, whitelist/blacklist — с телефона.


  О ПРОЕКТЕ
  ---------
  Бот автоматически отвечает в Discord, когда ты недоступен, и даёт
  управлять аккаунтом через Telegram.

  Возможности
    * Автоответ      — свой текст в ЛС и при упоминаниях (опционально)
    * Задержка       — пауза перед отправкой ответа
    * Кулдаун        — ограничение частоты ответов в одном канале
    * Панель в TG    — вкл/выкл автоответ, смена текста, списки
    * Профиль        — username, имя, bio, статус, аватарка
    * Списки         — whitelist и blacklist по Discord user id
    * Подключение    — все токены в одном файле: connection.py

  Зачем
    Discord отвечает за тебя, пока ты офлайн. Настройки и профиль —
    из Telegram, без клиента Discord.


  ПОДКЛЮЧЕНИЕ
  -----------
  Заполни connection.py:

    DISCORD_TOKEN       — user token Discord
    TELEGRAM_BOT_TOKEN  — токен от @BotFather
    TELEGRAM_ADMIN_IDS  — Telegram id тех, кто может управлять ботом

  Запуск:

    pip install -r requirements.txt
    python main.py


  ВАЖНО
  -----
  Используется user token Discord. Это может нарушать Terms of Service.
  Используй на свой риск.


================================================================================
  See also: commands.txt — full list of Telegram commands
================================================================================
