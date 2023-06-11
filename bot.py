from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from io import BytesIO
from PIL import Image
from pyzbar import pyzbar

TOKEN = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'

def start(update: Update, context):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Silakan kirimkan foto QRIS untuk pembayaran.')

def process_qris_photo(update: Update, context):
    chat_id = update.message.chat_id

    # Memeriksa apakah pesan yang diterima memiliki foto
    if update.message.photo:
        photo = update.message.photo[-1]  # Mengambil foto terakhir yang dikirim
        file = context.bot.get_file(photo.file_id)
        image_bytes = BytesIO()
        file.download(out=image_bytes)  # Mengunduh foto QRIS

        qris_data = read_qris(image_bytes)  # Membaca data QRIS dari foto

        if qris_data:
            # Lakukan verifikasi pembayaran berdasarkan data QRIS yang didapat
            # ...

            # Jika pembayaran valid, kirimkan tautan channel kepada pengguna
            send_channel_link(chat_id)
        else:
            bot.send_message(chat_id=chat_id, text='Foto QRIS tidak valid.')
    else:
        bot.send_message(chat_id=chat_id, text='Mohon kirimkan foto QRIS.')

def read_qris(image_bytes):
    # Membaca data QRIS dari foto menggunakan library pyzbar
    image = Image.open(image_bytes)
    qris_codes = pyzbar.decode(image)

    if qris_codes:
        qris_data = qris_codes[0].data.decode('utf-8')
        return qris_data
    else:
        return None

def send_channel_link(chat_id):
    channel_link = 'https://t.me/+0g8h6exjM942ZGVl'  # Ganti dengan tautan channel Anda
    message = f'Anda telah berhasil membayar. Silakan klik tautan ini untuk bergabung dengan channel kami: {channel_link}'
    bot.send_message(chat_id=chat_id, text=message)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    qris_photo_handler = MessageHandler(Filters.photo, process_qris_photo)
    dispatcher.add_handler(qris_photo_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    main()
