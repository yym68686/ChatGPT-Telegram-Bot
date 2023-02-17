import sys
from config import config
from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config)

def getResult(prompt):
    for data in chatbot.ask(prompt):
        response = data["message"]
    print("getresult", response)
    return response

if __name__ == '__main__':
    getResult(sys.argv[1])