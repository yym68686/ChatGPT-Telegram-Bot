import re
import os
import sys
sys.dont_write_bytecode = True
import config
import logging
import traceback
import utils.decorators as decorators
from md2tgmd import escape
from utils.chatgpt2api import Chatbot as GPT
from utils.chatgpt2api import claudebot
from utils.prompt import translator_en2zh_prompt, translator_prompt
from telegram.constants import ChatAction
from utils.plugins import Document_extract, get_encode_image
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters, CallbackQueryHandler, Application, AIORateLimiter, InlineQueryHandler
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

def CutNICK(update_text, update_chat):
    if config.NICK is None:
        return update_text
    else:
        if update_text[:botNicKLength].lower() == botNick:
            return update_text[botNicKLength:].strip()
        else:
            if update_chat.type == 'private':
                return update_text
            else:
                return None

async def GetMesage(update_message, context):
    image_url = None
    reply_to_message_text = None
    chatid = update_message.chat_id
    messageid = update_message.message_id
    if update_message.text:
        message = CutNICK(update_message.text, update_message.chat)
        rawtext = update_message.text

    if update_message.reply_to_message:
        reply_to_message_text = update_message.reply_to_message.text

    if update_message.photo:
        photo = update_message.photo[-1]
        file_id = photo.file_id
        photo_file = await context.bot.getFile(file_id)
        image_url = photo_file.file_path

        message = rawtext = CutNICK(update_message.caption, update_message.chat)
    return message, rawtext, image_url, chatid, messageid, reply_to_message_text

@decorators.GroupAuthorization
@decorators.Authorization
async def command_bot(update, context, language=None, prompt=translator_prompt, title="", robot=None, has_command=True):
    image_url = None
    if update.edited_message:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text = await GetMesage(update.edited_message, context)
    else:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text = await GetMesage(update.message, context)

    print("\033[32m", update.effective_user.username, update.effective_user.id, rawtext, "\033[0m")

    if has_command == False or len(context.args) > 0:
        if reply_to_message_text:
            message = reply_to_message_text + "\n" + message
        if has_command:
            message = ' '.join(context.args)
        if prompt and has_command:
            if translator_prompt == prompt:
                if language == "english":
                    prompt = prompt.format(language)
                else:
                    prompt = translator_en2zh_prompt
            message = prompt + message
        if message:
            if "claude" in config.GPT_ENGINE and config.ClaudeAPI:
                robot = config.claudeBot
            if image_url:
                robot = config.GPT4visionbot
                title = "`🤖️ gpt-4-vision-preview`\n\n"
            message = [{"type": "text", "text": message}]
            if (image_url and config.GPT_ENGINE == "gpt-4-vision-preview") or (image_url and robot == config.GPT4visionbot):
                base64_image = get_encode_image(image_url)
                message.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                )
            await context.bot.send_chat_action(chat_id=chatid, action=ChatAction.TYPING)
            await getChatGPT(update, context, title, robot, message, chatid, messageid)
    else:
        message = await context.bot.send_message(
            chat_id=chatid,
            text="请在命令后面放入文本。",
            parse_mode='MarkdownV2',
            reply_to_message_id=messageid,
        )

@decorators.GroupAuthorization
@decorators.Authorization
async def reset_chat(update, context):
    if config.API:
        config.ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
    if config.ClaudeAPI:
        config.claudeBot.reset(convo_id=str(update.message.chat_id), system_prompt=config.systemprompt)
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
    )

