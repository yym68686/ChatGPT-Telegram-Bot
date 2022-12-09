import sys
from config import config
from revChatGPT.revChatGPT import Chatbot

chatbot = Chatbot(config, conversation_id=None)

def resetChat():
    chatbot.reset_chat() # Forgets conversation

def refreshSession():
    chatbot.refresh_session() # Uses the session_token to get a new bearer token
    print("refresh session Success!")

def getResult(prompt):
    chatbot.refresh_session() # Uses the session_token to get a new bearer token
    resp = chatbot.get_chat_response(prompt, output="text") # Sends a request to the API and returns the response by OpenAI
    print("getresult", resp['message'])
    return resp['message']

if __name__ == '__main__':
    getResult(sys.argv[1])