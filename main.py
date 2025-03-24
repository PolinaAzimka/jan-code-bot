import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pytesseract
from PIL import Image
import requests

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Путь к языковым данным tesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

# Обработка изображения и распознавание текста
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "/tmp/photo.jpg"
    await photo_file.download_to_drive(photo_path)

    try:
        text = pytesseract.image_to_string(Image.open(photo_path), lang='jpn')
        await update.message.reply_text(f"Распознанный текст: {text}")
{text}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания текста: {e}")

async def main():
    bot_token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