async def getChatGPT(update, context, title, robot, message, chatid, messageid):
    result = ""
    text = message
    modifytime = 0
    time_out = 600
    lastresult = title

    message = await context.bot.send_message(
        chat_id=chatid,
        text="思考中💭",
        parse_mode='MarkdownV2',
        reply_to_message_id=messageid,
    )
    messageid = message.message_id
    get_answer = robot.ask_stream
    pass_history = config.PASS_HISTORY
    if "gpt-4-vision-preview" in title:
        pass_history = False

    try:
        for data in get_answer(text, convo_id=str(chatid), pass_history=pass_history):
            if "🌐" not in data:
                result = result + data
            tmpresult = title + result
            modifytime = modifytime + 1
            if re.sub(r"```", '', result).count("`") % 2 != 0:
                tmpresult = title + result + "`"
            if result.count("```") % 2 != 0:
                tmpresult = title + result + "\n```"
            if 'claude2' in title:
                tmpresult = re.sub(r",", '，', tmpresult)
            if "🌐" in data:
                tmpresult = data
            if "answer:" in result:
                tmpresult = re.sub(r"thought:[\S\s]+?answer:\s", '', tmpresult)
                tmpresult = re.sub(r"action:[\S\s]+?answer:\s", '', tmpresult)
                tmpresult = re.sub(r"answer:\s", '', tmpresult)
                tmpresult = re.sub(r"thought:[\S\s]+", '', tmpresult)
                tmpresult = re.sub(r"action:[\S\s]+", '', tmpresult)
            else:
                tmpresult = re.sub(r"thought:[\S\s]+", '', tmpresult)
            if (modifytime % 20 == 0 and lastresult != tmpresult) or "🌐" in data:
                await context.bot.edit_message_text(chat_id=chatid, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        traceback.print_exc()
        print('\033[0m')
        if config.API:
            robot.reset(convo_id=str(chatid), system_prompt=config.systemprompt)
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=chatid, message_id=messageid)
            messageid = ''
            config.API = ''
        tmpresult = f"`{e}`"
    print(tmpresult)
    if lastresult != tmpresult and messageid:
        if 'claude2' in title:
            tmpresult = re.sub(r",", '，', tmpresult)
        await context.bot.edit_message_text(chat_id=chatid, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)

@decorators.GroupAuthorization
@decorators.Authorization
async def image(update, context):
    if update.edited_message:
        message = update.edited_message.text if config.NICK is None else update.edited_message.text[botNicKLength:].strip() if update.edited_message.text[:botNicKLength].lower() == botNick else None
        rawtext = update.edited_message.text
        chatid = update.edited_message.chat_id
        messageid = update.edited_message.message_id
    else:
        message = update.message.text if config.NICK is None else update.message.text[botNicKLength:].strip() if update.message.text[:botNicKLength].lower() == botNick else None
        rawtext = update.message.text
        chatid = update.message.chat_id
        messageid = update.message.message_id
    print("\033[32m", update.effective_user.username, update.effective_user.id, rawtext, "\033[0m")

    if (len(context.args) == 0):
        message = (
            f"格式错误哦~，示例：\n\n"
            f"`/pic 一只可爱长毛金渐层趴在路由器上`\n\n"
            f"👆点击上方命令复制格式\n\n"
        )
        await context.bot.send_message(chat_id=chatid, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
        return
    message = ' '.join(context.args)
    result = ""
    robot = config.dallbot
    text = message
    message = await context.bot.send_message(
        chat_id=chatid,
        text="生成中💭",
        parse_mode='MarkdownV2',
        reply_to_message_id=messageid,
    )
    start_messageid = message.message_id

    try:
        for data in robot.dall_e_3(text):
            result = data
            await context.bot.delete_message(chat_id=chatid, message_id=start_messageid)
            await context.bot.send_photo(chat_id=chatid, photo=result, reply_to_message_id=messageid)
    except Exception as e:
        print('\033[31m')
        print(e)
        print('\033[0m')
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            result += "OpenAI api 已过期！"
            config.API = ''
        elif "content_policy_violation" in str(e) or "violates OpenAI's policies" in str(e):
            result += "当前 prompt 未能成功生成图片，可能因为版权，政治，色情，暴力，种族歧视等违反 OpenAI 的内容政策😣，换句话试试吧～"
        elif "server is busy" in str(e):
            result += "服务器繁忙，请稍后再试～"
        elif "billing_hard_limit_reached" in str(e):
            result += "当前账号余额不足～"
        else:
            result += f"`{e}`"
        await context.bot.edit_message_text(chat_id=chatid, message_id=start_messageid, text=escape(result), parse_mode='MarkdownV2', disable_web_page_preview=True)

import time
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
        InlineKeyboardButton("gpt-4", callback_data="gpt-4"),
        InlineKeyboardButton("gpt-4-32k", callback_data="gpt-4-32k"),
    ],
    [
        InlineKeyboardButton("gpt-3.5-turbo-1106", callback_data="gpt-3.5-turbo-1106"),
    ],
    [
        InlineKeyboardButton("gpt-4-turbo-preview", callback_data="gpt-4-turbo-preview"),
    ],
    [
        InlineKeyboardButton("gpt-4-0125-preview", callback_data="gpt-4-0125-preview"),
    ],
    [
        InlineKeyboardButton("gpt-4-1106-preview", callback_data="gpt-4-1106-preview"),
    ],
    [
        InlineKeyboardButton("gpt-4-vision-preview", callback_data="gpt-4-vision-preview"),
    ],
    [
        InlineKeyboardButton("claude-2", callback_data="claude-2"),
    ],
    [
        InlineKeyboardButton("返回上一级", callback_data="返回上一级"),
    ],
]

