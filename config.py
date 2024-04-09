import os
from dotenv import load_dotenv
load_dotenv()
import utils.prompt as prompt
from telegram import InlineKeyboardButton

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
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
CUSTOM_MODELS = os.environ.get('CUSTOM_MODELS', None)
if CUSTOM_MODELS:
    CUSTOM_MODELS_LIST = [id for id in CUSTOM_MODELS.split(",")]
else:
    CUSTOM_MODELS_LIST = None


from datetime import datetime
current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))

from utils.chatgpt2api import Chatbot as GPT
from utils.chatgpt2api import Imagebot, claudebot, groqbot, claude3bot
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
    claude3Bot = claude3bot(api_key=f"{ClaudeAPI}")

if GROQ_API_KEY:
    groqBot = groqbot(api_key=f"{GROQ_API_KEY}")

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

class userConfig:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.language = LANGUAGE
        self.temperature = temperature
        self.engine = GPT_ENGINE
        self.system_prompt = systemprompt
        self.search_system_prompt = prompt.search_system_prompt.format(self.language)
        self.search_model = "gpt-3.5-turbo-1106"

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

def get_plugins_status(item):
    return "✅" if PLUGINS[item] else "☑️"

buttons = [
    [
        InlineKeyboardButton("mixtral-8x7b", callback_data="mixtral-8x7b-32768"),
        InlineKeyboardButton("llama2-70b", callback_data="llama2-70b-4096"),
    ],
    [
        InlineKeyboardButton("claude-3-opus", callback_data="claude-3-opus-20240229"),
        InlineKeyboardButton("claude-3-sonnet", callback_data="claude-3-sonnet-20240229"),
    ],
    [
        InlineKeyboardButton("claude-3-haiku", callback_data="claude-3-haiku-20240307"),
        # InlineKeyboardButton("claude-2.1", callback_data="claude-2.1"),
    ],
    [
        InlineKeyboardButton("gpt-4-0125-preview", callback_data="gpt-4-0125-preview"),
    ],
    [
        InlineKeyboardButton("gpt-4-vision-preview", callback_data="gpt-4-vision-preview"),
    ],
    [
        InlineKeyboardButton("gpt-3.5-turbo", callback_data="gpt-3.5-turbo"),
        # InlineKeyboardButton("gpt-3.5-turbo-16k", callback_data="gpt-3.5-turbo-16k"),
    ],
    # [
    #     # InlineKeyboardButton("gpt-4", callback_data="gpt-4"),
    #     InlineKeyboardButton("gpt-4-32k", callback_data="gpt-4-32k"),
    # ],
    # [
    #     InlineKeyboardButton("gpt-3.5-turbo-1106", callback_data="gpt-3.5-turbo-1106"),
    # ],
    # [
    #     InlineKeyboardButton("gpt-4-turbo-preview", callback_data="gpt-4-turbo-preview"),
    # ],
    # [
    #     InlineKeyboardButton("gpt-4-1106-preview", callback_data="gpt-4-1106-preview"),
    # ],
]
if CUSTOM_MODELS_LIST:
    for model in CUSTOM_MODELS_LIST:
        buttons.append(
            [
                InlineKeyboardButton(model, callback_data=model),
            ]
        )
buttons.append(
    [
        InlineKeyboardButton("返回上一级", callback_data="返回上一级"),
    ],
)

def update_first_buttons_message():
    history = "✅" if PASS_HISTORY else "☑️"
    language = "🇨🇳 中文" if LANGUAGE == "Simplified Chinese" else "🇺🇸 English"

    first_buttons = [
        [
            InlineKeyboardButton("更换问答模型", callback_data="更换问答模型"),
            InlineKeyboardButton(language, callback_data="language"),
            InlineKeyboardButton(f"历史记录 {history}", callback_data="PASS_HISTORY"),
        ],
        [
            InlineKeyboardButton(f"搜索 {get_plugins_status('SEARCH_USE_GPT')}", callback_data='SEARCH_USE_GPT'),
            InlineKeyboardButton(f"当前时间 {get_plugins_status('DATE')}", callback_data='DATE'),
        ],
        [
            InlineKeyboardButton(f"URL 总结 {get_plugins_status('URL')}", callback_data='URL'),
            InlineKeyboardButton(f"版本信息 {get_plugins_status('VERSION')}", callback_data='VERSION'),
            # InlineKeyboardButton(f"gpt4free {get_plugins_status('USE_G4F')}", callback_data='USE_G4F'),
        ],
    ]
    return first_buttons