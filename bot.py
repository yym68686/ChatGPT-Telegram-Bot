import re
import sys
sys.dont_write_bytecode = True
import logging
import traceback
import utils.decorators as decorators
from md2tgmd import escape

from ModelMerge.plugins import PLUGINS
from ModelMerge.utils.prompt import translator_en2zh_prompt, translator_prompt, claude3_doc_assistant_prompt
from ModelMerge.utils.scripts import Document_extract, claude_replace

import config
from config import (
    WEB_HOOK,
    PORT,
    BOT_TOKEN,
    Users,
    PREFERENCES,
    LANGUAGES,
    update_first_buttons_message,
    get_current_lang,
    update_info_message,
    update_ENGINE,
    reset_ENGINE,
    get_robot,
    get_image_message,
    get_ENGINE,
    update_language_status,
    update_models_buttons,
    update_menu_buttons,
)

from utils.i18n import strings

from telegram.constants import ChatAction
from telegram import BotCommand, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters, CallbackQueryHandler, Application, AIORateLimiter, InlineQueryHandler

import asyncio
lock = asyncio.Lock()
event = asyncio.Event()

from collections import defaultdict
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.CRITICAL)

httpx_logger = logging.getLogger("chromadb.telemetry.posthog")
httpx_logger.setLevel(logging.WARNING)

class SpecificStringFilter(logging.Filter):
    def __init__(self, specific_string):
        super().__init__()
        self.specific_string = specific_string

    def filter(self, record):
        return self.specific_string not in record.getMessage()

specific_string = "httpx.RemoteProtocolError: Server disconnected without sending a response."
my_filter = SpecificStringFilter(specific_string)

update_logger = logging.getLogger("telegram.ext.Updater")
update_logger.addFilter(my_filter)
update_logger = logging.getLogger("root")
update_logger.addFilter(my_filter)


botNick = config.NICK.lower() if config.NICK else None
botNicKLength = len(botNick) if botNick else 0
print("nick:", botNick)

def CutNICK(update_text, update_message):
    update_chat = update_message.chat
    update_reply_to_message = update_message.reply_to_message
    if botNick is None:
        return update_text
    else:
        if update_text[:botNicKLength].lower() == botNick:
            return update_text[botNicKLength:].strip()
        else:
            if update_chat.type == 'private' or (botNick and update_reply_to_message and update_reply_to_message.text and update_reply_to_message.from_user.is_bot and update_reply_to_message.sender_chat == None):
                return update_text
            else:
                return None

async def GetMesage(update_message, context):
    image_url = None
    reply_to_message_text = None
    chatid = update_message.chat_id
    messageid = update_message.message_id
    if update_message.text:
        message = CutNICK(update_message.text, update_message)
        rawtext = update_message.text

    if update_message.reply_to_message:
        reply_to_message_text = update_message.reply_to_message.text

    if update_message.photo:
        photo = update_message.photo[-1]
        file_id = photo.file_id
        photo_file = await context.bot.getFile(file_id)
        image_url = photo_file.file_path

        message = rawtext = CutNICK(update_message.caption, update_message)
    return message, rawtext, image_url, chatid, messageid, reply_to_message_text

# 定义一个缓存来存储消息
message_cache = defaultdict(lambda: [])
time_stamps = defaultdict(lambda: [])

@decorators.GroupAuthorization
@decorators.Authorization
async def command_bot(update, context, language=None, prompt=translator_prompt, title="", robot=None, has_command=True):
    print("update", update)
    image_url = None
    if update.edited_message:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text = await GetMesage(update.edited_message, context)
        update_message = update.edited_message
    else:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text = await GetMesage(update.message, context)
        update_message = update.message

    print("\033[32m", update.effective_user.username, update.effective_user.id, rawtext, "\033[0m")

    if has_command == False or len(context.args) > 0:
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
            if reply_to_message_text and update_message.reply_to_message.from_user.is_bot:
                message = '\n'.join(reply_to_message_text.split('\n')[1:]) + "\n" + message
            elif reply_to_message_text and not update_message.reply_to_message.from_user.is_bot:
                message = reply_to_message_text + "\n" + message

            if robot is None:
                robot, role = get_robot(chatid)
            engine = get_ENGINE(chatid)

            if PREFERENCES["LONG_TEXT"]:
                async with lock:
                    if len(message_cache[chatid]) == 0:
                        event.set()
                    message_cache[chatid].append(message)
                    time_stamps[chatid].append(time.time())
                    if len(message_cache[chatid]) > 1:
                        return

                while True:
                    if len(message_cache[chatid]) == 1:
                        print("first message len:", len(message_cache[chatid][0]))
                        if len(message_cache[chatid][0]) < 2000:
                            break
                    event.clear()
                    try:
                        await asyncio.wait_for(event.wait(), timeout=0.78)
                    except asyncio.TimeoutError:
                        break

                intervals = [
                    time_stamps[chatid][i] - time_stamps[chatid][i - 1]
                    for i in range(1, len(time_stamps[chatid]))
                ]
                print(f"Chat ID {chatid} 时间间隔: {intervals}")

                message = "\n".join(message_cache[chatid])
                message_cache[chatid] = []
                time_stamps[chatid] = []

            if "gpt" in engine or (config.CLAUDE_API and "claude-3" in engine):
                message = [{"type": "text", "text": message}]
            message = get_image_message(image_url, message, chatid)
            await context.bot.send_chat_action(chat_id=chatid, action=ChatAction.TYPING)
            if PREFERENCES["TITLE"]:
                title = f"`🤖️ {engine}`\n\n"
            await getChatGPT(update, context, title, robot, message, chatid, messageid)
    else:
        message = await context.bot.send_message(
            chat_id=chatid,
            text="请在命令后面放入文本。",
            parse_mode='MarkdownV2',
            reply_to_message_id=messageid,
        )