def get_plugins_status(item):
    return "✅" if config.PLUGINS[item] else "☑️"

def update_first_buttons_message():
    history = "✅" if config.PASS_HISTORY else "☑️"
    language = "🇨🇳 中文" if config.LANGUAGE == "Simplified Chinese" else "🇺🇸 English"

    first_buttons = [
        [
            InlineKeyboardButton("更换问答模型", callback_data="更换问答模型"),
            InlineKeyboardButton(language, callback_data="language"),
            InlineKeyboardButton(f"历史记录 {history}", callback_data="PASS_HISTORY"),
        ],
        [
            InlineKeyboardButton(f"搜索 {get_plugins_status('SEARCH_USE_GPT')}", callback_data='SEARCH_USE_GPT'),
            InlineKeyboardButton(f"当前时间 {get_plugins_status('DATE')}", callback_data='DATE'),
        ],
        [
            InlineKeyboardButton(f"URL 总结 {get_plugins_status('URL')}", callback_data='URL'),
            InlineKeyboardButton(f"版本信息 {get_plugins_status('VERSION')}", callback_data='VERSION'),
            # InlineKeyboardButton(f"gpt4free {get_plugins_status('USE_G4F')}", callback_data='USE_G4F'),
        ],
    ]
    return first_buttons

def replace_with_asterisk(string, start=10, end=45):
    return string[:start] + '*' * (end - start) + string[end:]

def update_info_message(update):
    return (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"**Default engine:** `{config.GPT_ENGINE}`\n"
        f"**Temperature:** `{config.temperature}`\n"
        f"**API_URL:** `{config.API_URL}`\n\n"
        f"**API:** `{replace_with_asterisk(config.API)}`\n\n"
        f"**WEB_HOOK:** `{config.WEB_HOOK}`\n\n"
    )

banner = "👇下面可以随时更改默认 gpt 模型："
@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def button_press(update, context):
    """Function to handle the button press"""
    info_message = update_info_message(update)
    callback_query = update.callback_query
    await callback_query.answer()
    data = callback_query.data
    if "gpt-" in data or "claude" in data:
        config.GPT_ENGINE = data
        if (config.API and "gpt-" in data) or (config.API and not config.ClaudeAPI):
            config.ChatGPTbot = GPT(api_key=f"{config.API}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
            config.ChatGPTbot.reset(convo_id=str(update.effective_chat.id), system_prompt=config.systemprompt)
        if config.ClaudeAPI and "claude" in data:
            config.claudeBot = claudebot(api_key=f"{config.ClaudeAPI}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
        try:
            info_message = update_info_message(update)
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
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )
    elif "language" in data:
        if config.LANGUAGE == "Simplified Chinese":
            config.LANGUAGE = "English"
            config.systemprompt = config.systemprompt.replace("Simplified Chinese", "English")
        else:
            config.LANGUAGE = "Simplified Chinese"
            config.systemprompt = config.systemprompt.replace("English", "Simplified Chinese")
        # config.systemprompt = f"You are ChatGPT, a large language model trained by OpenAI. Respond conversationally in {config.LANGUAGE}. Knowledge cutoff: 2021-09. Current date: [ {config.Current_Date} ]"
        if config.API:
            config.ChatGPTbot = GPT(api_key=f"{config.API}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)
            config.ChatGPTbot.reset(convo_id=str(update.effective_chat.id), system_prompt=config.systemprompt)
        if config.ClaudeAPI:
            config.claudeBot = claudebot(api_key=f"{config.ClaudeAPI}", engine=config.GPT_ENGINE, system_prompt=config.systemprompt, temperature=config.temperature)

        info_message = update_info_message(update)
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )
    else:
        try:
            config.PLUGINS[data] = not config.PLUGINS[data]
        except:
            setattr(config, data, not getattr(config, data))
        info_message = update_info_message(update)
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )

