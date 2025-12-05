from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

def chat_with_ai(update: Update, context: CallbackContext):
    user_msg = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_msg}]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = res.json()['choices'][0]['message']['content']
    except:
        reply = "متأسفم، مشکلی در ارتباط با هوش مصنوعی پیش اومده."
    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat_with_ai))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()