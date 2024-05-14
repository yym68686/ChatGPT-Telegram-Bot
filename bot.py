import re
import sys
sys.dont_write_bytecode = True
import logging
import traceback
import utils.decorators as decorators
from md2tgmd import escape

from ModelMerge.models.config import PLUGINS
from ModelMerge.utils.prompt import translator_en2zh_prompt, translator_prompt, claude3_doc_assistant_prompt
from ModelMerge.utils.scripts import Document_extract, get_encode_image, claude_replace

import config
from config import (
    WEB_HOOK,
    PORT,
    BOT_TOKEN,
    update_first_buttons_message,
    update_model_buttons,
    get_current_lang,
    update_info_message,
    update_ENGINE,
    reset_ENGINE,
    update_language,
    get_robot
)

from utils.i18n import strings

from telegram.constants import ChatAction
from telegram import BotCommand, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, filters, CallbackQueryHandler, Application, AIORateLimiter, InlineQueryHandler

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

            robot, role = get_robot()
            if "gpt" in config.GPT_ENGINE or (config.CLAUDE_API and "claude-3" in config.GPT_ENGINE):
                message = [{"type": "text", "text": message}]
            if image_url and (config.GPT_ENGINE == "gpt-4-turbo-2024-04-09" or "gpt-4o" in config.GPT_ENGINE):
                base64_image = get_encode_image(image_url)
                message.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                )
            # print("robot", robot)
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
    reset_ENGINE(update.message.chat_id)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
    )

async def getChatGPT(update, context, title, robot, message, chatid, messageid):
    result = ""
    text = message
    modifytime = 0
    time_out = 600
    Frequency_Modification = 20
    if "gemini" in title:
        Frequency_Modification = 2
    lastresult = title
    tmpresult = ""

    message = await context.bot.send_message(
        chat_id=chatid,
        text=strings['message_think'][get_current_lang()],
        parse_mode='MarkdownV2',
        reply_to_message_id=messageid,
    )
    messageid = message.message_id
    pass_history = config.PASS_HISTORY

    try:
        for data in robot.ask_stream(text, convo_id=str(chatid), pass_history=pass_history):
            if "🌐" not in data:
                result = result + data
            tmpresult = result
            if re.sub(r"```", '', result.split("\n")[-1]).count("`") % 2 != 0:
                tmpresult = result + "`"
            # if re.sub(r"```", '', result).count("`") % 2 != 0:
            #     tmpresult = result + "`"
            if sum([line.strip().startswith("```") for line in result.split('\n')]) % 2 != 0:
                tmpresult = tmpresult + "\n```"
            # if result.count("```") % 2 != 0:
            #     tmpresult = tmpresult + "\n```"
            tmpresult = title + tmpresult
            if "claude" in title:
                tmpresult = claude_replace(tmpresult)
            if "🌐" in data:
                tmpresult = data
            # if "answer:" in result:
            #     tmpresult = re.sub(r"thought:[\S\s]+?answer:\s", '', tmpresult)
            #     tmpresult = re.sub(r"action:[\S\s]+?answer:\s", '', tmpresult)
            #     tmpresult = re.sub(r"answer:\s", '', tmpresult)
            #     tmpresult = re.sub(r"thought:[\S\s]+", '', tmpresult)
            #     tmpresult = re.sub(r"action:[\S\s]+", '', tmpresult)
            # else:
            #     tmpresult = re.sub(r"thought:[\S\s]+", '', tmpresult)
            modifytime = modifytime + 1
            if (modifytime % Frequency_Modification == 0 and lastresult != tmpresult) or "🌐" in data:
                await context.bot.edit_message_text(chat_id=chatid, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2', disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        traceback.print_exc()
        print(tmpresult)
        print('\033[0m')
        if config.API:
            robot.reset(convo_id=str(chatid), system_prompt=config.systemprompt)
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=chatid, message_id=messageid)
            messageid = ''
            config.API = ''
        tmpresult = f"{tmpresult}\n\n`{e}`"
    print(tmpresult)
    if lastresult != tmpresult and messageid:
        if "Can't parse entities: can't find end of code entity at byte offset" in tmpresult:
            # await context.bot.edit_message_text(chat_id=chatid, message_id=messageid, text=tmpresult, disable_web_page_preview=True, read_timeout=time_out, write_timeout=time_out, pool_timeout=time_out, connect_timeout=time_out)
            await update.message.reply_text(tmpresult)
            print(escape(tmpresult))
        else:
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
        for data in robot.generate(text):
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

