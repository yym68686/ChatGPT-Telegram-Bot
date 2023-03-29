import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import re
import json
from config import COOKIES
from telegram import ChatAction
async def typing(update, context):
    context.bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.TYPING, timeout=60)
from EdgeGPT import Chatbot as BingAI, ConversationStyle
Bingbot = BingAI(cookies=json.loads(COOKIES))
async def getBing(message, update, context):
    await typing(update, context)
    result = ''
    prompt = "If you are asked to translate, you don't need to search. Otherwise use English and Chinese to search respectively, and finally answer my questions with Chinese. Please do a recursive search of at least 4 searches before you answer."
    try:
        # creative balanced precise
        result = await Bingbot.ask(prompt=prompt + message, conversation_style=ConversationStyle.balanced)
        numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
        maxNumMessages = result["item"]["throttling"]["maxNumUserMessagesInConversation"]
        print(numMessages, "/", maxNumMessages, end="")
        result = result["item"]["messages"][1]["text"]
        if numMessages == maxNumMessages - 1:
            Bingbot.reset()
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        print('\033[0m')
        result = "Bing 出错啦。"
    result = re.sub(r"\[\^\d+\^\]", '', result)
    print(" BingAI", result)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="▎Bing\n\n" + result,
        # parse_mode=ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id,
    )

async def resetBing():
    await Bingbot.reset()

from config import API
from revChatGPT.V3 import Chatbot as GPT
ChatGPTbot = GPT(api_key=f"{API}")
def getChatGPT(message, update, context):
    result = ''
    try:
        for data in ChatGPTbot.ask(message):
            result += data
    except Exception as e:
        print('\033[31m')
        print("response_msg", result)
        print("error", e)
        print('\033[0m')
        result = "ChatGPT 出错啦。"
    print("ChatGPT", result)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="▎ChatGPT3.5\n\n" + result,
        reply_to_message_id=update.message.message_id,
    )

def reset_chat(update, context):
    ChatGPTbot.reset()
    loop.run_until_complete(resetBing())
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="重置成功！",
    )

if __name__ == "__main__":
    pass