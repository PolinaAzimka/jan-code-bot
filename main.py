import logging
import os
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка переменной окружения
os.environ["TESSDATA_PREFIX"] = "/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_path = "/tmp/image.png"
        await photo_file.download_to_drive(photo_path)
        text = pytesseract.image_to_string(Image.open(photo_path), lang="jpn")
        await update.message.reply_text(f"Распознанный текст:\n{text}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания текста: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.run_polling()
