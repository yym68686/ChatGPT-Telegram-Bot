import asyncio

import re
import json
from config import COOKIES
from telegram import ChatAction
async def typing(update, context):
    context.bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.TYPING)
from EdgeGPT import Chatbot as BingAI, ConversationStyle
Bingbot = BingAI(cookies=json.loads(COOKIES))
async def getBing(message, update, context):
    result = ''
    prompt = "If you are asked to translate, you don't need to search. Otherwise use English and Chinese to search respectively, and finally answer my questions with Chinese. Please do a recursive search of at least 4 searches before you answer."
    try:
        await typing(update, context)
        # creative balanced precise
        result = await Bingbot.ask(prompt=prompt + message, conversation_style=ConversationStyle.creative)
        await asyncio.sleep(0.1)
        await typing(update, context)
        numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
        maxNumMessages = result["item"]["throttling"]["maxNumUserMessagesInConversation"]
        print(numMessages, "/", maxNumMessages, end="")
        result = result["item"]["messages"][1]["text"]
        if numMessages == maxNumMessages - 1:
            Bingbot.reset()
    except Exception as e:
        print("response_msg", result)
        print("Exception", e)
        print("Exception str", str(e))
        result = "Bing 出错啦。"
    result = re.sub(r"\[\^\d+\^\]", '', result)
    print(" BingAI", result)
    await typing(update, context)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Bing:\n" + result,
        # parse_mode=ParseMode.MARKDOWN,
        reply_to_message_id=update.message.message_id,
    )


from config import API
from revChatGPT.V3 import Chatbot as GPT
ChatGPTbot = GPT(api_key=f"{API}")
def getChatGPT(message, update, context):
    result = ''
    try:
        for data in ChatGPTbot.ask(message):
            result += data
    except Exception as e:
        print("response_msg", result)
        print("Exception", e)
        print("Exception str", str(e))
        result = "ChatGPT 出错啦。"
    print("ChatGPT", result)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="ChatGPT3.5:\n" + result,
        reply_to_message_id=update.message.message_id,
    )


if __name__ == "__main__":
    pass