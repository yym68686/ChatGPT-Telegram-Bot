import os
import logging
from md2tgmd import escape
from runasync import run_async
from telegram import BotCommand
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters
from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY
from telegram.constants import ChatAction
from AI import getChatGPT, reset_chat, ChatGPTbot, ChatGPT4bot, Claude2bot, api, api4

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

async def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    message = (
        "我是人见人爱的 ChatGPT~\n\n"
        "欢迎访问 https://github.com/yym68686/ChatGPT-Telegram-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    await update.message.reply_html(rf"Hi {user.mention_html()} ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",)
    await update.message.reply_text(escape(message), parse_mode='MarkdownV2')

botNick = NICK.lower() if NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)
translator_prompt = "You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {}, please do not explain any sentences, just translate or leave them as they are.: "
async def command_bot(update, context, language="simplified chinese", prompt=translator_prompt, title="", robot=ChatGPTbot, has_command=True):
    if has_command == False or len(context.args) > 0:
        message = update.message.text if NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
        if has_command:
            message = ' '.join(context.args)
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        if prompt:
            prompt = prompt.format(language)
            message = prompt + message
        if (api or api4) and message:
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            await getChatGPT(title, robot, message, update, context)
    else:
        message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="请在命令后面放入文本。",
            parse_mode='MarkdownV2',
            reply_to_message_id=update.message.message_id,
        )

async def info(update, context):
    message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**BOT_TOKEN:** `{BOT_TOKEN}`\n\n"
        f"**API_URL:** `{os.environ.get('API_URL', None)}`\n\n"
        f"**API:** `{API}`\n\n"
        f"**API4:** `{API4}`\n\n"
        f"**WEB_HOOK:** `{WEB_HOOK}`\n\n"
        f"**NICK:** `{NICK}`\n"
        f"**PASS_HISTORY:** `{PASS_HISTORY}`"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2')

async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    await context.bot.send_message(chat_id=update.message.chat_id, text="出错啦！请重试。", parse_mode='MarkdownV2')

async def unknown(update, context): # 当用户输入未知命令时，返回文本
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def setup(token):
    application = ApplicationBuilder().read_timeout(10).connection_pool_size(50000).pool_timeout(1200.0).token(token).build()
    
    run_async(application.bot.set_my_commands([
        BotCommand('gpt4', 'use gpt4'),
        BotCommand('claude2', 'use claude2'),
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        BotCommand('info', 'basic information'),
    ]))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", command_bot))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english")))
    application.add_handler(CommandHandler("gpt4", lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ gpt-4`\n\n", robot=ChatGPT4bot)))
    application.add_handler(CommandHandler("claude2", lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ claude2`\n\n", robot=Claude2bot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ gpt-3.5`\n\n", robot=ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    return application