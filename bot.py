import telegram
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Token bot Telegram Anda
TOKEN = '6171063049:AAEtT8LfoUS6xqV2rCQlA_M_7DAse0e_zG0'

# Token API pembayaran QRIS
QRIS_TOKEN = 'ID2022147421889A01'

# Fungsi untuk menangani perintah /start
def start(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Generate QR code pembayaran
    qr_code = generate_qr_code(chat_id)
    
    # Kirim QR code sebagai foto
    context.bot.send_photo(chat_id=chat_id, photo=qr_code)
    
    # Kirim pesan dengan instruksi pembayaran
    context.bot.send_message(chat_id=chat_id, text='Silakan lakukan pembayaran melalui QR code di atas.')
    context.bot.send_message(chat_id=chat_id, text='Setelah pembayaran berhasil, Anda akan menerima tautan channel khusus.')
    

# Fungsi untuk menghasilkan QR code pembayaran menggunakan API QRIS
def generate_qr_code(chat_id):
    # URL API QRIS
    api_url = 'https://api.qris.com/generate_qr_code'
    
    # Data pembayaran yang akan dikirim ke API QRIS
    payment_data = {
        'chat_id': chat_id,
        'amount': 100,  # Jumlah pembayaran dalam rupiah
        'description': 'Pembayaran Bergabung ke Channel Khusus'  # Deskripsi pembayaran
    }
    
    # Kirim permintaan POST ke API QRIS
    response = requests.post(api_url, json=payment_data, headers={'Authorization': f'Bearer {QRIS_TOKEN}'})
    
    # Ambil QR code dari respons API
    qr_code_url = response.json().get('qr_code')
    
    # Unduh QR code sebagai file
    qr_code = requests.get(qr_code_url).content
    
    return qr_code
    

# Fungsi untuk menangani perintah /verify_payment
def verify_payment(update, context):
    chat_id = update.effective_chat.id
    
    # Lakukan verifikasi pembayaran
    
    # Jika pembayaran berhasil, berikan tautan channel khusus
    channel_link = 'https://t.me/nama_channel_khusus'
    context.bot.send_message(chat_id=chat_id, text=f'Pembayaran berhasil. Berikut adalah tautan channel khusus: {channel_link}')
    

def main():
    # Inisialisasi bot
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Tambahkan handler perintah /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    # Tambahkan handler perintah /verify_payment
    verify_payment_handler = CommandHandler('verify_payment', verify_payment)
    dispatcher.add_handler(verify_payment_handler)
    
    # Jalankan bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
