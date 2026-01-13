from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re
import os

# Bot token will be taken from Railway environment variable
BOT_TOKEN = os.getenv("8599332997:AAFxPZjtXcPJ1UZzJWh8YWyvairZXX_ePrs")

def extract_shopsy_link(flipkart_url: str):
    # Extract slug and itm ID from Flipkart URL
    match = re.search(r"flipkart\.com/(.+?)/p/(itm[a-zA-Z0-9]+)", flipkart_url)
    if not match:
        return None

    slug = match.group(1)
    itm = match.group(2)

    # Extract PID
    pid_match = re.search(r"pid=([A-Z0-9]+)", flipkart_url, re.I)
    if not pid_match:
        return None

    pid = pid_match.group(1)

    return f"https://www.shopsy.in/{slug}/p/{itm}?pid={pid}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Ignore messages that are not Flipkart links
    if "flipkart.com" not in text:
        return

    shopsy_link = extract_shopsy_link(text)

    if not shopsy_link:
        await update.message.reply_text("Invalid Flipkart product link")
        return

    # Reply with ONLY the Shopsy link
    await update.message.reply_text(shopsy_link)

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