async def delete_message(update, context, messageid, delay=60):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=messageid)
    except Exception as e:
        print('\033[31m')
        print("error", e)
        print('\033[0m')

@decorators.GroupAuthorization
@decorators.Authorization
async def reset_chat(update, context):
    message = None
    if (len(context.args) > 0):
        message = ' '.join(context.args)
    reset_ENGINE(update.message.chat_id, message)

    remove_keyboard = ReplyKeyboardRemove()
    message = await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
        reply_markup=remove_keyboard,
    )
    await delete_message(update, context, message.message_id)

async def getChatGPT(update, context, title, robot, message, chatid, messageid):
    result = ""
    text = message
    modifytime = 0
    time_out = 600
    model_name = Users.get_config(chatid, "engine")
    Frequency_Modification = 20
    if "gemini" in model_name:
        Frequency_Modification = 2
    lastresult = title
    tmpresult = ""

    message = await context.bot.send_message(
        chat_id=chatid,
        text=strings['message_think'][get_current_lang()],
        parse_mode='MarkdownV2',
        reply_to_message_id=messageid,
    )
    answer_messageid = message.message_id
    pass_history = PREFERENCES["PASS_HISTORY"]
    image_has_send = 0

    try:
        for data in robot.ask_stream(text, convo_id=str(chatid), pass_history=pass_history, model=model_name):
            if "🌐" not in data:
                result = result + data
            tmpresult = result
            if re.sub(r"```", '', result.split("\n")[-1]).count("`") % 2 != 0:
                tmpresult = result + "`"
            if sum([line.strip().startswith("```") for line in result.split('\n')]) % 2 != 0:
                tmpresult = tmpresult + "\n```"
            tmpresult = title + tmpresult
            if "claude" in model_name:
                tmpresult = claude_replace(tmpresult)
            if "🌐" in data:
                tmpresult = data
            history = robot.conversation[str(chatid)]
            if history[-1].get('name') == "generate_image" and not image_has_send:
                await context.bot.send_photo(chat_id=chatid, photo=history[-1]['content'], reply_to_message_id=answer_messageid)
                image_has_send = 1
            modifytime = modifytime + 1
            if (modifytime % Frequency_Modification == 0 and lastresult != tmpresult) or "🌐" in data:
                await context.bot.edit_message_text(chat_id=chatid, message_id=answer_messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        traceback.print_exc()
        print(tmpresult)
        print('\033[0m')
        if config.API:
            robot.reset(convo_id=str(chatid), system_prompt=config.systemprompt)
        tmpresult = f"{tmpresult}\n\n`{e}`"
    print(tmpresult)
    if lastresult != tmpresult and answer_messageid:
        if "Can't parse entities: can't find end of code entity at byte offset" in tmpresult:
            # await context.bot.edit_message_text(chat_id=chatid, message_id=messageid, text=tmpresult, disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
            await update.message.reply_text(tmpresult)
            print(escape(tmpresult))
        else:
            sent_message = await context.bot.edit_message_text(chat_id=chatid, message_id=answer_messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
    if PREFERENCES["FOLLOW_UP"]:
        prompt = (
            f"You are a professional Q&A expert. You will now be given reference information. Based on the reference information, please help me ask three most relevant questions that you most want to know from my perspective. Be concise and to the point. Do not have numbers in front of questions. Separate each question with a line break. Only output three questions in {config.LANGUAGE}, no need for any explanation. reference infomation is provided inside <infomation></infomation> XML tags."
            "Here is the reference infomation, inside <infomation></infomation> XML tags:"
            "<infomation>"
            "{}"
            "</infomation>"
        ).format("\n\n".join(tmpresult.split("\n\n")[1:]))
        result = config.SummaryBot.ask(prompt, convo_id=str(chatid), pass_history=False).split('\n')
        keyboard = []
        result = [i for i in result if i.strip() and len(i) > 5]
        print(result)
        for ques in result:
            keyboard.append([KeyboardButton(ques)])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await context.bot.delete_message(chat_id=chatid, message_id=sent_message.message_id)
        await update.message.reply_text(text=escape(tmpresult), parse_mode='MarkdownV2', reply_to_message_id=messageid, reply_markup=reply_markup)

@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def button_press(update, context):
    """Function to handle the button press"""
    callback_query = update.callback_query
    chatid = callback_query.message.chat_id
    info_message = update_info_message(chatid)
    await callback_query.answer()
    data = callback_query.data
    # print("data", data)
    banner = strings['message_banner'][get_current_lang()]
    if data.endswith("_MODELS"):
        data = data[:-7]
        update_ENGINE(data, chatid)
        try:
            info_message = update_info_message(chatid)
            if  info_message + banner != callback_query.message.text:
                message = await callback_query.edit_message_text(
                    text=escape(info_message + banner),
                    reply_markup=InlineKeyboardMarkup(update_models_buttons()),
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.info(e)
            pass
    elif data.startswith("MODELS"):
        message = await callback_query.edit_message_text(
            text=escape(info_message + banner),
            reply_markup=InlineKeyboardMarkup(update_models_buttons()),
            parse_mode='MarkdownV2'
        )
    elif data.endswith("_LANGUAGES"):
        data = data[:-10]
        update_language_status(data)
        try:
            info_message = update_info_message(chatid)
            if  info_message != callback_query.message.text:
                message = await callback_query.edit_message_text(
                    text=escape(info_message),
                    reply_markup=InlineKeyboardMarkup(update_menu_buttons(LANGUAGES, "_LANGUAGES")),
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.info(e)
            pass
    elif data.startswith("LANGUAGE"):
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_menu_buttons(LANGUAGES, "_LANGUAGES")),
            parse_mode='MarkdownV2'
        )
    if data.endswith("_PREFERENCES"):
        data = data[:-12]
        try:
            PREFERENCES[data] = not PREFERENCES[data]
        except Exception as e:
            logger.info(e)
        try:
            info_message = update_info_message(chatid)
            if  info_message != callback_query.message.text:
                message = await callback_query.edit_message_text(
                    text=escape(info_message),
                    reply_markup=InlineKeyboardMarkup(update_menu_buttons(PREFERENCES, "_PREFERENCES")),
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.info(e)
            pass
    elif data.startswith("PREFERENCES"):
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_menu_buttons(PREFERENCES, "_PREFERENCES")),
            parse_mode='MarkdownV2'
        )
    if data.endswith("_PLUGINS"):
        data = data[:-8]
        try:
            PLUGINS[data] = not PLUGINS[data]
        except Exception as e:
            logger.info(e)
        try:
            info_message = update_info_message(chatid)
            if  info_message != callback_query.message.text:
                message = await callback_query.edit_message_text(
                    text=escape(info_message),
                    reply_markup=InlineKeyboardMarkup(update_menu_buttons(PLUGINS, "_PLUGINS")),
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.info(e)
            pass
    elif data.startswith("PLUGINS"):
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_menu_buttons(PLUGINS, "_PLUGINS")),
            parse_mode='MarkdownV2'
        )

    elif data.startswith("BACK"):
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )

@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def info(update, context):
    chatid = update.message.chat_id
    info_message = update_info_message(chatid)
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(info_message), reply_markup=InlineKeyboardMarkup(update_first_buttons_message()), parse_mode='MarkdownV2', disable_web_page_preview=True)
    await delete_message(update, context, message.message_id)

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
    robot, role = get_robot()
    robot.add_to_conversation(extracted_text_with_prompt, role, str(update.effective_chat.id))
    chatid = update.message.chat_id
    engine = get_ENGINE(chatid)
    if config.CLAUDE_API and "claude-3" in engine:
        robot.add_to_conversation(claude3_doc_assistant_prompt, "assistant", str(update.effective_chat.id))
    message = (
        f"文档上传成功！\n\n"
    )
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
    await delete_message(update, context, message.message_id)


@decorators.GroupAuthorization
@decorators.Authorization
async def handle_photo(update, context):
    if update.edited_message:
        update_message = update.edited_message
    else:
        update_message = update.message

    chatid = update_message.chat_id
    messageid = update_message.message_id

    photo = update_message.photo[-1]
    file_id = photo.file_id
    photo_file = await context.bot.getFile(file_id)
    image_url = photo_file.file_path

    robot, role = get_robot()
    message = get_image_message(image_url, [], chatid)

    robot.add_to_conversation(message, role, str(chatid))
    # if config.CLAUDE_API and "claude-3" in config.GPT_ENGINE:
    #     robot.add_to_conversation(claude3_doc_assistant_prompt, "assistant", str(update.effective_chat.id))
    message = (
        f"图片上传成功！\n\n"
    )
    message = await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)
    await delete_message(update, context, message.message_id)

