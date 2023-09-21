import re
import os
import config
import logging
from md2tgmd import escape
from runasync import run_async
from chatgpt2api.V3 import Chatbot as GPT
from telegram.constants import ChatAction
from agent import docQA, get_doc_from_local, search_summary
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters, CallbackQueryHandler


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# 获取 httpx 的 logger
httpx_logger = logging.getLogger("httpx")
# 设置 httpx 的日志级别为 WARNING
httpx_logger.setLevel(logging.WARNING)

botNick = config.NICK.lower() if config.NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)
translator_prompt = "You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {}, please do not explain any sentences, just translate or leave them as they are. this is the content you need to translate: "
async def command_bot(update, context, language=None, prompt=translator_prompt, title="", robot=None, has_command=True):
    if update.message.reply_to_message is None:
        if has_command == False or len(context.args) > 0:
            message = update.message.text if config.NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
            if has_command:
                message = ' '.join(context.args)
            print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
            if prompt:
                prompt = prompt.format(language)
                message = prompt + message
            if config.API and message:
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
    else:
        if update.message.reply_to_message.document is None:
            message = (
                f"格式错误哦~，需要回复一个文件，我才知道你要针对哪个文件提问，注意命令与问题之间的空格\n\n"
                f"请输入 `要问的问题`\n\n"
                f"例如已经上传某文档 ，问题是 蘑菇怎么分类？\n\n"
                f"先左滑文档进入回复模式，在聊天框里面输入 `蘑菇怎么分类？`\n\n"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
            return
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        pdf_file = update.message.reply_to_message.document
        # print(pdf_file)
        file_id = pdf_file.file_id
        new_file = await context.bot.get_file(file_id)
        # print(new_file)
        file_url = new_file.file_path

        question = update.message.text

        file_name = pdf_file.file_name
        docpath = os.getcwd() + "/" + file_name
        result = await pdfQA(file_url, docpath, question)
        print(result)
        await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def reset_chat(update, context):
    if config.API:
        config.ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
    # if config.API4:
    #     config.ChatGPT4bot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
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
        for data in robot.ask_stream(text, convo_id=str(update.message.chat_id), pass_history=config.PASS_HISTORY):
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
        if config.API:
            robot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
            messageid = ''
            config.API = ''
        result += f"`出错啦！{e}`"
    print(result)
    if lastresult != result and messageid:
        if 'claude2' in title:
            result = re.sub(r",", '，', result)
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2')

import time
import threading
async def delete_message(update, context, messageid, delay=10):
    time.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageid)
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')

buttons = [
    [
        InlineKeyboardButton("gpt-3.5-turbo", callback_data="gpt-3.5-turbo"),
        InlineKeyboardButton("gpt-3.5-turbo-16k", callback_data="gpt-3.5-turbo-16k"),
    ],
    [
        InlineKeyboardButton("gpt-3.5-turbo-0301", callback_data="gpt-3.5-turbo-0301"),
    ],
    [
        InlineKeyboardButton("gpt-3.5-turbo-0613", callback_data="gpt-3.5-turbo-0613"),
    ],
    [
        InlineKeyboardButton("gpt-4", callback_data="gpt-4"),
        InlineKeyboardButton("gpt-4-0314", callback_data="gpt-4-0314"),
    ],
    [
        InlineKeyboardButton("gpt-4-32k", callback_data="gpt-4-32k"),
        InlineKeyboardButton("gpt-4-32k-0314", callback_data="gpt-4-32k-0314"),
    ],
    [
        InlineKeyboardButton("gpt-4-0613", callback_data="gpt-4-0613"),
        InlineKeyboardButton("gpt-4-32k-0613", callback_data="gpt-4-32k-0613"),
    ],
    [
        InlineKeyboardButton("claude-2-web", callback_data="claude-2-web"),
    ],
    [
        InlineKeyboardButton("返回上一级", callback_data="返回上一级"),
    ],
]

first_buttons = [
    [
        InlineKeyboardButton("更换模型", callback_data="更换模型"),
    ],
    [
        InlineKeyboardButton("历史记录已关闭", callback_data="历史记录"),
        InlineKeyboardButton("google已打开", callback_data="google"),
    ],
    [
        InlineKeyboardButton("搜索已打开", callback_data="搜索"),
        InlineKeyboardButton("联网解析PDF已打开", callback_data="pdf"),
    ],
]
if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
    first_buttons[1][1] = InlineKeyboardButton("google已关闭", callback_data="google")


