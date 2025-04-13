import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from analysis import get_analysis
from prediction import predict_price
from plotter import plot_price_chart

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di Forex Bot!\n\n"
        "/prediksi EURUSD\n"
        "/analisa EURUSD\n"
        "/chart EURUSD"
    )

async def prediksi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = context.args[0].upper() if context.args else "EURUSD"
    msg = await predict_price(pair)
    await update.message.reply_text(msg)

async def analisa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = context.args[0].upper() if context.args else "EURUSD"
    msg = await get_analysis(pair)
    await update.message.reply_text(msg)

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = context.args[0].upper() if context.args else "EURUSD"
    file_path = await plot_price_chart(pair)
    await update.message.reply_photo(photo=open(file_path, 'rb'))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediksi", prediksi))
    app.add_handler(CommandHandler("analisa", analisa))
    app.add_handler(CommandHandler("chart", chart))
    app.run_polling()

if __name__ == "__main__":
    main(
