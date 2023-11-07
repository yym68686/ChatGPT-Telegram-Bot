import os
WEB_HOOK = os.environ.get('WEB_HOOK', None)
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
PORT = int(os.environ.get('PORT', '8080'))
NICK = os.environ.get('NICK', None)
API = os.environ.get('API', None)
PASS_HISTORY = (os.environ.get('PASS_HISTORY', "False") == "False") == False
USE_GOOGLE = (os.environ.get('USE_GOOGLE', "True") == "False") == False
if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
    USE_GOOGLE = False
temperature = float(os.environ.get('temperature', '0.5'))
GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-3.5-turbo-16k')
# DEFAULT_SEARCH_MODEL = os.environ.get('DEFAULT_SEARCH_MODEL', 'gpt-3.5-turbo-1106')
SEARCH_USE_GPT = (os.environ.get('SEARCH_USE_GPT', "True") == "False") == False
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
PDF_EMBEDDING = (os.environ.get('PDF_EMBEDDING', "True") == "False") == False

from datetime import datetime
current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = f"You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: [ {Current_Date} ]"

from chatgpt2api.chatgpt2api import Chatbot as GPT
if API:
    ChatGPTbot = GPT(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
    Claude2bot = GPT(api_key=f"{API}", engine="claude-2-web")
else:
    ChatGPTbot = None

whitelist = os.environ.get('whitelist', None)
if whitelist:
    whitelist = [int(id) for id in whitelist.split(",")]

USE_G4F = False