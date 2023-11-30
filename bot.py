import re
import os
import config
import logging
import traceback
import utils.decorators as decorators
from utils.md2tgmd import escape
from utils.chatgpt2api import Chatbot as GPT
from utils.chatgpt2api import claudebot
from telegram.constants import ChatAction
from utils.agent import docQA, get_doc_from_local, claudeQA
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters, CallbackQueryHandler, Application, AIORateLimiter
from config import WEB_HOOK, PORT, BOT_TOKEN


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# 获取 httpx 的 logger
httpx_logger = logging.getLogger("httpx")
# 设置 httpx 的日志级别为 WARNING
httpx_logger.setLevel(logging.WARNING)

httpx_logger = logging.getLogger("chromadb.telemetry.posthog")
httpx_logger.setLevel(logging.WARNING)

botNick = config.NICK.lower() if config.NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)
translator_prompt = "You are a translation engine, you can only translate text and cannot interpret it, and do not explain. Translate the text to {}, please do not explain any sentences, just translate or leave them as they are. this is the content you need to translate: "
@decorators.Authorization
async def command_bot(update, context, language=None, prompt=translator_prompt, title="", robot=None, has_command=True):
    if update.message.reply_to_message is None or update.message.reply_to_message.text or update.message.reply_to_message.document is None:
        if has_command == False or len(context.args) > 0:
            message = update.message.text if config.NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
            if has_command:
                message = ' '.join(context.args)
            print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
            if prompt and has_command:
                prompt = prompt.format(language)
                message = prompt + message
            if message:
                if "claude" in config.GPT_ENGINE and config.ClaudeAPI:
                    robot = config.claudeBot
                await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
                await getChatGPT(update, context, title, robot, message, config.SEARCH_USE_GPT, has_command)
        else:
            message = await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="请在命令后面放入文本。",
                parse_mode='MarkdownV2',
                reply_to_message_id=update.message.message_id,
            )
    else:
        # if update.message.reply_to_message.document is None:
        #     message = (
        #         f"格式错误哦~，需要回复一个文件，我才知道你要针对哪个文件提问，注意命令与问题之间的空格\n\n"
        #         f"请输入 `要问的问题`\n\n"
        #         f"例如已经上传某文档 ，问题是 蘑菇怎么分类？\n\n"
        #         f"先左滑文档进入回复模式，在聊天框里面输入 `蘑菇怎么分类？`\n\n"
        #     )
        #     await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        #     return
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        pdf_file = update.message.reply_to_message.document

        file_id = pdf_file.file_id
        new_file = await context.bot.get_file(file_id)

        file_url = new_file.file_path

        question = update.message.text

        file_name = pdf_file.file_name
        docpath = os.getcwd() + "/" + file_name
        if  "cluade" in config.GPT_ENGINE:
            result = await claudeQA(file_url, question)
        else:
            result = await pdfQA(file_url, docpath, question)
        print(result)
        await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.Authorization
async def reset_chat(update, context):
    if config.API:
        config.ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
    )

