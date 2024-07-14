import config

# 判断是否在白名单
def Authorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        from utils.scripts import GetMesageInfo
        _, _, _, chatid, _, _, _, _, _, _, _ = await GetMesageInfo(update, context)
        if config.whitelist == None or chatid in config.GROUP_LIST:
            return await func(*args, **kwargs)
        if (update.effective_user.id not in config.whitelist):
            message = (
                f"`Hi, {update.effective_user.username}!`\n\n"
                f"id: `{update.effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await context.bot.send_message(chat_id=chatid, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否在群聊白名单
def GroupAuthorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        from utils.scripts import GetMesageInfo
        _, _, _, chatid, _, _, _, _, _, _, _ = await GetMesageInfo(update, context)
        if config.GROUP_LIST == None:
            return await func(*args, **kwargs)
        if update.effective_chat == None or chatid[0] != "-":
            return await func(*args, **kwargs)
        if (chatid not in config.GROUP_LIST):
            if (config.ADMIN_LIST and update.effective_user.id in config.ADMIN_LIST):
                return await func(*args, **kwargs)
            message = (
                f"`Hi, {update.effective_user.username}!`\n\n"
                f"id: `{update.effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await context.bot.send_message(chat_id=chatid, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否是管理员
def AdminAuthorization(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        if config.ADMIN_LIST == None:
            return await func(*args, **kwargs)
        if (update.effective_user.id not in config.ADMIN_LIST):
            message = (
                f"`Hi, {update.effective_user.username}!`\n\n"
                f"id: `{update.effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await context.bot.send_message(chat_id=update.effective_user.id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

def APICheck(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        from utils.scripts import GetMesageInfo
        _, _, _, chatid, _, _, _, message_thread_id, convo_id, _, _ = await GetMesageInfo(update, context)
        from config import (
            Users,
            get_robot,
            get_current_lang,
        )
        from md2tgmd.src.md2tgmd import escape
        from utils.i18n import strings
        api_key = Users.get_config(convo_id, "api_key")
        api_url = Users.get_config(convo_id, "api_url")
        robot, role = get_robot(convo_id)
        if robot == None or api_key == None:
            await context.bot.send_message(
                chat_id=chatid,
                message_thread_id=message_thread_id,
                text=escape(strings['message_api_none'][get_current_lang()]),
                parse_mode='MarkdownV2',
            )
            return
        if api_key.endswith("your_api_key") or api_url.endswith("your_api_url"):
            await context.bot.send_message(chat_id=chatid, message_thread_id=message_thread_id, text=escape(strings['message_api_error'][get_current_lang()]), parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

def PrintMessage(func):
    async def wrapper(*args, **kwargs):
        update, context = args[:2]
        from utils.scripts import GetMesageInfo
        _, rawtext, _, _, _, _, _, _, _, _, _ = await GetMesageInfo(update, context)
        import json
        print("update", json.dumps(update.to_dict(), indent=2, ensure_ascii=False))
        print("\033[32m", update.effective_user.username, update.effective_user.id, rawtext, "\033[0m")
        return await func(*args, **kwargs)
    return wrapper