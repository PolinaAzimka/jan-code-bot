import logging
import re
import requests
import pytesseract
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from googlesearch import search
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

HEADERS = {"User-Agent": "Mozilla/5.0"}
JAN_PATTERN = re.compile(r"\b(?:JANコード[:：]?\s*)?(\d{13})\b")

SITES = [
    "shopping.yahoo.co.jp", "amazon.co.jp", "rakuten.co.jp", "yodobashi.com",
    "auctions.yahoo.co.jp", "matsukiyococokara-online.com", "beautygarage.jp",
    "bh-s.net", "be-wavestyle.jp", "bisella.com", "biccamera.com", "beplants.jp",
    "t-esthe.jp", "j-b-m.co.jp", "netsea.jp", "karadahouse.jp", "jp.mercari.com",
    "netdeoroshi.com", "superdelivery.com", "dokodemo.world", "tajimaya-oroshi.net"
]

def extract_jan_from_text(text):
    match = JAN_PATTERN.search(text)
    if match:
        return match.group(1)
    return None

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Ищу JAN-код...")
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    image = Image.open(BytesIO(photo_bytes))
    text = pytesseract.image_to_string(image, lang="jpn")
    jan_code = extract_jan_from_text(text)
    if jan_code:
        await update.message.reply_text(f"Найден JAN-код: {jan_code}")
        return
    await search_jan_online(update, text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ищу JAN-код по описанию...")
    await search_jan_online(update, update.message.text)

async def search_jan_online(update: Update, query: str):
    query = query.strip()
    search_query = f"{query} " + " OR ".join([f"site:{site}" for site in SITES])
    try:
        for url in search(search_query, num_results=10):
            page = requests.get(url, headers=HEADERS, timeout=10)
            jan_code = extract_jan_from_text(page.text)
            if jan_code:
                await update.message.reply_text(f"Найден JAN-код: {jan_code}\n{url}")
                return
        await update.message.reply_text("Не удалось найти JAN-код.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при поиске: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_polling()
