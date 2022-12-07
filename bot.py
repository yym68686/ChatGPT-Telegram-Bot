import os
import sys
import time
import asyncio
import logging, datetime, pytz
from chat import getresult, resetChat
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, filters
from config import admin, MODE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . ! 
# must be escaped with the preceding character '\'.
def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} 欢迎使用 🎉",
        # reply_markup=ForceReply(selective=True),
    )
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
    chat_text = update.message.text
    if chat_text.startswith("javis"):
        chat_id = update.message.chat_id
        chat_text = chat_text.split("javis")[1].strip()
        print(chat_text)
        response_msg = ''
        try:
            response_msg = getresult(chat_text)
        except Exception:
            print(response_msg["detail"]["message"])
            if "expired" in response_msg["detail"]["message"]:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="token 已过期 :(",
                    parse_mode=ParseMode.MARKDOWN,
                )
            elif "available" in response_msg: 
                context.bot.send_message(
                    chat_id=chat_id,
                    text="抱歉，openai 官网g啦，您等会儿再问问…… :(",
                    parse_mode=ParseMode.MARKDOWN,
                )
            elif "many" in response_msg["detail"]["message"]:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="抱歉，我现在忙不过来啦，您等会儿再问问…… :(",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                context.bot.send_message(
                    chat_id=chat_id,
                    text="抱歉，遇到未知错误 :(" + response_msg["detail"]["message"],
                    parse_mode=ParseMode.MARKDOWN,
                )
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text=response_msg,
                # parse_mode=ParseMode.MARKDOWN,
            )

# 小功能
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    if ("can't" in str(context.error)):
        message = (
            f"出错啦！请重试。\n\n"
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

def echo(update, context):
    updater.bot.send_message(chat_id = admin, text= str(update.effective_chat.id) + " " + update.message.text)
    # update.message.reply_text(update.message.text)

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

    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.text, process_message))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
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
