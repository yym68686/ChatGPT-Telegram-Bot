import logging
from md2tgmd import escape
from runasync import run_async
from telegram import BotCommand
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters
from AI import AIBot
ai_bot = AIBot()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . !
# must be escaped with the preceding character '\'.
async def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    message = (
        "我是人见人爱的 ChatGPT~\n\n"
        "欢迎访问 https://github.com/yym68686/ChatGPT-Telegram-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    await update.message.reply_html(rf"Hi {user.mention_html()} ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",)
    await update.message.reply_text(escape(message), parse_mode='MarkdownV2')

async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    await context.bot.send_message(chat_id=update.message.chat_id, text="出错啦！请重试。", parse_mode='MarkdownV2')

async def unknown(update, context): # 当用户输入未知命令时，返回文本
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def setup(token):
    application = ApplicationBuilder().read_timeout(10).connection_pool_size(50000).pool_timeout(1200.0).token(token).build()
    
    run_async(application.bot.set_my_commands([
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
        BotCommand('en2zh', 'translate English to Chinese'),
        BotCommand("creative_bing", "get a creative new Bing"),
        BotCommand("balanced_bing", "get a balanced new Bing"),
        BotCommand("precise_bing", "get a precise new Bing"),
    ]))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", ai_bot.reset_chat))
    application.add_handler(CommandHandler("en2zh", ai_bot.en2zhtranslator))
    application.add_handler(CommandHandler("creative_bing", ai_bot.creative_bing))
    application.add_handler(CommandHandler("balanced_bing", ai_bot.balanced_bing))
    application.add_handler(CommandHandler("precise_bing", ai_bot.precise_bing))
    application.add_handler(MessageHandler(filters.TEXT, ai_bot.getResult))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    return application