banner = "👇下面可以随时更改默认 gpt 模型："
async def button_press(update, context):
    """Function to handle the button press"""
    info_message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**Default engine:** `{config.GPT_ENGINE}`\n"
        f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
        f"**temperature:** `{config.temperature}`\n"
        f"**API_URL:** `{config.API_URL}`\n\n"
        f"**API:** `{config.API}`\n\n"
        f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
    )
    callback_query = update.callback_query
    await callback_query.answer()
    data = callback_query.data
    if ("gpt" or "cluade") in data:
        config.GPT_ENGINE = data
        if config.API:
            config.ChatGPTbot = GPT(api_key=f"{config.API}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
            config.ChatGPTbot.reset(convo_id=str(update.effective_chat.id), system_prompt=config.systemprompt)
            try:
                info_message = (
                    f"`Hi, {update.effective_user.username}!`\n\n"
                    f"**Default engine:** `{config.GPT_ENGINE}`\n"
                    f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
    
                    f"**temperature:** `{config.temperature}`\n"
                    f"**PASS_HISTORY:** `{config.PASS_HISTORY}`\n"
                    f"**USE_GOOGLE:** `{config.USE_GOOGLE}`\n\n"
                    f"**API_URL:** `{config.API_URL}`\n\n"
                    f"**API:** `{config.API}`\n\n"
                    f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
                )
                message = await callback_query.edit_message_text(
                    text=escape(info_message + banner),
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode='MarkdownV2'
                )
                # messageid = message.message_id
                # thread = threading.Thread(target=run_async, args=(delete_message(update, context, messageid, delay=10),))
                # thread.start()
            except Exception as e:
                logger.info(e)
                pass
    elif "更换模型" in data:
        message = await callback_query.edit_message_text(
            text=escape(info_message + banner),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode='MarkdownV2'
        )
    elif "返回" in data:
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "历史记录" in data:
        config.PASS_HISTORY = not config.PASS_HISTORY
        if config.PASS_HISTORY == False:
            first_buttons[1][0] = InlineKeyboardButton("历史记录已关闭", callback_data="历史记录")
        else:
            first_buttons[1][0] = InlineKeyboardButton("历史记录已打开", callback_data="历史记录")
        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{config.API}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "搜索" in data:
        config.SEARCH_USE_GPT = not config.SEARCH_USE_GPT
        if config.SEARCH_USE_GPT == False:
            first_buttons[2][0] = InlineKeyboardButton("搜索已关闭", callback_data="搜索")
        else:
            first_buttons[2][0] = InlineKeyboardButton("搜索已打开", callback_data="搜索")

        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{config.API}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )

        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "google" in data:
        if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
            return
        config.USE_GOOGLE = not config.USE_GOOGLE
        if config.USE_GOOGLE == False:
            first_buttons[1][1] = InlineKeyboardButton("google已关闭", callback_data="google")
        else:
            first_buttons[1][1] = InlineKeyboardButton("google已打开", callback_data="google")

        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{config.API}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "pdf" in data:
        config.PDF_EMBEDDING = not config.PDF_EMBEDDING
        if config.PDF_EMBEDDING == False:
            first_buttons[2][1] = InlineKeyboardButton("联网解析PDF已关闭", callback_data="pdf")
        else:
            first_buttons[2][1] = InlineKeyboardButton("联网解析PDF已打开", callback_data="pdf")

        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{config.API}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )


async def info(update, context):
    info_message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**Default engine:** `{config.GPT_ENGINE}`\n"
        f"**Default search model:** `{config.DEFAULT_SEARCH_MODEL}`\n"
        f"**temperature:** `{config.temperature}`\n"
        f"**API_URL:** `{config.API_URL}`\n\n"
        f"**API:** `{config.API}`\n\n"
        f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
    )
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(info_message), reply_markup=InlineKeyboardMarkup(first_buttons), parse_mode='MarkdownV2')

    messageid = message.message_id
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)


async def search(update, context, has_command=True):
    if has_command == False or len(context.args) > 0:
        message = update.message.text if config.NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
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
            for data in search_summary(text, model=config.DEFAULT_SEARCH_MODEL, use_goolge=config.USE_GOOGLE, use_gpt=config.SEARCH_USE_GPT):
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

from agent import pdfQA, getmd5, persist_emdedding_pdf
async def handle_pdf(update, context):
    # 获取接收到的文件
    pdf_file = update.message.document
    # 得到文件的url
    file_name = pdf_file.file_name
    docpath = os.getcwd() + "/" + file_name
    persist_db_path = getmd5(docpath)
    match_embedding = os.path.exists(persist_db_path)
    file_id = pdf_file.file_id
    new_file = await context.bot.get_file(file_id)
    file_url = new_file.file_path

    question = update.message.caption
    if question is None:
        if not match_embedding:
            persist_emdedding_pdf(file_url, persist_db_path)
        message = (
            f"已成功解析文档！\n\n"
            f"请输入 `要问的问题`\n\n"
            f"例如已经上传某文档 ，问题是 蘑菇怎么分类？\n\n"
            f"先左滑文档进入回复模式，并在聊天框里面输入 `蘑菇怎么分类？`\n\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        return

    result = await pdfQA(file_url, docpath, question)
    print(result)
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

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
        BotCommand('info', 'basic information'),
        BotCommand('qa', 'Document Q&A with Embedding Database Search'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
        # BotCommand('gpt_use_search', 'open or close gpt use search'),
        # BotCommand('history', 'open or close chat history'),
        # BotCommand('google', 'open or close google search'),
    ]))

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, "simplified chinese", robot=config.ChatGPTbot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=config.ChatGPTbot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("qa", qa))
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handle_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    return application