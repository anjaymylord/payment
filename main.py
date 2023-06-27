import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading

bot_token = "5892295406:AAFJZZzTgB9b1Zt68JGFRNdruNIlimta3Hg" 
api_hash = "3f724ad34a81a6def449ffc8e3f1344a"
api_id = 22915641
bot = Client("kontolkudabot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = "AQAhIHQABabYk5E_6qM-5YTnssjy65CyfWjgPYVP4pwfpwg_muhZAaOlCe9MrD16Hh3YTrW8_EBOeb27eZWODMB8ZOobwyOLVFKmtlHpyxoV7_60s29GLXg8xV_LL_E4vjuDyrBOzBd_WJsc0oagPogTYTKzVlGBxac76NpawLZv7N46q0ch7I5gojFAHJx5JQ-7iGjVZyMPRpMPlkEFIS8kIzXhDCcx1A8mQ4rvoL6KvL99a1AQB_5hCW6RShsOVmY0wQwIeHhRoAMzrZc1xb-M2GCrRQKmnQJTYb8atEWfLBze8h8N4DkmQbSzMPl7tJPPkFKD27OdK1gW45slefyOi26PsgAAAABlSe1PAA" 
if ss is not None:
    acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None

# download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)


# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bot.send_message(
        message.chat.id,
        f"👋 Hai **{message.from_user.mention}**, Saya adalah Save Restricted Bot, Saya dapat mengirimkan konten terbatas berdasarkan tautan kiriman",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]]
        ),
        reply_to_message_id=message.id,
    )


# handle private
def handle_private(message, chatid, msgid):
    msg = acc.get_messages(chatid, msgid)

    if "text" in str(msg):
        bot.send_message(
            message.chat.id,
            msg.text,
            entities=msg.entities,
            reply_to_message_id=message.id,
        )
        return

    smsg = bot.send_message(message.chat.id, "__Downloading__", reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    if "Document" in str(msg):
        try:
            thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_document(
            message.chat.id,
            file,
            thumb=thumb,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            reply_to_message_id=message.id,
            progress=progress,
            progress_args=[message, "up"],
        )
        if thumb is not None:
            os.remove(thumb)

    elif "Video" in str(msg):
        try:
            thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_video(
            message.chat.id,
            file,
            duration=msg.video.duration,
            width=msg.video.width,
            height=msg.video.height,
            thumb=thumb,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            reply_to_message_id=message.id,
            progress=progress,
            progress_args=[message, "up"],
        )
        if thumb is not None:
            os.remove(thumb)

    elif "Animation" in str(msg):
        bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)

    elif "Sticker" in str(msg):
        bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

    elif "Voice" in str(msg):
        bot.send_voice(
            message.chat.id,
            file,
            caption=msg.caption,
            thumb=thumb,
            caption_entities=msg.caption_entities,
            reply_to_message_id=message.id,
            progress=progress,
            progress_args=[message, "up"],
        )

    elif "Audio" in str(msg):
        try:
            thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_audio(
            message.chat.id,
            file,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            reply_to_message_id=message.id,
            progress=progress,
            progress_args=[message, "up"],
        )
        if thumb is not None:
            os.remove(thumb)

    elif "Photo" in str(msg):
        bot.send_photo(
            message.chat.id,
            file,
            caption=msg.caption,
            caption_entities=msg.caption_entities,
            reply_to_message_id=message.id,
            progress=progress,
            progress_args=[message, "up"],
        )

    os.remove(f'{message.id}upstatus.txt')
    bot.delete_messages(message.chat.id, smsg.message_id)


# run batch
async def run_batch(client, conv, user_id, link, _range):
    for i in range(1, _range+1):
        await asyncio.sleep(1)
        msg = await bot.send_message(conv.chat_id, f"Processing link {i}/{_range}...")
        # Process the link here
        # ...
        await asyncio.sleep(1)
        await bot.edit_message_text(conv.chat_id, msg.message_id, f"Processed link {i}/{_range}")
    await bot.send_message(conv.chat_id, "Batch process completed!")


bot.run()