@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def info(update, context):
    info_message = update_info_message(update)
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(info_message), reply_markup=InlineKeyboardMarkup(update_first_buttons_message()), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.GroupAuthorization
@decorators.Authorization
async def handle_pdf(update, context):
    # 获取接收到的文件
    pdf_file = update.message.document
    # 得到文件的url
    file_id = pdf_file.file_id
    new_file = await context.bot.get_file(file_id)
    file_url = new_file.file_path
    extracted_text_with_prompt = Document_extract(file_url)
    # print(extracted_text_with_prompt)
    if config.ClaudeAPI and "claude" in config.GPT_ENGINE:
        robot = config.claudeBot
        role = "Human"
    else:
        robot = config.ChatGPTbot
        role = "user"
    robot.add_to_conversation(extracted_text_with_prompt, role, str(update.effective_chat.id))
    message = (
        f"文档上传成功！\n\n"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.GroupAuthorization
@decorators.Authorization
async def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=update.effective_user.id,
            title="Reverse",
            input_message_content=InputTextMessageContent(query[::-1], parse_mode='MarkdownV2'))
    ]

    await update.inline_query.answer(results)

# @decorators.GroupAuthorization
# @decorators.Authorization
# async def qa(update, context):
#     if (len(context.args) != 2):
#         message = (
#             f"格式错误哦~，需要两个参数，注意路径或者链接、问题之间的空格\n\n"
#             f"请输入 `/qa 知识库链接 要问的问题`\n\n"
#             f"例如知识库链接为 https://abc.com ，问题是 蘑菇怎么分类？\n\n"
#             f"则输入 `/qa https://abc.com 蘑菇怎么分类？`\n\n"
#             f"问题务必不能有空格，👆点击上方命令复制格式\n\n"
#             f"除了输入网址，同时支持本地知识库，本地知识库文件夹路径为 `./wiki`，问题是 蘑菇怎么分类？\n\n"
#             f"则输入 `/qa ./wiki 蘑菇怎么分类？`\n\n"
#             f"问题务必不能有空格，👆点击上方命令复制格式\n\n"
#             f"本地知识库目前只支持 Markdown 文件\n\n"
#         )
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
#         return
#     print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
#     await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
#     result = await docQA(context.args[0], context.args[1], get_doc_from_local)
#     print(result["answer"])
#     # source_url = set([i.metadata['source'] for i in result["source_documents"]])
#     # source_url = "\n".join(source_url)
#     # message = (
#     #     f"{result['result']}\n\n"
#     #     f"参考链接：\n"
#     #     f"{source_url}"
#     # )
#     await context.bot.send_message(chat_id=update.message.chat_id, text=escape(result["answer"]), parse_mode='MarkdownV2', disable_web_page_preview=True)

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
    # await update.message.reply_text(escape("出错啦！请重试。"), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.GroupAuthorization
@decorators.Authorization
async def unknown(update, context): # 当用户输入未知命令时，返回文本
    return
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand('info', 'basic information'),
        BotCommand('pic', 'Generate image'),
        BotCommand('copilot', 'Advanced search mode'),
        BotCommand('search', 'search Google or duckduckgo'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
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
    application.add_handler(CommandHandler("pic", image, block = False))
    application.add_handler(CommandHandler("search", lambda update, context: command_bot(update, context, prompt="search: ", title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command="search")))
    # application.add_handler(CommandHandler("search", lambda update, context: search(update, context, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot)))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, "Simplified Chinese", robot=config.translate_bot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=config.translate_bot)))
    application.add_handler(CommandHandler("copilot", lambda update, context: command_bot(update, context, None, None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.copilot_bot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(InlineQueryHandler(inlinequery))
    # application.add_handler(CommandHandler("qa", qa))
    application.add_handler(MessageHandler(filters.Document.PDF | filters.Document.TXT | filters.Document.DOC, handle_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.CAPTION & filters.PHOTO & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    if WEB_HOOK:
        print("WEB_HOOK:", WEB_HOOK)
        application.run_webhook("0.0.0.0", PORT, webhook_url=WEB_HOOK)
    else:
        # application.run_polling()
        time_out = 600
        application.run_polling(read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out, timeout=time_out)
        # application.run_polling(read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out, timeout=time_out)