async def getChatGPT(update, context, title, robot, message, use_search=config.SEARCH_USE_GPT, has_command=True):
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
    get_answer = robot.ask_stream
    if not config.API or (config.USE_G4F and not config.SEARCH_USE_GPT):
        import utils.gpt4free as gpt4free
        get_answer = gpt4free.get_response

    try:
        for data in get_answer(text, convo_id=str(update.message.chat_id), pass_history=config.PASS_HISTORY):
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
                await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True)
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        traceback.print_exc()
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
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def search(update, context, title, robot):
    message = update.message.text if config.NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
    print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
    if (len(context.args) == 0):
        message = (
            f"格式错误哦~，示例：\n\n"
            f"`/search 今天的微博热搜有哪些？`\n\n"
            f"👆点击上方命令复制格式\n\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        return
    message = ' '.join(context.args)
    result = title
    text = message
    modifytime = 0
    lastresult = ''
    message = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="搜索中💭",
        parse_mode='MarkdownV2',
        reply_to_message_id=update.message.message_id,
    )
    messageid = message.message_id
    get_answer = robot.search_summary
    if not config.API or (config.USE_G4F and not config.SEARCH_USE_GPT):
        import utils.gpt4free as gpt4free
        get_answer = gpt4free.get_response

    try:
        for data in get_answer(text, convo_id=str(update.message.chat_id), pass_history=config.PASS_HISTORY):
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
                await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True)
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        traceback.print_exc()
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
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def image(update, context):
    print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
    if (len(context.args) == 0):
        message = (
            f"格式错误哦~，示例：\n\n"
            f"`/pic 一只可爱长毛金渐层在趴在路由器上`\n\n"
            f"👆点击上方命令复制格式\n\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        return
    message = ' '.join(context.args)
    result = ""
    robot = config.dallbot
    text = message
    message = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="生成中💭",
        parse_mode='MarkdownV2',
        reply_to_message_id=update.message.message_id,
    )
    messageid = message.message_id

    try:
        for data in robot.dall_e_3(text):
            result = data
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=result, reply_to_message_id=update.message.message_id)
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        traceback.print_exc()
        print('\033[0m')
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
            messageid = ''
            config.API = ''
        result += f"`出错啦！{e}`"
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text="当前prompt未能成功生成图片😣换句话试试吧～", parse_mode='MarkdownV2', disable_web_page_preview=True)
    print(result)

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
        InlineKeyboardButton("gpt-3.5-turbo-1106", callback_data="gpt-3.5-turbo-1106"),
    ],
    # [
    #     InlineKeyboardButton("gpt-3.5-turbo-0301", callback_data="gpt-3.5-turbo-0301"),
    # ],
    # [
    #     InlineKeyboardButton("gpt-3.5-turbo-0613", callback_data="gpt-3.5-turbo-0613"),
    # ],
    [
        InlineKeyboardButton("gpt-4-1106-preview", callback_data="gpt-4-1106-preview"),
        # InlineKeyboardButton("gpt-4-32k", callback_data="gpt-4-32k"),
        # InlineKeyboardButton("gpt-4-32k-0314", callback_data="gpt-4-32k-0314"),
    ],
    [
        InlineKeyboardButton("gpt-4", callback_data="gpt-4"),
        InlineKeyboardButton("gpt-4-32k", callback_data="gpt-4-32k"),
        # InlineKeyboardButton("gpt-4-0314", callback_data="gpt-4-0314"),
    ],
    # [
    #     InlineKeyboardButton("gpt-4-0613", callback_data="gpt-4-0613"),
    #     InlineKeyboardButton("gpt-4-32k-0613", callback_data="gpt-4-32k-0613"),
    # ],
    [
        InlineKeyboardButton("claude-2.1", callback_data="claude-2.1"),
        InlineKeyboardButton("claude-2-web", callback_data="claude-2-web"),
    ],
    [
        InlineKeyboardButton("返回上一级", callback_data="返回上一级"),
    ],
]

first_buttons = [
    [
        InlineKeyboardButton("更换问答模型", callback_data="更换问答模型"),
    ],
    [
        InlineKeyboardButton("历史记录已关闭", callback_data="历史记录"),
        InlineKeyboardButton("google已打开", callback_data="google"),
    ],
    [
        InlineKeyboardButton("搜索已打开", callback_data="搜索"),
        InlineKeyboardButton("联网解析PDF已打开", callback_data="pdf"),
    ],
    [
        InlineKeyboardButton("🇨🇳 中文", callback_data="language"),
    ],
    [
        InlineKeyboardButton("gpt4free已关闭", callback_data="gpt4free"),
    ],
]
if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
    first_buttons[1][1] = InlineKeyboardButton("google已关闭", callback_data="google")

def replace_with_asterisk(string, start=10, end=45):
    return string[:start] + '*' * (end - start) + string[end:]

banner = "👇下面可以随时更改默认 gpt 模型："
async def button_press(update, context):
    """Function to handle the button press"""
    info_message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**Default engine:** `{config.GPT_ENGINE}`\n"
        f"**temperature:** `{config.temperature}`\n"
        f"**API_URL:** `{config.API_URL}`\n\n"
        f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
        f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
    )
    callback_query = update.callback_query
    await callback_query.answer()
    data = callback_query.data
    if "gpt-" in data or "claude" in data:
        config.GPT_ENGINE = data
        if config.API and "gpt-" in data:
            config.ChatGPTbot = GPT(api_key=f"{config.API}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
            config.ChatGPTbot.reset(convo_id=str(update.effective_chat.id), system_prompt=config.systemprompt)
        if config.ClaudeAPI and "claude" in data:
            config.claudeBot = claudebot(api_key=f"{config.ClaudeAPI}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
        try:
            info_message = (
                f"`Hi, {update.effective_user.username}!`\n\n"
                f"**Default engine:** `{config.GPT_ENGINE}`\n"
                f"**temperature:** `{config.temperature}`\n"
                f"**API_URL:** `{config.API_URL}`\n\n"
                f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
                f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
            )
            message = await callback_query.edit_message_text(
                text=escape(info_message + banner),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode='MarkdownV2'
            )
        except Exception as e:
            logger.info(e)
            pass
    elif "更换问答模型" in data:
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
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
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
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
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
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
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
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "language" in data:
        if config.LANGUAGE == "Simplified Chinese":
            first_buttons[3][0] = InlineKeyboardButton("🇺🇸 English", callback_data="language")
            config.LANGUAGE = "English"
        else:
            first_buttons[3][0] = InlineKeyboardButton("🇨🇳 中文", callback_data="language")
            config.LANGUAGE = "Simplified Chinese"
        config.systemprompt = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally in {config.LANGUAGE}. Knowledge cutoff: 2021-09. Current date: [ {config.Current_Date} ]"
        if config.API:
            config.ChatGPTbot = GPT(api_key=f"{config.API}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
            config.ChatGPTbot.reset(convo_id=str(update.effective_chat.id), system_prompt=config.systemprompt)
        if config.ClaudeAPI:
            config.claudeBot = claudebot(api_key=f"{config.ClaudeAPI}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)

        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )
    elif "gpt4free" in data:
        config.USE_G4F = not config.USE_G4F
        if config.USE_G4F == False:
            first_buttons[4][0] = InlineKeyboardButton("gpt4free已关闭", callback_data="gpt4free")
        else:
            first_buttons[4][0] = InlineKeyboardButton("gpt4free已打开", callback_data="gpt4free")

        info_message = (
            f"`Hi, {update.effective_user.username}!`\n\n"
            f"**Default engine:** `{config.GPT_ENGINE}`\n"
            f"**temperature:** `{config.temperature}`\n"
            f"**API_URL:** `{config.API_URL}`\n\n"
            f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
            f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
        )
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(first_buttons),
            parse_mode='MarkdownV2'
        )

@decorators.Authorization
async def info(update, context):
    info_message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**Default engine:** `{config.GPT_ENGINE}`\n"
        f"**temperature:** `{config.temperature}`\n"
        f"**API_URL:** `{config.API_URL}`\n\n"
        f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
        f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
    )
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(info_message), reply_markup=InlineKeyboardMarkup(first_buttons), parse_mode='MarkdownV2', disable_web_page_preview=True)

    messageid = message.message_id
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

