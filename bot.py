import os
import io
import telebot
from PIL import Image, ImageFilter
from rembg import remove

TOKEN = os.environ["8599026487:AAF6TtOCpBJnuly-QLnU2sZz3RsdxCP-Bl0"]   # Render Environment Variable

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["photo"])
def blur(message):
    try:
        bot.reply_to(message, "⏳ Processing...")

        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        img_bytes = bot.download_file(file_info.file_path)

        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        subject = remove(img)

        bg = img.convert("RGB").filter(ImageFilter.GaussianBlur(25)).convert("RGBA")
        bg.paste(subject, (0, 0), subject)

        output = io.BytesIO()
        bg.convert("RGB").save(output, format="JPEG")
        output.seek(0)

        bot.send_photo(message.chat.id, output)

    except Exception as e:
        bot.reply_to(message, f"❌ Error:\n{e}")

print("✅ Bot Started...")
bot.infinity_polling(skip_pending=True)
