import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import pytesseract
from PIL import Image
import requests
from io import BytesIO

TOKEN = 'YOUR_TOKEN'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Отправь мне фото с текстом, и я попробую его распознать.')

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Фото получено! Распознаю текст...')
    
    photo_file = await update.message.photo[-1].get_file()
    photo = requests.get(photo_file.file_path)
    img = Image.open(BytesIO(photo.content))
    
    custom_oem_psm_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang='eng+jpn', config=custom_oem_psm_config)
    
    await update.message.reply_text(f"Распознанный текст: {extracted_text}")
{text}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()
