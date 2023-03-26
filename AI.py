import asyncio

import json
from config import COOKIES
from EdgeGPT import Chatbot as BingAI, ConversationStyle
Bingbot = BingAI(cookies=json.loads(COOKIES))
async def getBing(message, update, context):
    try:
        # creative balanced precise
        result = await Bingbot.ask(prompt=message, conversation_style=ConversationStyle.creative)
        await asyncio.sleep(0.1)
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
    print(" BingAI", result)
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
        print("getresult", result)
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