import re
import os
import logging
from md2tgmd import escape
from datetime import datetime
from runasync import run_async
from telegram import BotCommand
from agent import duckduckgo_search, docQA, get_doc_from_sitemap, get_doc_from_local, search_summary
from chatgpt2api.V3 import Chatbot as GPT
from telegram.constants import ChatAction
from config import BOT_TOKEN, WEB_HOOK, NICK, API, API4, PASS_HISTORY, temperature, USE_GOOGLE, DEFAULT_SEARCH_MODEL, DEFAULT_SEARCH_MODEL, SEARCH_USE_GPT, GPT_ENGINE, API_URL
import config
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# 获取 httpx 的 logger
httpx_logger = logging.getLogger("httpx")
# 设置 httpx 的日志级别为 WARNING
httpx_logger.setLevel(logging.WARNING)

current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = f"You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: [ {Current_Date} ]"

if API:
    ChatGPTbot = GPT(api_key=f"{API}", system_prompt=systemprompt, temperature=temperature)
    Claude2bot = GPT(api_key=f"{API}", engine="claude-2-web")
if API4:
    ChatGPT4bot = GPT(api_key=f"{API4}", engine="gpt-4-0613", system_prompt=systemprompt, temperature=temperature)

botNick = NICK.lower() if NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)
translator_prompt = "You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {}, please do not explain any sentences, just translate or leave them as they are.: "
async def command_bot(update, context, language=None, prompt=translator_prompt, title="", robot=None, has_command=True):
    if has_command == False or len(context.args) > 0:
        message = update.message.text if NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
        if has_command:
            message = ' '.join(context.args)
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        if prompt:
            prompt = prompt.format(language)
            message = prompt + message
        global API
        global API4
        if (API or API4) and message:
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            if config.SEARCH_USE_GPT and "gpt-4" not in title and language == None:
                await search(update, context, has_command=False)
            else:
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
        f"**Default engine:** `{GPT_ENGINE}`\n"
        f"**Default search model:** `{DEFAULT_SEARCH_MODEL}`\n"
        f"**gpt use search:** `{config.SEARCH_USE_GPT}`\n"
        f"**temperature:** `{temperature}`\n"
        f"**PASS_HISTORY:** `{PASS_HISTORY}`\n"
        f"**USE_GOOGLE:** `{config.USE_GOOGLE}`\n\n"
        f"**API_URL:** `{API_URL}`\n\n"
        f"**API:** `{API}`\n\n"
        f"**API4:** `{API4}`\n\n"
        f"**WEB_HOOK:** `{WEB_HOOK}`"
        # f"**BOT_TOKEN:** `{BOT_TOKEN}`\n\n"
        # f"**NICK:** `{NICK}`\n"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2')

async def reset_chat(update, context):
    if API:
        ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
    if API4:
        ChatGPT4bot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
    )

async def getChatGPT(title, robot, message, update, context):
    result = title
    text = message
    modifytime = 0
    lastresult = ''
    message = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="思考中💭",
        parse_mode='MarkdownV2',
        reply_to_message_id=update.message.message_id,
    )
    messageid = message.message_id
    try:
        for data in robot.ask_stream(text, convo_id=str(update.message.chat_id), pass_history=PASS_HISTORY):
            result = result + data
            tmpresult = result
            modifytime = modifytime + 1
            if re.sub(r"```", '', result).count("`") % 2 != 0:
                tmpresult = result + "`"
            if result.count("```") % 2 != 0:
                tmpresult = result + "\n```"
            if modifytime % 20 == 0 and lastresult != tmpresult:
                if 'claude2' in title:
                    tmpresult = re.sub(r",", '，', tmpresult)
                await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2')
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        print('\033[0m')
        global API
        if API:
            robot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
            messageid = ''
            API = ''
        result += f"`出错啦！{e}`"
    print(result)
    if lastresult != result and messageid:
        if 'claude2' in title:
            result = re.sub(r",", '，', result)
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2')

