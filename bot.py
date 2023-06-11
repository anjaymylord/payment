import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime, timedelta

TOKEN = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    chat_id = update.message.chat_id

    # Buat tautan unik dengan menambahkan timestamp saat ini
    link = f"https://t.me/paymentryubot?start=unique_code_{datetime.now().timestamp()}"

    # Tambahkan tautan ke keyboard inline
    keyboard = [[InlineKeyboardButton("Join Channel", url=link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Kirim pesan dengan keyboard inline
    response_message = "Klik tombol berikut untuk bergabung dengan channel:"
    context.bot.send_message(chat_id=chat_id, text=response_message, reply_markup=reply_markup)

def join_channel(update, context):
    chat_id = update.message.chat_id

    # Periksa apakah tautan masih berlaku
    link_timestamp = float(update.message.text.split('_')[-1])
    expiration_time = datetime.fromtimestamp(link_timestamp) + timedelta(hours=1)
    current_time = datetime.now()

    if current_time < expiration_time:
        response_message = "Selamat bergabung dengan channel!"
        # Lakukan tindakan lain yang diinginkan, misalnya menambahkan pengguna ke database
    else:
        response_message = "Maaf, tautan sudah kedaluwarsa."

    context.bot.send_message(chat_id=chat_id, text=response_message)

start_handler = CommandHandler('start', start)
join_channel_handler = MessageHandler(Filters.text & Filters.regex(r'^unique_code_'), join_channel)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(join_channel_handler)

updater.start_polling()
