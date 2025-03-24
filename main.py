import os
import logging
import pytesseract
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = f"photo_{update.message.message_id}.jpg"
    await file.download_to_drive(file_path)
    await update.message.reply_text("Фото получено! Распознаю текст...")

    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang='eng+jpn')

        if text.strip():
            await update.message.reply_text(f"Распознанный текст:\n{text.strip()}")
        else:
            await update.message.reply_text("Текст не распознан. Буду искать по изображению...")

    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания текста: {e}")

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    await application.bot.delete_webhook(drop_pending_updates=True)
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
