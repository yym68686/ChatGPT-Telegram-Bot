import os
import sys
import time
import asyncio
import logging, datetime, pytz
from chat import getResult, resetChat
from telegram import BotCommand, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, filters
from config import MODE, NICK

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

botNick = NICK.lower() if NICK is not None else None
botNicKLength = len(botNick) if botNick is not None else 0

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . ! 
# must be escaped with the preceding character '\'.
def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} ! I am Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",
        # reply_markup=ForceReply(selective=True),
    )

def help(update, context):
    message = (
        "我是人见人爱的 ChatGPT\~\n\n"
        "欢迎访问 https://github\.com/yym68686/ChatGPT\-Telegram\-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')

def reset(update, context):
    resetChat()
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Conversation has been reset!"
    )

def process_message(update, context):
    print(update.effective_user.username, update.effective_user.id, update.message.text)
    if NICK is None:
        chat_content = update.message.text
    else:
        if update.message.text[:botNicKLength].lower() != botNick: return
        chat_content = update.message.text[botNicKLength:].strip()

    chat_id = update.effective_chat.id
    response_msg = ''
    try:
        response_msg = getResult(chat_content)
    except Exception as e:
        print("response_msg", response_msg)
        print("Exception", e)
        print("Exception str", str(e))
        if "expired" in str(e):
            context.bot.send_message(
                chat_id=chat_id,
                text="token 已过期 :(",
                parse_mode=ParseMode.MARKDOWN,
            )
        elif "available" in str(e):
            context.bot.send_message(
                chat_id=chat_id,
                text="抱歉，openai 官网 g 啦，您等会儿再问问…… :(",
                parse_mode=ParseMode.MARKDOWN,
            )
        elif "many" in str(e):
            context.bot.send_message(
                chat_id=chat_id,
                text="抱歉，我现在忙不过来啦，您等会儿再问问…… :(",
                parse_mode=ParseMode.MARKDOWN,
            )
            resetChat()
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Conversation has been reset!"
            )
        elif "Incorrect response from OpenAI API" in str(e):
            pass
        elif "Not a JSON response" in str(e):
            pass
        elif "Wrong response code" in str(e):
            pass
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="抱歉，遇到未知错误 :( \n\n" + str(e),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=response_msg,

            # text=telegram.utils.helpers.escape_markdown(response_msg, 2),
            # parse_mode="MarkdownV2",
            # text=escaped(response_msg),
            # parse_mode="Markdown",
        )

# 小功能
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    if ("can't" in str(context.error)):
        message = (
            f"出错啦！请重试。\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

def unknown(update: Update, context: CallbackContext): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def setup(token):
    if MODE == "dev": # 本地调试，需要挂代理，这里使用的是 surge
        updater = Updater(token, use_context=True, request_kwargs={
            'proxy_url': 'http://127.0.0.1:6152' # 需要代理才能使用 telegram
        })
    elif MODE == "prod": # 生产服务器在美国，不需要代理
        updater = Updater(token, use_context=True)
    else:
        logger.error("需要设置 MODE!")
        sys.exit(1)

    # set commands
    updater.bot.set_my_commands([
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the conversation'),
        BotCommand('help', 'Help'),
    ])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text, process_message))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    return updater, dispatcher

    # if MODE == "dev": # 本地调试
    #     updater.start_polling()
    # elif MODE == "prod": # HeroKu 远程生产环境
    #     updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    #     updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))

    # schedule.every().day.at(toUTC(checktime)).do(dailysign)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # updater.idle()
