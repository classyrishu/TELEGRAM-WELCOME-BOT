import os
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, ContextTypes
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")
WELCOME_MSG = os.getenv("WELCOME_MSG", "Welcome bhai! 🔥")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member.new_chat_member.status == "member":
        name = update.chat_member.new_chat_member.user.first_name
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=WELCOME_MSG.replace("{name}", name)
        )

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