from utils.agent import pdfQA, getmd5, persist_emdedding_pdf, get_doc_from_url
from pdfminer.high_level import extract_text
@decorators.Authorization
async def handle_pdf(update, context):
    # 获取接收到的文件
    pdf_file = update.message.document
    # 得到文件的url
    # file_name = pdf_file.file_name
    # docpath = os.getcwd() + "/" + file_name
    file_id = pdf_file.file_id
    new_file = await context.bot.get_file(file_id)
    file_url = new_file.file_path
    filename = get_doc_from_url(file_url)
    docpath = os.getcwd() + "/" + filename
    if config.ClaudeAPI:
        text = extract_text(docpath)
        prompt = (
            "Here is the document, inside <document></document> XML tags:"
            "<document>"
            "{}"
            "</document>"
        )
        # print(prompt.format(text))
        config.claudeBot.add_to_conversation(prompt.format(text), "Human", str(update.effective_chat.id))
        message = (
            f"文档上传成功！\n\n"
        )
        os.remove(docpath)
        await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

    # persist_db_path = getmd5(docpath)
    # match_embedding = os.path.exists(persist_db_path)
    # file_id = pdf_file.file_id
    # new_file = await context.bot.get_file(file_id)
    # file_url = new_file.file_path

    # question = update.message.caption
    # if question is None:
    #     if not match_embedding:
            # persist_emdedding_pdf(file_url, persist_db_path)
    #     message = (
    #         f"已成功解析文档！\n\n"
    #         f"请输入 `要问的问题`\n\n"
    #         f"例如已经上传某文档 ，问题是 蘑菇怎么分类？\n\n"
    #         f"先左滑文档进入回复模式，并在聊天框里面输入 `蘑菇怎么分类？`\n\n"
    #     )
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
    #     return

    # result = await pdfQA(file_url, docpath, question)
    # print(result)
    # await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.Authorization
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
    print(result["answer"])
    # source_url = set([i.metadata['source'] for i in result["source_documents"]])
    # source_url = "\n".join(source_url)
    # message = (
    #     f"{result['result']}\n\n"
    #     f"参考链接：\n"
    #     f"{source_url}"
    # )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result["answer"]), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    message = (
        "我是人见人爱的 ChatGPT~\n\n"
        "欢迎访问 https://github.com/yym68686/ChatGPT-Telegram-Bot 查看源码\n\n"
        "有 bug 可以联系 @yym68686"
    )
    await update.message.reply_html(rf"Hi {user.mention_html()} ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.",)
    await update.message.reply_text(escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    await context.bot.send_message(chat_id=update.message.chat_id, text="出错啦！请重试。", parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.Authorization
async def unknown(update, context): # 当用户输入未知命令时，返回文本
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand('info', 'basic information'),
        BotCommand('pic', 'Generate image'),
        BotCommand('search', 'search Google or duckduckgo'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        BotCommand('qa', 'Document Q&A with Embedding Database Search'),
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
    ])

if __name__ == '__main__':
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .read_timeout(10)
        .connection_pool_size(50000)
        .pool_timeout(1200.0)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pic", image))
    application.add_handler(CommandHandler("search", lambda update, context: search(update, context, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot)))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, config.LANGUAGE, robot=config.ChatGPTbot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=config.ChatGPTbot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("qa", qa))
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handle_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    if WEB_HOOK:
        print("WEB_HOOK:", WEB_HOOK)
        application.run_webhook("127.0.0.1", PORT, webhook_url=WEB_HOOK)
    else:
        application.run_polling()