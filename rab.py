import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from datetime import datetime


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def time(update, context):
    await update.message.reply_text(datetime.now().time())


async def date(update, context):
    await update.message.reply_text(datetime.now().date())


def main():
    application = Application.builder().token('6273204407:AAHc-578ru2Uie1JQnypi7YjdXL3fUU2-ew').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)

    async def start(update, context):
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я телеграмм-бот.",
        )

    async def time(update, context):
        await update.message.reply_text(rf'Сейчас {datetime.now().time()}')

    async def date(update, context):
        await update.message.reply_text(rf'Сегодня {datetime.now().date()}')

    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("date", date))
    application.run_polling()


if __name__ == '__main__':
    main()





