import config

# 判断是否在白名单
def Authorization(func):
    async def wrapper(*args, **kwargs):
        if config.whitelist == None:
            return await func(*args, **kwargs)
        if (args[0].effective_user.id not in config.whitelist):
            message = (
                f"`Hi, {args[0].effective_user.username}!`\n\n"
                f"id: `{args[0].effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await args[1].bot.send_message(chat_id=args[0].effective_user.id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否在群聊白名单
def GroupAuthorization(func):
    async def wrapper(*args, **kwargs):
        if config.GROUP_LIST == None:
            return await func(*args, **kwargs)
        if (args[0].effective_chat.id not in config.GROUP_LIST):
            if (args[0].effective_user.id in config.ADMIN_LIST and config.ADMIN_LIST):
                return await func(*args, **kwargs)
            message = (
                f"`Hi, {args[0].effective_user.username}!`\n\n"
                f"id: `{args[0].effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper

# 判断是否是管理员
def AdminAuthorization(func):
    async def wrapper(*args, **kwargs):
        if config.ADMIN_LIST == None:
            return await func(*args, **kwargs)
        if (args[0].effective_user.id not in config.ADMIN_LIST):
            message = (
                f"`Hi, {args[0].effective_user.username}!`\n\n"
                f"id: `{args[0].effective_user.id}`\n\n"
                f"无权访问！\n\n"
            )
            await args[1].bot.send_message(chat_id=args[0].effective_user.id, text=message, parse_mode='MarkdownV2')
            return
        return await func(*args, **kwargs)
    return wrapper