import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === ВСТАВЬ СЮДА СВОИ ТОКЕНЫ ===
TELEGRAM_TOKEN = '8470406400:AAEYFC27iCLVpg6CZNWeFrYesPu2U8i9k8s'
HF_TOKEN = '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'

# Hugging Face модель
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

logging.basicConfig(level=logging.INFO)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я ИИ-бот по теме электронной подписи.\n"
        "Задай мне вопрос:\n"
        "— Что такое КЭП?\n"
        "— Как получить электронную подпись?\n"
        "— В чём разница между ЭП и УЭП?"
    )


# Обращение к нейросети Hugging Face
def ask_ai(prompt: str) -> str:
    payload = {"inputs": f"Вопрос: {prompt} Ответ:"}
    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "Не удалось сгенерировать ответ.")
        return result.get("error", "Ошибка в ответе модели.")
    except Exception as e:
        return f"Ошибка: {str(e)}"


# Ответ на текст
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Думаю...")
    reply = ask_ai(question)
    await update.message.reply_text(reply)

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен.")
    app.run_polling()

