import os
import sys
import time
import logging, datetime, pytz
from revChatGPT.V1 import Chatbot
from telegram import BotCommand, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, filters
from config import MODE, NICK, config

chatbot = Chatbot(config)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

botNick = NICK.lower() if NICK is not None else None
botNicKLength = len(botNick) if botNick is not None else 0
print("nick:", botNick)

# In all other places characters
# _ * [ ] ( ) ~ ` > # + - = | { } . ! 
# must be escaped with the preceding character '\'.
def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()} ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",
    )

def help(update, context):
    message = (
        "我是人见人爱的 ChatGPT\~\n\n"
        "欢迎访问 https://github\.com/yym68686/ChatGPT\-Telegram\-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    update.message.reply_text(message, parse_mode='MarkdownV2')

def reset(update, context):
    chatbot.reset_chat()

def process_message(update, context):
    print(update.effective_user.username, update.effective_user.id, update.message.text)
    if NICK is None:
        chat_content = update.message.text
    else:
        if update.message.text[:botNicKLength].lower() != botNick: return
        chat_content = update.message.text[botNicKLength:].strip()

    chat_id = update.effective_chat.id
    response = ''
    LastMessage_id = ''
    try:
        for data in chatbot.ask(chat_content):
            try:
                response = data["message"]
            #     if LastMessage_id == '':
            #         message = context.bot.send_message(
            #             chat_id=chat_id,
            #             text=response,
            #         )
            #         LastMessage_id = message.message_id
            #         print("LastMessage_id", LastMessage_id)
            #         continue
            #     context.bot.edit_message_text(chat_id=chat_id, message_id=LastMessage_id, text=response)
            except:
                # print("response", data)
                if "reloading the conversation" in data:
                    chatbot.reset_chat()
                    message = context.bot.send_message(
                        chat_id=chat_id,
                        text="对话已超过上限，已重置聊天，请重试！",
                    )
                    return
                if "conversation_id" in data:
                    continue
                message = context.bot.send_message(
                    chat_id=chat_id,
                    text="未知错误：" + str(data),
                )
                return
        context.bot.send_message(
            chat_id=chat_id,
            text=response,
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id,
        )
        print("getresult", response)
    except Exception as e:
        print("response_msg", response)
        print("Exception", e)
        print("Exception str", str(e))
        context.bot.send_message(
            chat_id=chat_id,
            text="出错啦 :(",
            parse_mode=ParseMode.MARKDOWN,
        )

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
        BotCommand('reset', 'reset the chat'),
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