import config

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from md2tgmd.src.md2tgmd import escape

from utils.i18n import strings
from utils.scripts import GetMesageInfo

def ban_message(update, convo_id):
    message = (
        f"`Hi, {update.effective_user.username}!`\n\n"
        f"id: `{update.effective_user.id}`\n\n"
        f"{strings['message_ban'][config.get_current_lang(convo_id)]}\n\n"
    )
    return escape(message, italic=False)

# 判断是否在白名单
def Authorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        _, _, _, chatid, _, _, _, message_thread_id, convo_id, _, _, _ = await GetMesageInfo(update, context, voice=False)
        if config.BLACK_LIST and chatid in config.BLACK_LIST:
            message = ban_message(update, convo_id)
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=message, parse_mode='MarkdownV2')
            return
        if config.whitelist == None or (config.GROUP_LIST and chatid in config.GROUP_LIST):
            return await func(*args, **kwargs)
        if config.whitelist and update.effective_user and str(update.effective_user.id) not in config.whitelist:
            message = ban_message(update, convo_id)
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否在群聊白名单
def GroupAuthorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        _, _, _, chatid, _, _, _, message_thread_id, convo_id, _, _, _ = await GetMesageInfo(update, context, voice=False)
        if config.GROUP_LIST == None:
            return await func(*args, **kwargs)
        if update.effective_chat == None or chatid[0] != "-":
            return await func(*args, **kwargs)
        if (chatid not in config.GROUP_LIST):
            if (config.ADMIN_LIST and str(update.effective_user.id) in config.ADMIN_LIST):
                return await func(*args, **kwargs)
            message = ban_message(update, convo_id)
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否是管理员
def AdminAuthorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        _, _, _, chatid, _, _, _, message_thread_id, convo_id, _, _, _ = await GetMesageInfo(update, context, voice=False)
        if config.ADMIN_LIST == None:
            return await func(*args, **kwargs)
        if (str(update.effective_user.id) not in config.ADMIN_LIST):
            message = ban_message(update, convo_id)
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

def APICheck(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        _, _, _, chatid, _, _, _, message_thread_id, convo_id, _, _, _ = await GetMesageInfo(update, context, voice=False)
        from config import (
            Users,
            get_robot,
            get_current_lang,
            CLAUDE_API,
        )
        from md2tgmd.src.md2tgmd import escape
        from utils.i18n import strings
        robot, role, api_key, api_url = get_robot(convo_id)
        if robot == None or (api_key == None and CLAUDE_API == None):
            await context.bot.send_message(
                chat_id=chatid,
                message_thread_id=message_thread_id,
                text=escape(strings['message_api_none'][get_current_lang(convo_id)]),
                parse_mode='MarkdownV2',
            )
            return
        if (api_key and api_key.endswith("your_api_key")) or (api_url and api_url.endswith("your_api_url")):
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=escape(strings['message_api_error'][get_current_lang()]), parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

def PrintMessage(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        import json
        print("\033[32m")
        print(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))
        print("\033[0m")
        return await func(*args, **kwargs)
    return wrapper