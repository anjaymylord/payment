from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta

TOKEN = '6007897911:AAGgi7Ya7Gz7SNa8bjV31-4fMjguShjl3rU'

def buat_tautan(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Cek apakah pengguna telah memiliki tautan channel sebelumnya
    if user_id in context.user_data:
        # Cek apakah tautan channel masih berlaku
        if context.user_data[user_id]['expiration'] > datetime.now():
            tautan = context.user_data[user_id]['tautan']
            update.message.reply_text(f"Anda sudah memiliki tautan channel yang masih berlaku: {tautan}")
            return

    # Buat tautan channel baru
    channel_link = "https://t.me/+zn9YABu82_M3M2I5"
    expiration_time = datetime.now() + timedelta(minutes=1)
    context.user_data[user_id] = {'tautan': channel_link, 'expiration': expiration_time}

    update.message.reply_text(f"Anda telah membuat tautan channel: {channel_link}. Tautan akan kedaluwarsa dalam 1 menit.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("buat_tautan", buat_tautan))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