# DEBOUNCE_TIME = 4
@decorators.GroupAuthorization
@decorators.Authorization
async def inlinequery(update: Update, context) -> None:
    """Handle the inline query."""
    # current_time = time.time()

    # # 获取上次查询时间
    # if context.user_data == {}:
    #     context.user_data['last_query_time'] = current_time
    # last_query_time = context.user_data.get('last_query_time', 0)
    # context.user_data['last_query_time'] = current_time

    # # 如果距离上次查询时间不足去抖动时间，则跳过处理
    # print("current_time - last_query_time", current_time - last_query_time)
    # if current_time - last_query_time < DEBOUNCE_TIME:
    #     return

    chatid = update.effective_user.id
    engine = get_ENGINE(chatid)
    query = update.inline_query.query
    # 调用 getChatGPT 函数获取结果
    if (query.endswith(';') or query.endswith('；')) and query.strip():
        prompt = "Answer the following questions as concisely as possible:\n\n"
        result = config.ChatGPTbot.ask(prompt + query, convo_id=str(chatid), pass_history=False)

        results = [
            InlineQueryResultArticle(
                id=str(chatid),
                title=f"{engine}",
                thumbnail_url="https://pb.yym68686.top/TTGk",
                description=f"{result}",
                input_message_content=InputTextMessageContent(escape(result), parse_mode='MarkdownV2')),
        ]

        await update.inline_query.answer(results)

async def start(update, context): # 当用户输入/start时，返回文本
    user = update.effective_user
    message = (
        f"Hi `{user.username}` ! I am an Assistant, a large language model trained by OpenAI. I will do my best to help answer your questions.\n\n"
        # "我是人见人爱的 ChatGPT~\n\n"
        # "欢迎访问 https://github.com/yym68686/ChatGPT-Telegram-Bot 查看源码\n\n"
        # "有 bug 可以联系 @yym68686"
    )

    await update.message.reply_text(escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

async def error(update, context):
    # if str(context.error) == "httpx.RemoteProtocolError: Server disconnected without sending a response.": return
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    traceback_string = traceback.format_exception(None, context.error, context.error.__traceback__)
    logger.warning('Error traceback: %s', ''.join(traceback_string))
    # await update.message.reply_text(escape("出错啦！请重试。"), parse_mode='MarkdownV2', disable_web_page_preview=True)

@decorators.GroupAuthorization
@decorators.Authorization
async def unknown(update, context): # 当用户输入未知命令时，返回文本
    return
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand('info', 'basic information'),
        BotCommand('reset', 'Reset the bot'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        # BotCommand('search', 'search Google or duckduckgo'),
        BotCommand('start', 'Start the bot'),
    ])

from http.server import BaseHTTPRequestHandler
import json
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        update = Update.de_json(json.loads(post_data), application.bot)

        async def process_update(update):
            await application.process_update(update)

        application.run_async(process_update(update))

        self.send_response(200)
        self.end_headers()
        return

if __name__ == '__main__':
    time_out = 600
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .connection_pool_size(50000)
        .read_timeout(time_out)
        .pool_timeout(time_out)
        .get_updates_read_timeout(time_out)
        .get_updates_write_timeout(time_out)
        .get_updates_pool_timeout(time_out)
        .get_updates_connect_timeout(time_out)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("search", lambda update, context: command_bot(update, context, prompt="search: ", has_command="search")))
    application.add_handler(CallbackQueryHandler(button_press))
    # application.add_handler(ChosenInlineResultHandler(chosen_inline_result))
    # application.add_handler(MessageHandler(filters.TEXT & filters.VIA_BOT, handle_message))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, "Simplified Chinese", robot=config.translate_bot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=config.translate_bot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(InlineQueryHandler(inlinequery))
    application.add_handler(MessageHandler(filters.Document.PDF | filters.Document.TXT | filters.Document.DOC, handle_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, has_command=False), block = False))
    application.add_handler(MessageHandler(filters.CAPTION & filters.PHOTO & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, has_command=False)))
    application.add_handler(MessageHandler(~filters.CAPTION & filters.PHOTO & ~filters.COMMAND, handle_photo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    if WEB_HOOK:
        print("WEB_HOOK:", WEB_HOOK)
        application.run_webhook("0.0.0.0", PORT, webhook_url=WEB_HOOK)
    else:
        application.run_polling(timeout=time_out)