async def history(update, context):
    config.PASS_HISTORY = not config.PASS_HISTORY
    status = "打开" if config.PASS_HISTORY else "关闭"
    message = (
        f"当前已{status}聊天记录！\n"
        f"**PASS_HISTORY:** `{config.PASS_HISTORY}`"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2')

async def gpt_use_search(update, context):
    config.SEARCH_USE_GPT = not config.SEARCH_USE_GPT
    status = "打开" if config.SEARCH_USE_GPT else "关闭"
    message = (
        f"当前已{status}gpt默认搜索🔍！\n"
        f"**SEARCH_USE_GPT:** `{config.SEARCH_USE_GPT}`"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2')

async def google(update, context):
    if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
        await context.bot.send_message(chat_id=update.message.chat_id, text=escape("GOOGLE_API_KEY or GOOGLE_CSE_ID not found"), parse_mode='MarkdownV2')
        return
    config.USE_GOOGLE = not config.USE_GOOGLE
    status = "打开" if config.USE_GOOGLE else "关闭"
    message = (
        f"当前已{status}google搜索！\n"
        f"**USE_GOOGLE:** `{config.USE_GOOGLE}`"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2')

async def search(update, context, has_command=True):
    if has_command == False or len(context.args) > 0:
        message = update.message.text if NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
        if has_command:
            message = ' '.join(context.args)
            print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        if message:
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
            text = message
            result = ''
            modifytime = 0
            lastresult = ''
            message = await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="思考中💭",
                parse_mode='MarkdownV2',
                reply_to_message_id=update.message.message_id,
            )
            messageid = message.message_id
            for data in search_summary(text, model=DEFAULT_SEARCH_MODEL, use_goolge=config.USE_GOOGLE, use_gpt=config.SEARCH_USE_GPT):
                result = result + data
                tmpresult = result
                modifytime = modifytime + 1
                if re.sub(r"```", '', result).count("`") % 2 != 0:
                    tmpresult = result + "`"
                if result.count("```") % 2 != 0:
                    tmpresult = result + "\n```"
                if modifytime % 20 == 0 and lastresult != tmpresult:
                    await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2')
                    lastresult = tmpresult
            print(result)
            if lastresult != result and messageid:
                await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2')
    else:
        message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="请在命令后面放入文本。",
            parse_mode='MarkdownV2',
            reply_to_message_id=update.message.message_id,
        )

async def qa(update, context):
    if (len(context.args) != 2):
        message = (
            f"格式错误哦~，需要两个参数，注意路径或者链接、问题之间的空格\n\n"
            f"请输入 `/qa 知识库链接 要问的问题`\n\n"
            f"例如知识库链接为 https://abc.com ，问题是 蘑菇怎么分类？\n\n"
            f"则输入 `/qa https://abc.com 蘑菇怎么分类？`\n\n"
            f"问题务必不能有空格，👆点击上方命令复制格式\n\n"
            f"除了输入网址，同时支持本地知识库，本地知识库文件夹路径为 `./wiki`，问题是 蘑菇怎么分类？\n\n"
            f"则输入 `/qa ./wiki 蘑菇怎么分类？`\n\n"
            f"问题务必不能有空格，👆点击上方命令复制格式\n\n"
            f"本地知识库目前只支持 Markdown 文件\n\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        return
    print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    # result = docQA(context.args[0], context.args[1], get_doc_from_sitemap)
    result = await docQA(context.args[0], context.args[1], get_doc_from_local)
    source_url = set([i.metadata['source'] for i in result["source_documents"]])
    source_url = "\n".join(source_url)
    message = (
        f"{result['result']}\n\n"
        f"参考链接：\n"
        f"{source_url}"
    )
    print(message)
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

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
        BotCommand('gpt4', 'use gpt4'),
        BotCommand('claude2', 'use claude2'),
        BotCommand('search', 'search the web with google and duckduckgo'),
        BotCommand('qa', 'Document Q&A with Embedding Database Search'),
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        BotCommand('info', 'basic information'),
        BotCommand('history', 'open or close chat history'),
        BotCommand('google', 'open or close google search'),
        BotCommand('gpt_use_search', 'open or close gpt use search'),
    ]))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, "simplified chinese", robot=ChatGPTbot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=ChatGPTbot)))
    application.add_handler(CommandHandler("gpt4", lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ gpt-4`\n\n", robot=ChatGPT4bot)))
    application.add_handler(CommandHandler("claude2", lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ claude2`\n\n", robot=Claude2bot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("google", google))
    application.add_handler(CommandHandler("gpt_use_search", gpt_use_search))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("qa", qa))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title="`🤖️ gpt-3.5`\n\n", robot=ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    return application