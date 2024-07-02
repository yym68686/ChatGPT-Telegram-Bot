def CutNICK(update_text, update_message):
    import config
    botNick = config.NICK.lower() if config.NICK else None
    botNicKLength = len(botNick) if botNick else 0

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

async def get_file_url(file, context):
    file_id = file.file_id
    new_file = await context.bot.get_file(file_id)
    file_url = new_file.file_path
    return file_url

async def GetMesage(update_message, context):
    image_url = None
    file_url = None
    reply_to_message_text = None
    message = None
    rawtext = None
    reply_to_message_file_content = None

    chatid = str(update_message.chat_id)
    message_thread_id = update_message.message_thread_id
    if message_thread_id:
        convo_id = str(chatid) + "_" + str(message_thread_id)
    else:
        convo_id = str(chatid)

    messageid = update_message.message_id

    if update_message.text:
        message = CutNICK(update_message.text, update_message)
        rawtext = update_message.text

    if update_message.reply_to_message:
        reply_to_message_text = update_message.reply_to_message.text
        reply_to_message_file = update_message.reply_to_message.document
        if reply_to_message_file:
            reply_to_message_file_url = await get_file_url(reply_to_message_file, context)
            reply_to_message_file_content = Document_extract(reply_to_message_file_url, reply_to_message_file_url, None)

    if update_message.photo:
        photo = update_message.photo[-1]

        image_url = await get_file_url(photo, context)

        if update_message.caption:
            message = rawtext = CutNICK(update_message.caption, update_message)

    if update_message.document:
        file = update_message.document

        file_url = await get_file_url(file, context)

        if image_url == None and file_url and (file_url[-3:] == "jpg" or file_url[-3:] == "png" or file_url[-4:] == "jpeg"):
            image_url = file_url

        message = rawtext = CutNICK(update_message.caption, update_message)

    return message, rawtext, image_url, chatid, messageid, reply_to_message_text, message_thread_id, convo_id, file_url, reply_to_message_file_content

async def GetMesageInfo(update, context):
    if update.edited_message:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text, message_thread_id, convo_id, file_url, reply_to_message_file_content = await GetMesage(update.edited_message, context)
        update_message = update.edited_message
    elif update.callback_query:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text, message_thread_id, convo_id, file_url, reply_to_message_file_content = await GetMesage(update.callback_query.message, context)
        update_message = update.callback_query.message
    else:
        message, rawtext, image_url, chatid, messageid, reply_to_message_text, message_thread_id, convo_id, file_url, reply_to_message_file_content = await GetMesage(update.message, context)
        update_message = update.message
    return message, rawtext, image_url, chatid, messageid, reply_to_message_text, update_message, message_thread_id, convo_id, file_url, reply_to_message_file_content