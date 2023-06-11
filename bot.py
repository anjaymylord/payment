import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Inisialisasi token bot Telegram
telegram_token = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'
bot = telegram.Bot(token=telegram_token)

# Fungsi untuk menangani perintah /start
def start(update, context):
    update.message.reply_text('Halo! Untuk bergabung dengan grup, silakan bergabung dengan saluran terlebih dahulu.')

# Fungsi untuk menangani pesan media yang diterima
def handle_media(update, context):
    # Cek apakah pengirim pesan adalah admin atau pemilik bot
    if update.message.from_user.id in [1931366417, 1837975267]:  # Ganti admin_id dan owner_id dengan ID yang sesuai
        # Cek apakah pesan adalah media (gambar, video, dll.)
        if update.message.photo:
            media_file_id = update.message.photo[-1].file_id
            media_link = bot.get_file(media_file_id).file_path
            update.message.reply_text(f"Berikut adalah tautan untuk media yang dikirim: {media_link}")
        elif update.message.video:
            media_file_id = update.message.video.file_id
            media_link = bot.get_file(media_file_id).file_path
            update.message.reply_text(f"Berikut adalah tautan untuk video yang dikirim: {media_link}")
        # Tambahkan kondisi lainnya sesuai dengan jenis media yang ingin Anda dukung
    else:
        channel_username = '@mediasayu'  # Ganti dengan username channel yang diinginkan
        button = InlineKeyboardButton('Bergabung ke Channel', url=f'https://t.me/mediasayu')
        keyboard = InlineKeyboardMarkup([[button]])
        update.message.reply_text('Silakan bergabung dengan saluran terlebih dahulu untuk bergabung dengan grup.', reply_markup=keyboard)

# Fungsi utama untuk menjalankan bot Telegram
def main():
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Handler perintah /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Handler pesan media yang diterima
    media_handler = MessageHandler(Filters.media, handle_media)
    dispatcher.add_handler(media_handler)
    
    updater.start_polling()
    updater.idle()

# Menjalankan bot Telegram
if __name__ == '__main__':
    main()
