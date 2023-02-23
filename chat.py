import sys
from config import config
from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config)
def resetChat():
    chatbot.reset_chat()

def getResult(prompt):
    for data in chatbot.ask(prompt):
        try:
            response = data["message"]
        except:
            print("response", data)
            if "reloading the conversation" in data:
                resetChat()
                return "对话已超过上限，已重置聊天，请重试！"
            return "未知错误：" + str(data)
    print("getresult", response)
    return response

if __name__ == '__main__':
    getResult(sys.argv[1])