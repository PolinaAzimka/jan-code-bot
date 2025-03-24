import logging
import requests
import re
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"
GOOGLE_SEARCH_URL = "https://www.google.com/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TARGET_DOMAINS = [
    "shopping.yahoo.co.jp", "www.yahoo.co.jp", "auctions.yahoo.co.jp",
    "www.matsukiyococokara-online.com", "www.beautygarage.jp", "bh-s.net",
    "www.be-wavestyle.jp", "www.bisella.com", "www.biccamera.com", "beplants.jp",
    "t-esthe.jp", "www.yodobashi.com", "www.j-b-m.co.jp", "www.netsea.jp",
    "www.karadahouse.jp", "jp.mercari.com", "netdeoroshi.com",
    "www.superdelivery.com", "dokodemo.world", "www.tajimaya-oroshi.net",
    "amazon.co.jp", "rakuten.co.jp"
]

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    try:
        # OCR.space API
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": photo_bytes},
            data={"language": "jpn", "apikey": "helloworld"}
        )
        result = response.json()
        text = result["ParsedResults"][0]["ParsedText"]
        await update.message.reply_text(f"Распознанный текст:\n{text}")
        await search_jan_code(text, update)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при распознавании: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    await update.message.reply_text(f"Ищу JAN-код по тексту: {text}")
    await search_jan_code(text, update)

async def search_jan_code(query, update: Update):
    try:
        params = {"q": f"{query} site:" + " OR site:".join(TARGET_DOMAINS)}
        res = requests.get(GOOGLE_SEARCH_URL, params=params, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        links = [a["href"] for a in soup.select("a[href]") if "url?q=" in a["href"]]
        jan_code = None
        for link in links:
            real_url = link.split("url?q=")[1].split("&")[0]
            page = requests.get(real_url, headers=HEADERS, timeout=10)
            jan_match = re.search(r"JAN(?:コード)?:?\s*([0-9]{8,13})", page.text)
            if jan_match:
                jan_code = jan_match.group(1)
                await update.message.reply_text(f"Найден JAN-код: {jan_code}\nИсточник: {real_url}")
                break
        if not jan_code:
            await update.message.reply_text("JAN-код не найден.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при поиске: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_polling()
