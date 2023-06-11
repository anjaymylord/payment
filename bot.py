import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Inisialisasi token bot Telegram
telegram_token = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'
bot = telegram.Bot(token=telegram_token)

# Fungsi untuk menangani perintah /start
def start(update, context):
    update.message.reply_text('Halo! Untuk mengakses grup ini, silakan langganan ke saluran terlebih dahulu.')

# Fungsi untuk menangani pesan yang diterima dari pengguna
def handle_message(update, context):
    user_id = update.message.from_user.id
    channel_username = '@mediasayu'  # Ganti dengan username saluran yang diinginkan
    subscribed = bot.get_chat_member(channel_username, user_id).status == 'member'
    
    if subscribed:
        update.message.reply_text('Anda sudah berlangganan ke saluran. Selamat datang di grup!')
    else:
        update.message.reply_text('Silakan langganan ke saluran terlebih dahulu untuk mengakses grup.')

# Fungsi untuk menangani callback query
def handle_callback_query(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    message = query.message
    
    # Cek apakah pesan merupakan pesan forward
    if message.forward_from:
        bot.answer_callback_query(query.id, text='Anda tidak diizinkan meneruskan pesan ini.')
        # Jika pesan merupakan pesan forward, lakukan tindakan yang diinginkan (misalnya, hapus pesan)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    else:
        bot.answer_callback_query(query.id, text='Pesan tidak diteruskan.')

# Fungsi utama untuk menjalankan bot Telegram
def main():
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Handler perintah /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Handler pesan yang diterima
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)
    
    # Handler callback query
    callback_query_handler = CallbackQueryHandler(handle_callback_query)
    dispatcher.add_handler(callback_query_handler)
    
    updater.start_polling()
    updater.idle()

# Menjalankan bot Telegram
if __name__ == '__main__':
    main()
