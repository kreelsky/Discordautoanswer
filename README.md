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

--------------------------------------------------------------------------------
Only users listed in TELEGRAM_ADMIN_IDS can use these commands.
Только пользователи из TELEGRAM_ADMIN_IDS могут использовать эти команды.

--------------------------------------------------------------------------------
ENGLISH
--------------------------------------------------------------------------------

/start, /help
    Show command list.

/status
    Show current auto-reply settings (on/off, message, delay, cooldown, DMs, mentions, whitelist/blacklist counts).

/profile
    Show Discord profile info (id, username, display name, bio).

/autoreply on
    Enable auto-reply.

/autoreply off
    Disable auto-reply.

/setmessage <text>
    Set the auto-reply message text.

/setdelay <seconds>
    Set delay before sending a reply (0 or higher).

/setcooldown <seconds>
    Set per-channel cooldown between replies (0 or higher).

/dms on
    Enable auto-reply in direct messages.

/dms off
    Disable auto-reply in direct messages.

/mentions on
    Enable auto-reply when you are mentioned in a server channel.

/mentions off
    Disable auto-reply on mentions.

/username <name>
    Change Discord username.

/displayname <name>
    Change Discord display name (global name).

/displayname clear
    Clear Discord display name.

/bio <text>
    Change Discord profile bio.

/customstatus <text>
    Set Discord custom status text.

/customstatus clear
    Clear Discord custom status.

/avatar
    Change Discord avatar. Send a photo with this command, or reply to a photo with /avatar.

/whitelist list
    List whitelisted Discord user IDs.

/whitelist add <id>
    Add a Discord user ID to the whitelist (only these users get replies if whitelist is not empty).

/whitelist remove <id>
    Remove a Discord user ID from the whitelist.

/blacklist list
    List blacklisted Discord user IDs.

/blacklist add <id>
    Add a Discord user ID to the blacklist (they will never get auto-replies).

/blacklist remove <id>
    Remove a Discord user ID from the blacklist.

--------------------------------------------------------------------------------
РУССКИЙ
--------------------------------------------------------------------------------

/start, /help
    Показать список команд.

/status
    Показать текущие настройки автоответа (вкл/выкл, текст, задержка, кулдаун, ЛС, упоминания, кол-во в whitelist/blacklist).

/profile
    Показать профиль Discord (id, username, отображаемое имя, bio).

/autoreply on
    Включить автоответ.

/autoreply off
    Выключить автоответ.

/setmessage <текст>
    Задать текст автоответа.

/setdelay <секунды>
    Задержка перед отправкой ответа (0 и больше).

/setcooldown <секунды>
    Кулдаун между ответами в одном канале (0 и больше).

/dms on
    Включить автоответ в личных сообщениях.

/dms off
    Выключить автоответ в личных сообщениях.

/mentions on
    Включить автоответ при упоминании на сервере.

/mentions off
    Выключить автоответ при упоминании.

/username <имя>
    Сменить username в Discord.

/displayname <имя>
    Сменить отображаемое имя (global name).

/displayname clear
    Убрать отображаемое имя.

/bio <текст>
    Сменить описание профиля (bio).

/customstatus <текст>
    Установить кастомный статус.

/customstatus clear
    Убрать кастомный статус.

/avatar
    Сменить аватарку. Отправь фото вместе с командой или ответь /avatar на фото.

/whitelist list
    Список ID в whitelist.

/whitelist add <id>
    Добавить Discord user id в whitelist (если список не пуст — ответы только им).

/whitelist remove <id>
    Удалить id из whitelist.

/blacklist list
    Список ID в blacklist.

/blacklist add <id>
    Добавить id в blacklist (автоответ им не отправляется).

/blacklist remove <id>
    Удалить id из blacklist.

================================================================================