@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def button_press(update, context):
    """Function to handle the button press"""
    info_message = update_info_message()
    callback_query = update.callback_query
    await callback_query.answer()
    data = callback_query.data
    banner = strings['message_banner'][get_current_lang()]
    if data.endswith("ENGINE"):
        data = data[:-6]
        update_ENGINE(data)
        try:
            info_message = update_info_message()
            if  info_message + banner != callback_query.message.text:
                message = await callback_query.edit_message_text(
                    text=escape(info_message + banner),
                    reply_markup=InlineKeyboardMarkup(update_model_buttons()),
                    parse_mode='MarkdownV2'
                )
        except Exception as e:
            logger.info(e)
            pass
    elif "MODEL" in data:
        message = await callback_query.edit_message_text(
            text=escape(info_message + banner),
            reply_markup=InlineKeyboardMarkup(update_model_buttons()),
            parse_mode='MarkdownV2'
        )
    elif "BACK" in data:
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )
    elif "language" in data:
        update_language()
        update_ENGINE()
        info_message = update_info_message()
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )
    else:
        try:
            PLUGINS[data] = not PLUGINS[data]
        except:
            setattr(config, data, not getattr(config, data))
        info_message = update_info_message()
        message = await callback_query.edit_message_text(
            text=escape(info_message),
            reply_markup=InlineKeyboardMarkup(update_first_buttons_message()),
            parse_mode='MarkdownV2'
        )

@decorators.AdminAuthorization
@decorators.GroupAuthorization
@decorators.Authorization
async def info(update, context):
    info_message = update_info_message()
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
    robot, role = get_robot()
    robot.add_to_conversation(extracted_text_with_prompt, role, str(update.effective_chat.id))
    if config.CLAUDE_API and "claude-3" in config.GPT_ENGINE:
        robot.add_to_conversation(claude3_doc_assistant_prompt, "assistant", str(update.effective_chat.id))
    message = (
        f"文档上传成功！\n\n"
    )
    await context.bot.send_message(chat_id=update.message.chat_id, text=escape(message), parse_mode='MarkdownV2', disable_web_page_preview=True)

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

    base64_image = get_encode_image(image_url)
    if image_url and ("gpt-4" in config.GPT_ENGINE or (config.CLAUDE_API is None and "claude-3" in config.GPT_ENGINE)):
        message = [
            {
                "type": "image_url",
                "image_url": {
                    "url": base64_image
                }
            }
        ]
    if image_url and config.CLAUDE_API and "claude-3" in config.GPT_ENGINE:
        message = [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image.split(",")[1],
                }
            }
        ]

    # print(message)
    robot.add_to_conversation(message, role, str(chatid))
    # print(robot.conversation)
    # print(robot.conversation[str(chatid)])
    # if config.CLAUDE_API and "claude-3" in config.GPT_ENGINE:
    #     robot.add_to_conversation(claude3_doc_assistant_prompt, "assistant", str(update.effective_chat.id))
    message = (
        f"图片上传成功！\n\n"
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
        BotCommand('pic', 'Generate image'),
        # BotCommand('copilot', 'Advanced search mode'),
        BotCommand('search', 'search Google or duckduckgo'),
        BotCommand('en2zh', 'translate to Chinese'),
        BotCommand('zh2en', 'translate to English'),
        BotCommand('start', 'Start the bot'),
        BotCommand('reset', 'Reset the bot'),
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
    application.add_handler(CommandHandler("pic", image, block = False))
    application.add_handler(CommandHandler("search", lambda update, context: command_bot(update, context, prompt="search: ", title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command="search")))
    # application.add_handler(CommandHandler("search", lambda update, context: search(update, context, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot)))
    application.add_handler(CallbackQueryHandler(button_press))
    application.add_handler(CommandHandler("reset", reset_chat))
    application.add_handler(CommandHandler("en2zh", lambda update, context: command_bot(update, context, "Simplified Chinese", robot=config.translate_bot)))
    application.add_handler(CommandHandler("zh2en", lambda update, context: command_bot(update, context, "english", robot=config.translate_bot)))
    # application.add_handler(CommandHandler("copilot", lambda update, context: command_bot(update, context, None, None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.copilot_bot)))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(InlineQueryHandler(inlinequery))
    # application.add_handler(CommandHandler("qa", qa))
    application.add_handler(MessageHandler(filters.Document.PDF | filters.Document.TXT | filters.Document.DOC, handle_pdf))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(filters.CAPTION & filters.PHOTO & ~filters.COMMAND, lambda update, context: command_bot(update, context, prompt=None, title=f"`🤖️ {config.GPT_ENGINE}`\n\n", robot=config.ChatGPTbot, has_command=False)))
    application.add_handler(MessageHandler(~filters.CAPTION & filters.PHOTO & ~filters.COMMAND, handle_photo))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_error_handler(error)

    if WEB_HOOK:
        print("WEB_HOOK:", WEB_HOOK)
        application.run_webhook("0.0.0.0", PORT, webhook_url=WEB_HOOK)
    else:
        application.run_polling(timeout=time_out)