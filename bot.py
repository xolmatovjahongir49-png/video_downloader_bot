import os
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.getenv("8369155374:AAG4hRhRCy0EPeDsMTs2AXE-bM_-GJlpvpQ")

def start(update, context):
    update.message.reply_text("Assalomu alaykum! Bot ishlayapti 😊")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
