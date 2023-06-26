import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
import threading
import batch

bot_token = "5892295406:AAFJZZzTgB9b1Zt68JGFRNdruNIlimta3Hg"
api_hash = "3f724ad34a81a6def449ffc8e3f1344a"
api_id = 22915641
bot = Client("kontolkudabot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = "AQAhIHQABabYk5E_6qM-5YTnssjy65CyfWjgPYVP4pwfpwg_muhZAaOlCe9MrD16Hh3YTrW8_EBOeb27eZWODMB8ZOobwyOLVFKmtlHpyxoV7_60s29GLXg8xV_LL_E4vjuDyrBOzBd_WJsc0oagPogTYTKzVlGBxac76NpawLZv7N46q0ch7I5gojFAHJx5JQ-7iGjVZyMPRpMPlkEFIS8kIzXhDCcx1A8mQ4rvoL6KvL99a1AQB_5hCW6RShsOVmY0wQwIeHhRoAMzrZc1xb-M2GCrRQKmnQJTYb8atEWfLBze8h8N4DkmQbSzMPl7tJPPkFKD27OdK1gW45slefyOi26PsgAAAABlSe1PAA"
if ss is not None:
    acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None

# download status
def downstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# upload status
def upstatus(statusfile,message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile,"r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt',"w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

        
# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot, I can send you restricted content by its post link__",
                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]]), reply_to_message_id=message.id)


@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        # ...
        pass
    
    # getting message
    elif "https://t.me/" in message.text:
        # ...
        pass


# handle private
def handle_private(message, chatid, msgid):
    # ...
    pass


# Fungsi untuk memproses pesan dalam mode batch
def process_batch(batch_messages):
    for message in batch_messages:
        # Lakukan pemrosesan pesan di sini
        handle_private(message, chatid, msgid)  # Ganti dengan pemrosesan yang sesuai


@bot.on_message(filters.command(["batch"]))
def process_batch_command(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    command_parts = message.text.split()  # Memisahkan teks perintah menjadi bagian-bagian
    batch_messages = []  # Daftar pesan yang akan diproses dalam mode batch

    # Periksa apakah perintah memiliki argumen yang sesuai
    if len(command_parts) > 1:
        # Misalnya, jika argumen kedua adalah daftar ID pesan yang akan diproses
        for message_id in command_parts[1:]:
            try:
                message_id = int(message_id)
                message = bot.get_messages(message.chat.id, message_id)
                batch_messages.append(message)
            except Exception as e:
                # Tangani kesalahan jika ada
                print(f"Error: {e}")
    else:
        # Tanggapan jika tidak ada argumen yang diberikan
        bot.send_message(message.chat.id, "Please provide a list of message IDs to process.")

    # Jalankan pemrosesan dalam mode batch
    batch.batch_execute(process_batch, batch_messages)


# Infinity polling
bot.run()
