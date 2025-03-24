import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image
import pytesseract
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")

    photo_file = await update.message.photo[-1].get_file()
    photo_path = "/tmp/photo.jpg"
    await photo_file.download_to_drive(photo_path)

    try:
        image = Image.open(photo_path)
        text = pytesseract.image_to_string(image, lang="jpn")
        await update.message.reply_text(f"Распознанный текст: {text}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания текста: {e}")

async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())
