import logging
from revChatGPT.V3 import Chatbot
from telegram import BotCommand, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import MODE, NICK, API, COOKIES
from EdgeGPT import Chatbot as BingAI, ConversationStyle


Bingbot = BingAI(cookies=COOKIES)
ChatGPTbot = Chatbot(api_key=f"{API}")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

botNick = NICK.lower() if NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)

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

def reset(update, context):
    ChatGPTbot.reset_chat()

def bing(update, context):
    chat_content = context.args[0] if NICK is None else context.args[0][botNicKLength:].strip() if context.args[0][:botNicKLength].lower() == botNick else None
    # creative balanced precise
    message = Bingbot.ask(prompt=chat_content, conversation_style=ConversationStyle.balanced)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=message,
        parse_mode=ParseMode.MARKDOWN,
    )

def process_message(update, context):
    print(update.effective_user.username, update.effective_user.id, update.message.text)
    chat_content = update.message.text if NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
    chat_id = update.effective_chat.id
    response = ''
    try:
        for data in ChatGPTbot.ask(chat_content):
            response += data
        context.bot.send_message(
            chat_id=chat_id,
            text=response,
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

def unknown(update, context): # 当用户输入未知命令时，返回文本
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def setup(token):
    updater = Updater(token, use_context=True, request_kwargs={
        'proxy_url': 'http://127.0.0.1:6152' if MODE == "dev" else None
    })

    # set commands
    updater.bot.set_my_commands([
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the chat'),
    ])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(MessageHandler(Filters.text, process_message))
    dispatcher.add_handler(MessageHandler("bing", bing))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    return updater, dispatcher