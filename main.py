import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import telebot
import os
import threading

bot_token = os.environ.get("TOKEN", None) 
api_hash = os.environ.get("HASH", None) 
api_id = os.environ.get("ID", None)
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = os.environ.get("STRING", None)
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

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


# progress writter
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
	bot.send_message(message.chat.id, f"__👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot, I can send you restricted content by it's post link__",
	reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]]), reply_to_message_id=message.id)


@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# joining chats
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
				return
			bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.id)
		except UserAlreadyParticipant:
			bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.id)
		except InviteHashExpired:
			bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.id)
	
	# getting message
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		msgid = int(datas[-1].split("?")[0])

		# private
		if "https://t.me/c/" in message.text:
			chatid = int("-100" + datas[-2])
			if acc is None:
				bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
				return
			try: handle_private(message,chatid,msgid)
			except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)
		
		# public
		else:
			username = datas[-2]
			msg  = bot.get_messages(username,msgid)
			try: bot.copy_message(message.chat.id, msg.chat.id, msg.id)
			except:
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.id)

# private
@bot.message_handler(commands=['com'])
def handle_download_all_files(message):
    # Memecah pesan menjadi argumen msgid dan jumlah_file
    command_args = message.text.split(' ')
    if len(command_args) != 3:
        bot.reply_to(message, "Perintah tidak valid. Gunakan format: /com (msgid) (jumlah file)")
        return

    try:
        msgid = int(command_args[1])
        jumlah_file = int(command_args[2])
    except ValueError:
        bot.reply_to(message, "ID pesan dan jumlah file harus berupa angka.")
        return

    # Panggil fungsi handle_private dengan argumen yang sesuai
    handle_private(message, chatid, msgid, jumlah_file)

def handle_private(message, chatid, msgid, jumlah_file):
    msg = acc.get_messages(chatid, msgid)

    if "text" in str(msg):
        bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = bot.send_message(message.chat.id, '__Mengunduh Media__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()

    file_types = ["Document", "Video", "Animation", "Sticker", "Voice", "Audio", "Photo"]
    files = []

    for file_type in file_types:
        files.extend(acc.get_messages(chatid, filter=types.InputMessagesFilterDocument, limit=jumlah_file))

    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    for file in files:
        if "Document" in str(file):
            try:
                thumb = acc.download_media(file.document.thumbs[0].file_id)
            except:
                thumb = None

            bot.send_document(message.chat.id, file, thumb=thumb, caption=file.caption, caption_entities=file.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if thumb is not None:
                os.remove(thumb)

        elif "Video" in str(file):
            try:
                thumb = acc.download_media(file.video.thumbs[0].file_id)
            except:
                thumb = None

            bot.send_video(message.chat.id, file, duration=file.video.duration, width=file.video.width, height=file.video.height, thumb=thumb, caption=file.caption, caption_entities=file.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if thumb is not None:
                os.remove(thumb)

        elif "Animation" in str(file):
            bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)

        elif "Sticker" in str(file):
            bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

        elif "Voice" in str(file):
            bot.send_voice(message.chat.id, file, caption=file.caption, thumb=thumb, caption_entities=file.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

        elif "Audio" in str(file):
            try:
                thumb = acc.download_media(file.audio.thumbs[0].file_id)
            except:
                thumb = None

            bot.send_audio(message.chat.id, file, caption=file.caption, caption_entities=file.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
            if thumb is not None:
                os.remove(thumb)

        elif "Photo" in str(file):
            bot.send_photo(message.chat.id, file, caption=file.caption, caption_entities=file.caption_entities, reply_to_message_id=message.id)

        os.remove(file)
    
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')

    bot.delete_messages(message.chat.id, [smsg.id])

# infinty polling
bot.run()