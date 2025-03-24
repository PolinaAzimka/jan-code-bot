import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Ищу JAN-код...")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    files = {'encoded_image': ('image.jpg', photo_bytes), 'image_content': ''}
    params = {'hl': 'ja'}
    search_url = "https://www.google.com/searchbyimage/upload"
    response = requests.post(search_url, files=files, params=params, allow_redirects=False)

    if 'Location' not in response.headers:
        await update.message.reply_text("Ошибка при поиске изображения.")
        return

    fetch_url = response.headers['Location']
    headers = {'User-Agent': 'Mozilla/5.0'}
    result = requests.get(fetch_url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')

    text = soup.get_text()
    jan_code = None
    import re
    match = re.search(r'4\d{12}', text)
    if match:
        jan_code = match.group()

    if jan_code:
        await update.message.reply_text(f"Найден JAN-код: {jan_code}")
    else:
        await update.message.reply_text("JAN-код не найден.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
