from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'

def start(update: Update, context):
    chat_id = update.message.chat_id
    channel_link = 'https://t.me/+0g8h6exjM942ZGVl'  # Ganti dengan tautan channel Anda
    payment_link = 'https://link.dana.id/qr/6o3bdg13'  # Ganti dengan tautan pembayaran Anda
    message = f'Silakan bayar untuk bergabung dengan channel kami: {payment_link}'
    bot.send_message(chat_id=chat_id, text=message)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    main()
