import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_URL = "https://api.ocr.space/parse/image"

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    response = requests.post(
        API_URL,
        files={"filename": photo_bytes},
        data={"language": "jpn", "isOverlayRequired": False},
    )

    try:
        result = response.json()
        parsed_text = result["ParsedResults"][0]["ParsedText"]
        if parsed_text.strip():
            await update.message.reply_text(f"Распознанный текст:\n{parsed_text}")
        else:
            await update.message.reply_text("Не удалось распознать текст.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка распознавания: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
