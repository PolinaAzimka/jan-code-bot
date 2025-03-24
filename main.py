import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import pytesseract
from PIL import Image
import requests
from io import BytesIO

BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        await update.message.reply_text('Фото получено! Распознаю текст...')
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        photo_bytes = BytesIO(requests.get(file.file_path).content)

        try:
            img = Image.open(photo_bytes)
            text = pytesseract.image_to_string(img, lang='eng+jpn')
            await update.message.reply_text(f'Распознанный текст:\n{text}')
        except Exception as e:
            await update.message.reply_text(f'Ошибка распознавания текста: {str(e)}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, start_bot))
    app.run_polling()
