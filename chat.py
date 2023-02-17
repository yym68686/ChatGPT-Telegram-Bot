import sys
from config import config
# from revChatGPT.revChatGPT import AsyncChatbot
from revChatGPT.V1 import Chatbot

# chatbot = AsyncChatbot(config, conversation_id=None)
chatbot = Chatbot(config)

# def resetChat():
#     chatbot.reset_chat() # Forgets conversation

# def refreshSession():
#     chatbot.refresh_session() # Uses the session_token to get a new bearer token
#     print("refresh session Success!")

def getResult(prompt):
    for data in chatbot.ask(prompt):
        response = data["message"]
    print("getresult", response)
    return response

if __name__ == '__main__':
    getResult(sys.argv[1])