import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_URL = "https://api.ocr.space/parse/image"
BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"

logging.basicConfig(level=logging.INFO)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    response = requests.post(
        API_URL,
        files={"filename": ("image.jpg", photo_bytes)},
        data={"language": "jpn", "isOverlayRequired": False},
    )

    try:
        result = response.json()
        if result.get("IsErroredOnProcessing"):
            await update.message.reply_text("Ошибка OCR-сервиса: не удалось обработать изображение.")
            return

        parsed_results = result.get("ParsedResults")
        if parsed_results and isinstance(parsed_results, list):
            parsed_text = parsed_results[0].get("ParsedText", "")
            if parsed_text.strip():
                await update.message.reply_text(f"Распознанный текст:\n{parsed_text}")
            else:
                await update.message.reply_text("Не удалось распознать текст.")
        else:
            await update.message.reply_text("Не получен результат от OCR-сервиса.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
