import uuid
from telegram.ext import Updater, CommandHandler
from telegram import ChatAction

TOKEN = '6007897911:AAGgi7Ya7Gz7SNa8bjV31-4fMjguShjl3rU'

def buat_tautan(update, context):
    chat_id = update.effective_chat.id

    # Generate unique link
    unique_id = str(uuid.uuid4())
    channel_link = f"https://t.me/joinchat/{unique_id}"

    update.message.reply_text(f"Tautan channel baru: {channel_link}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("buat_tautan", buat_tautan))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
