import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_URL = "https://api.ocr.space/parse/image"
OCR_SPACE_API_KEY = "K83263040588957"  # Ключ пользователя

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено! Распознаю текст...")

    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()

    response = requests.post(
        API_URL,
        files={"file": photo_bytes},
        data={
            "apikey": OCR_SPACE_API_KEY,
            "language": "jpn",
            "isOverlayRequired": False
        },
    )

    try:
        result = response.json()
        parsed_results = result.get("ParsedResults")
        if parsed_results:
            parsed_text = parsed_results[0].get("ParsedText", "").strip()
            if parsed_text:
                await update.message.reply_text(f"Распознанный текст:
{parsed_text}")
            else:
                await update.message.reply_text("Не удалось распознать текст.")
        else:
            await update.message.reply_text("Ошибка при распознавании: нет результата.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при распознавании: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
