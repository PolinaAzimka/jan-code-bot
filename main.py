import logging
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

# Логи
logging.basicConfig(level=logging.INFO)

# Путь к tesseract
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

# Получение токена из переменных среды
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "/tmp/photo.jpg"
    await photo_file.download_to_drive(photo_path)

    try:
        img = Image.open(photo_path)
        text = pytesseract.image_to_string(img, lang='jpn')
        await update.message.reply_text(f"Распознанный текст:\n{text}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания текста: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправьте фото для распознавания текста.")

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.run_polling()
