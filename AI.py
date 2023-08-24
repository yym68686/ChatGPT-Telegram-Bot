import re
from md2tgmd import escape
from config import API, API4, PASS_HISTORY
from revChatGPT.V3 import Chatbot as GPT

systemprompt = "You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: [ Current Date ]"
api = API
api4 = API4
if api:
    ChatGPTbot = GPT(api_key=f"{api}")
    Claude2bot = GPT(api_key=f"{api}", engine="claude-2-web")
if api4:
    ChatGPT4bot = GPT(api_key=f"{api4}", engine="gpt-4-0613")
    
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
            if data[0] == ' ': # claude-2-web bug fix
                data = data[1:]
            result = result + data
            tmpresult = result
            modifytime = modifytime + 1
            if re.sub(r"```", '', result).count("`") % 2 != 0:
                tmpresult = result + "`"
            if result.count("```") % 2 != 0:
                tmpresult = result + "\n```"
            if modifytime % 12 == 0 and lastresult != tmpresult:
                if title == 'claude2':
                    tmpresult = re.sub(r",", '，', tmpresult)
                await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2')
                lastresult = tmpresult
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        print('\033[0m')
        if api:
            robot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
        if "You exceeded your current quota, please check your plan and billing details." in str(e):
            print("OpenAI api 已过期！")
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
            messageid = ''
            api = ''
        result += f"`出错啦！{e}`"
    print(result)
    if lastresult != result and messageid:
        await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2')

async def reset_chat(update, context):
    if api:
        ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
    if api4:
        ChatGPT4bot.reset(convo_id=str(update.message.chat_id), system_prompt=systemprompt)
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="重置成功！",
    )