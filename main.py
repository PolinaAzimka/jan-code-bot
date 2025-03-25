import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from googlesearch import search

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7587391633:AAHyIMZ5VKOTQBfUjyENBgQ99xX7mQf94bY"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text(f"Ищу JAN-код для: {query}")

    try:
        results = []
        urls = search(query + " JANコード", num=5, pause=2.0, advanced=True)
        for url in urls:
            results.append(url)

        if results:
            reply = "\n".join(results)
        else:
            reply = "JAN-код не найден."

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
