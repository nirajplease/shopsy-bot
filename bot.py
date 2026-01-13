from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re

BOT_TOKEN = "8599332997:AAFxPZjtXcPJ1UZzJWh8YWyvairZXX_ePrs"

def extract_shopsy_link(flipkart_url):
    # Extract slug + itm
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

    # Ignore non-Flipkart messages
    if "flipkart.com" not in text:
        return

    shopsy_link = extract_shopsy_link(text)

    if not shopsy_link:
        await update.message.reply_text("Invalid Flipkart product link")
        return

    # ✅ Reply with ONLY the link
    await update.message.reply_text(shopsy_link)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
