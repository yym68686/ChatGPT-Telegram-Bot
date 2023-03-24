import sys
import json
import asyncio
from EdgeGPT import Chatbot as BingAI, ConversationStyle
from config import COOKIES

bot = BingAI(cookies=json.loads(COOKIES))
async def getBing(message):
    try:
        # creative balanced precise
        result = await bot.ask(prompt=message, conversation_style=ConversationStyle.creative)
        numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
        maxNumMessages = result["item"]["throttling"]["maxNumUserMessagesInConversation"]
        print(numMessages, "/", maxNumMessages, end="")
        result = result["item"]["messages"][1]["text"]
        if numMessages == maxNumMessages - 1:
            bot.reset()
    except Exception as e:
        print("response_msg", result)
        print("Exception", e)
        print("Exception str", str(e))
        result = "Bing 出错啦。"
    print(" BingAI", result)
    return result

if __name__ == "__main__":
    asyncio.run(bing(sys.argv[1]))