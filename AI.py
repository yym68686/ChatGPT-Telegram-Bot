import asyncio

import json
from config import COOKIES
from EdgeGPT import Chatbot as BingAI, ConversationStyle
Bingbot = BingAI(cookies=json.loads(COOKIES))
async def getBing(message):
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
    return result


from config import API
from revChatGPT.V3 import Chatbot as GPT
ChatGPTbot = GPT(api_key=f"{API}")
def getChatGPT(message):
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
    return result


if __name__ == "__main__":
    pass