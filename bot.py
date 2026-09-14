import os
import time
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise Exception("TELEGRAM_TOKEN غير موجود")

URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    return requests.get(URL + "getUpdates", params=params, timeout=40).json()

def send_message(chat_id, text):
    requests.post(
        URL + "sendMessage",
        data={"chat_id": chat_id, "text": text},
        timeout=20
    )

offset = None

while True:
    try:
        data = get_updates(offset)

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message", {})
            chat = message.get("chat", {})
            text = message.get("text", "")

            if text == "/start":
                send_message(
                    chat["id"],
                    "🔥 ملك الشورت\n\nالبوت شغال تمام\n\nاكتب /help"
                )

            elif text == "/help":
                send_message(
                    chat["id"],
                    "الأوامر الحالية:\n/start\n/help"
                )

        time.sleep(1)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)
