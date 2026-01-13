from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re
import os

BOT_TOKEN = os.getenv("8599332997:AAFxPZjtXcPJ1UZzJWh8YWyvairZXX_ePrs")

def extract_shopsy_link(text: str):
    # Find Flipkart product URL (desktop or mobile)
    url_match = re.search(
        r"https?://(www\.|m\.)?flipkart\.com/([^/\s]+(?:/[^/\s]+)*)/p/(itm[a-zA-Z0-9]+)[^\s]*",
        text
    )

    if not url_match:
        return None

    slug = url_match.group(2)
    itm = url_match.group(3)

    # Extract PID from full text
    pid_match = re.search(r"pid=([A-Z0-9]+)", text, re.I)
    if not pid_match:
        return None

    pid = pid_match.group(1)

    return f"https://www.shopsy.in/{slug}/p/{itm}?pid={pid}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    shopsy_link = extract_shopsy_link(text)

    if not shopsy_link:
        return  # Ignore non-product messages silently

    await update.message.reply_text(shopsy_link)

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
