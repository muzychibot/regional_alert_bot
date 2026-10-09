import asyncio
import os

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiogram import Bot
from dotenv import load_dotenv
from aiohttp import web


# ============================================================
# 1. КОНФІГУРАЦІЯ
# ============================================================

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("TELETHON_SESSION")
BOT_TOKEN = os.getenv("bot_token")


# Перевіряємо змінні Railway
if not API_ID:
    raise ValueError("Не знайдено API_ID у Railway Variables.")

if not API_HASH:
    raise ValueError("Не знайдено API_HASH у Railway Variables.")

if not SESSION_STRING:
    raise ValueError("Не знайдено TELETHON_SESSION у Railway Variables.")

if not BOT_TOKEN:
    raise ValueError("Не знайдено bot_token у Railway Variables.")


# ============================================================
# 2. TELETHON STRING SESSION
# ============================================================

SESSION_STRING = SESSION_STRING.strip().strip('"').strip("'")


try:
    client = TelegramClient(
        StringSession(SESSION_STRING),
        API_ID,
        API_HASH
    )
except Exception as e:
    raise ValueError(
        f"Не вдалося прочитати TELETHON_SESSION: "
        f"{type(e).__name__}: {e}"
    )


# ============================================================
# 3. ДЖЕРЕЛО
# ============================================================

CHANNELS_TO_WATCH = ["airalarm_kyiv"]

STOP_WORDS = [
    "академ",
    "мостицька",
    "мостище",
]


# ============================================================
# 4. CHAT ID ТА КЛЮЧОВІ СЛОВА
# ============================================================

USERS = {

    628890725: [
        "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
        "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
        "міст",
        "мост",
        "мости",
        "соцмісто",
        "тец-6",
    ],

    475285184: [
        "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
         "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
          "міст",
        "мост",
        "мости",
         "соцмісто",
        "тец-6",
    ],

1018606307: [
        "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
     "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
      "міст",
        "мост",
        "мости",
     "соцмісто",
        "тец-6",
    ],

415630564: [
       "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
     "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
      "міст",
        "мост",
        "мости",
     "соцмісто",
        "тец-6",
    ],

1358472441: [
       "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
     "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
      "міст",
        "мост",
        "мости",
     "соцмісто",
        "тец-6",
    ],

8436451421: [
       "ракета",
        "лісовий",
        "воскресенка",
        "ракети",
        "балістика",
     "балістики",
        "онікс",
        "онікси",
        "калібр",
        "калібри",
        "циркон",
        "циркони",
        "кинджал",
        "крилата",
        "троя",
        "тец6",
        "троєщина",
        "лівобережний масив",
        "русанівка",
      "міст",
        "мост",
        "мости",
     "соцмісто",
        "тец-6",
    ],
    
    
    488055982: [
    "феофанія",
    "теремки",
    "новосілки",
    "чабани",
    "ракета",
    "гатне",
    "ракети",
    "балістика",
    "балістики",
    "онікс",
    "онікси",
    "калібр",
    "калібри",
    "циркон",
    "циркони",
    "кинджал",
    "крилата",
 ],

    # 123456789: [
    #     "ключове слово",
    #     "ключове слово",
    # ],

    # 123456789: [
    #     "ключове слово",
    #     "ключове слово",
    # ],

}


# ============================================================
# 5. ЧЕРГА ПОВІДОМЛЕНЬ
# ============================================================

message_queue = asyncio.Queue()


# ============================================================
# 6. СЛУХАЄМО airalarm_kyiv
# ============================================================

@client.on(events.NewMessage(chats=CHANNELS_TO_WATCH))
async def handler(event):

    message_text = event.raw_text

    if not message_text:
        return

    text_lower = message_text.lower()

        # Не пересилаємо повідомлення зі стоп-словами
    if any(word in text_lower for word in STOP_WORDS):
        print("[!] Повідомлення заблоковано стоп-словом.")
        return

    for chat_id, keywords in USERS.items():

        if any(keyword.lower() in text_lower for keyword in keywords):

            print(
                f"[!] Знайдено повідомлення для "
                f"Telegram ID {chat_id}."
            )

            text_to_send = (
                "🔔 Повітряна тривога Київ\n"
                "━━━━━━━━━━━━━━━\n\n"
                f"{message_text}"
            )

            await message_queue.put(
                (chat_id, text_to_send)
            )


# ============================================================
# 7. ВІДПРАВЛЕННЯ ПОВІДОМЛЕНЬ
# ============================================================

async def message_sender_worker():

    bot = Bot(token=BOT_TOKEN)

    print("[+] Відправник особистих повідомлень запущений.")

    try:

        while True:

            chat_id, text = await message_queue.get()

            try:

                await bot.send_message(
                    chat_id=chat_id,
                    text=text
                )

                print(
                    f"[+] Повідомлення успішно надіслано "
                    f"в Telegram ID {chat_id}"
                )

            except Exception as e:

                print(
                    f"[-] Помилка надсилання повідомлення "
                    f"в Telegram ID {chat_id}: "
                    f"{type(e).__name__}: {e}"
                )

            finally:

                message_queue.task_done()

            await asyncio.sleep(1)

    except asyncio.CancelledError:

        print("[*] Відправник повідомлень зупиняється.")
        raise

    finally:

        await bot.session.close()


# ============================================================
# 8. WEB-СЕРВЕР ДЛЯ RAILWAY
# ============================================================

async def handle_web(request):

    return web.Response(
        text="Regional Alert Bot працює."
    )


# ============================================================
# 9. ЗАПУСК TELETHON
# ============================================================

async def start_telegram_background(app):

    print("[+] Підключаємося до Telegram...")

    await client.connect()

    if not await client.is_user_authorized():

        await client.disconnect()

        raise RuntimeError(
            "TELETHON_SESSION існує, але Telegram її не авторизував."
        )

    me = await client.get_me()

    print(
        f"[+] Telegram авторизація успішна. "
        f"User ID: {me.id}"
    )

    print(
        "[+] Слухаємо канал airalarm_kyiv "
        "та перевіряємо ключові слова."
    )

    print(
        f"[+] Налаштовано отримувачів: {len(USERS)}"
    )

    app["tg_task"] = asyncio.create_task(
        client.run_until_disconnected()
    )

    app["sender_task"] = asyncio.create_task(
        message_sender_worker()
    )


# ============================================================
# 10. КОРЕКТНЕ ЗАВЕРШЕННЯ
# ============================================================

async def stop_telegram_background(app):

    print("[*] Зупиняємо Telegram-клієнт...")

    sender_task = app.get("sender_task")

    if sender_task:

        sender_task.cancel()

        try:
            await sender_task
        except asyncio.CancelledError:
            pass

    tg_task = app.get("tg_task")

    if tg_task:

        tg_task.cancel()

        try:
            await tg_task
        except asyncio.CancelledError:
            pass

    if client.is_connected():
        await client.disconnect()


# ============================================================
# 11. AIOHTTP APP
# ============================================================

def make_app():

    app = web.Application()

    app.router.add_get("/", handle_web)

    app.on_startup.append(start_telegram_background)
    app.on_cleanup.append(stop_telegram_background)

    return app


# ============================================================
# 12. ЗАПУСК НА RAILWAY
# ============================================================

if __name__ == "__main__":

    port = int(os.getenv("PORT", "8080"))

    print(f"[+] Запускаємо Railway web server на порту {port}.")

    web.run_app(
        make_app(),
        host="0.0.0.0",
        port=port
    )
