import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import subprocess

bot_token = "5892295406:AAFJZZzTgB9b1Zt68JGFRNdruNIlimta3Hg" 
api_hash = "3f724ad34a81a6def449ffc8e3f1344a" 
api_id = 22915641 
bot = Client("kontolkudabot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = "AQAhIHQABabYk5E_6qM-5YTnssjy65CyfWjgPYVP4pwfpwg_muhZAaOlCe9MrD16Hh3YTrW8_EBOeb27eZWODMB8ZOobwyOLVFKmtlHpyxoV7_60s29GLXg8xV_LL_E4vjuDyrBOzBd_WJsc0oagPogTYTKzVlGBxac76NpawLZv7N46q0ch7I5gojFAHJx5JQ-7iGjVZyMPRpMPlkEFIS8kIzXhDCcx1A8mQ4rvoL6KvL99a1AQB_5hCW6RShsOVmY0wQwIeHhRoAMzrZc1xb-M2GCrRQKmnQJTYb8atEWfLBze8h8N4DkmQbSzMPl7tJPPkFKD27OdK1gW45slefyOi26PsgAAAABlSe1PAA" 
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
	

# handle private
def handle_private(message,chatid,msgid):
		msg  = acc.get_messages(chatid,msgid)

		if "text" in str(msg):
			bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
			return

		smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.id}downstatus.txt')

		upsta = threading.Thread(target=lambda:upstatus(f'{message.id}upstatus.txt',smsg),daemon=True)
		upsta.start()
		
		if "Document" in str(msg):
			try:
				thumb = acc.download_media(msg.document.thumbs[0].file_id)
			except: thumb = None
			
			bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
			if thumb != None: os.remove(thumb)

		elif "Video" in str(msg):
			try: 
				thumb = acc.download_media(msg.video.thumbs[0].file_id)
			except: thumb = None

			bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
			if thumb != None: os.remove(thumb)

		elif "Animation" in str(msg):
			bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
			   
		elif "Sticker" in str(msg):
			bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

		elif "Voice" in str(msg):
			bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])

		elif "Audio" in str(msg):
			try:
				thumb = acc.download_media(msg.audio.thumbs[0].file_id)
			except: thumb = None
				
			bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
			if thumb != None: os.remove(thumb)

		elif "Photo" in str(msg):
			bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

		os.remove(file)
		if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
		bot.delete_messages(message.chat.id,[smsg.id])
		
# batch untuk copy konten sekaligus
@bot.on_message(filters.command(["batch"]))
def run_batch(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    # Menyimpan pesan dan teks perintah batch
    msg = message.reply_to_message
    command = message.text.split(None, 1)[1]

    # Memeriksa jika perintah dijalankan pada pesan balasan
    if msg is None:
        bot.send_message(message.chat.id, "⚠️ Kamu harus membalas pesan dengan perintah batch!", reply_to_message_id=message.id)
        return

    # Menyimpan konten pesan
    content = msg.text or msg.caption

    # Membuat file batch
    with open("batch_script.bat", "w") as file:
        file.write(content)

    # Menjalankan file batch dengan menggunakan subprocess
    try:
        output = subprocess.check_output("batch_script.bat", shell=True, stderr=subprocess.STDOUT, timeout=60)
        result = output.decode("utf-8")
        bot.send_message(message.chat.id, f"✅ Perintah batch dijalankan:\n\n```\n{result}\n```", reply_to_message_id=message.id)
    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, f"❌ Terjadi kesalahan saat menjalankan perintah batch:\n\n```\n{e.output.decode('utf-8')}\n```", reply_to_message_id=message.id)
    except subprocess.TimeoutExpired:
        bot.send_message(message.chat.id, "⌛ Waktu eksekusi perintah batch telah habis.", reply_to_message_id=message.id)

    # Menghapus file batch setelah selesai
    os.remove("batch_script.bat")

# infinty polling
bot.run()