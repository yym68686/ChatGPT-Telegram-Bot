import logging
from AI import AIBot
from config import MODE
from telegram import BotCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
ai_bot = AIBot()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . ! 
# must be escaped with the preceding character '\'.
def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    message = (
        "我是人见人爱的 ChatGPT\~\n\n"
        "欢迎访问 https://github\.com/yym68686/ChatGPT\-Telegram\-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    update.message.reply_html(
        rf"Hi {user.mention_html()} ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    context.bot.send_message(chat_id=update.effective_chat.id, text="出错啦！请重试。\n\n", parse_mode='MarkdownV2')

def unknown(update, context): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def setup(token):
    updater = Updater(token, use_context=True, request_kwargs={
        'proxy_url': 'http://127.0.0.1:6152' if MODE == "dev" else None
    })

    updater.bot.set_my_commands([
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
    ])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", ai_bot.reset_chat))
    dispatcher.add_handler(MessageHandler(Filters.text, ai_bot.getResult))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    return updater, dispatcher