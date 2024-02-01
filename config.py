import os
from dotenv import load_dotenv
load_dotenv()
import utils.prompt as prompt

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
GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4-0125-preview')
# DEFAULT_SEARCH_MODEL = os.environ.get('DEFAULT_SEARCH_MODEL', 'gpt-3.5-turbo-1106') gpt-3.5-turbo-16k
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
# PDF_EMBEDDING = (os.environ.get('PDF_EMBEDDING', "True") == "False") == False
LANGUAGE = os.environ.get('LANGUAGE', 'Simplified Chinese')


from datetime import datetime
current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))

from utils.chatgpt2api import Chatbot as GPT
from utils.chatgpt2api import Imagebot, claudebot
if API:
    try:
        ChatGPTbot = GPT(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
    except:
        ChatGPTbot = GPT(api_key=f"{API}", engine="gpt-3.5-turbo-1106", system_prompt=systemprompt, temperature=temperature)

    try:
        GPT4visionbot = GPT(api_key=f"{API}", engine="gpt-4-vision-preview", system_prompt=systemprompt, temperature=temperature)
    except:
        print("无法使用 gpt-4-vision-preview 模型")
    translate_bot = GPT(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
    copilot_bot = GPT(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=prompt.search_system_prompt.format(LANGUAGE), temperature=temperature)
    dallbot = Imagebot(api_key=f"{API}")
else:
    ChatGPTbot = None

ClaudeAPI = os.environ.get('claude_api_key', None)
if ClaudeAPI:
    claudeBot = claudebot(api_key=f"{ClaudeAPI}")

whitelist = os.environ.get('whitelist', None)
if whitelist:
    whitelist = [int(id) for id in whitelist.split(",")]
ADMIN_LIST = os.environ.get('ADMIN_LIST', None)
if ADMIN_LIST:
    ADMIN_LIST = [int(id) for id in ADMIN_LIST.split(",")]
GROUP_LIST = os.environ.get('GROUP_LIST', None)
if GROUP_LIST:
    GROUP_LIST = [int(id) for id in GROUP_LIST.split(",")]

PLUGINS = {
    "SEARCH_USE_GPT": (os.environ.get('SEARCH_USE_GPT', "True") == "False") == False,
    # "USE_G4F": (os.environ.get('USE_G4F', "False") == "False") == False,
    "DATE": True,
    "URL": True,
    "VERSION": True,
}

class openaiAPI:
    def __init__(
        self,
        api_url: str = (os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions"),
    ):
        from urllib.parse import urlparse, urlunparse
        self.source_api_url: str = api_url
        parsed_url = urlparse(self.source_api_url)
        self.base_url: str = urlunparse(parsed_url[:2] + ("",) * 4)
        self.v1_url: str = urlunparse(parsed_url[:2] + ("/v1",) + ("",) * 3)
        self.chat_url: str = urlunparse(parsed_url[:2] + ("/v1/chat/completions",) + ("",) * 3)
        self.image_url: str = urlunparse(parsed_url[:2] + ("/v1/images/generations",) + ("",) * 3)

bot_api_url = openaiAPI()