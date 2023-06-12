from telegram.ext import Updater, CommandHandler

# Inisialisasi variabel global
links = {}  # Dictionary untuk menyimpan tautan channel

# Fungsi untuk menangani perintah /copylink
def copy_link(update, context):
    user_id = update.effective_user.id

    if user_id in links:
        # Jika pengguna sudah meminta tautan sebelumnya
        update.message.reply_text("Anda sudah meminta tautan sebelumnya.")
    else:
        if len(links) < 1:
            # Jika masih ada slot tersedia
            channel_link = "https://t.me/+zn9YABu82_M3M2I5"  # Ganti dengan tautan channel yang sebenarnya
            links[user_id] = channel_link
            update.message.reply_text(f"Ini tautan channel: {channel_link}")
        else:
            # Jika semua slot sudah terisi
            update.message.reply_text("Maaf, jumlah permintaan sudah mencapai batas.")

# Fungsi utama untuk menjalankan bot
def main():
    # Inisialisasi bot dengan token
    updater = Updater("6007897911:AAGgi7Ya7Gz7SNa8bjV31-4fMjguShjl3rU")  # Ganti dengan token bot Telegram yang sebenarnya

    # Mendaftarkan handler untuk perintah /copylink
    updater.dispatcher.add_handler(CommandHandler("copylink", copy_link))

    # Memulai bot
    updater.start_polling()
    updater.idle()

# Menjalankan bot
if __name__ == '__main__':
    main()
