import os
from dotenv import load_dotenv
load_dotenv()

from utils.i18n import strings
from datetime import datetime
from ModelMerge.utils import prompt
from ModelMerge.models import chatgpt, claude, groq, claude3, gemini, dalle3
from ModelMerge.models.config import PLUGINS
from telegram import InlineKeyboardButton

NICK = os.environ.get('NICK', None)
PORT = int(os.environ.get('PORT', '8080'))
WEB_HOOK = os.environ.get('WEB_HOOK', None)
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)

API = os.environ.get('API', None)
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4o')
PASS_HISTORY = (os.environ.get('PASS_HISTORY', "True") == "False") == False

USE_GOOGLE = (os.environ.get('USE_GOOGLE', "True") == "False") == False
if os.environ.get('GOOGLE_API_KEY', None) == None and os.environ.get('GOOGLE_CSE_ID', None) == None:
    USE_GOOGLE = False

temperature = float(os.environ.get('temperature', '0.5'))
LANGUAGE = os.environ.get('LANGUAGE', 'English')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', None)
CUSTOM_MODELS = os.environ.get('CUSTOM_MODELS', None)
if CUSTOM_MODELS:
    CUSTOM_MODELS_LIST = [id for id in CUSTOM_MODELS.split(",")]
else:
    CUSTOM_MODELS_LIST = None

current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))
claude_systemprompt = os.environ.get('SYSTEMPROMPT', prompt.claude_system_prompt.format(LANGUAGE))

if API:
    ChatGPTbot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)

    translate_bot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
    copilot_bot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=prompt.search_system_prompt.format(LANGUAGE), temperature=temperature)
    dallbot = dalle3(api_key=f"{API}")
else:
    ChatGPTbot = None

ClaudeAPI = os.environ.get('claude_api_key', None)
if ClaudeAPI:
    claudeBot = claude(api_key=f"{ClaudeAPI}", system_prompt=claude_systemprompt)
    claude3Bot = claude3(api_key=f"{ClaudeAPI}", system_prompt=claude_systemprompt)

if GROQ_API_KEY:
    groqBot = groq(api_key=f"{GROQ_API_KEY}")
if GOOGLE_AI_API_KEY:
    gemini_Bot = gemini(api_key=f"{GOOGLE_AI_API_KEY}")

whitelist = os.environ.get('whitelist', None)
if whitelist:
    whitelist = [int(id) for id in whitelist.split(",")]
ADMIN_LIST = os.environ.get('ADMIN_LIST', None)
if ADMIN_LIST:
    ADMIN_LIST = [int(id) for id in ADMIN_LIST.split(",")]
GROUP_LIST = os.environ.get('GROUP_LIST', None)
if GROUP_LIST:
    GROUP_LIST = [int(id) for id in GROUP_LIST.split(",")]

class userConfig:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.language = LANGUAGE
        self.temperature = temperature
        self.engine = GPT_ENGINE
        self.system_prompt = systemprompt
        self.search_system_prompt = prompt.search_system_prompt.format(self.language)
        self.search_model = "gpt-3.5-turbo-1106"

def get_plugins_status(item):
    return "✅" if PLUGINS[item] else "☑️"

def delete_model_digit_tail(lst):
    for i in range(len(lst) - 1, -1, -1):
        if not lst[i].isdigit():
            if i == len(lst) - 1:
                return "-".join(lst)
            else:
                return "-".join(lst[:i + 1])

def create_buttons(strings):
    # 过滤出长度小于15的字符串
    filtered_strings1 = [s for s in strings if len(delete_model_digit_tail(s.split("-"))) <= 14]
    filtered_strings2 = [s for s in strings if len(delete_model_digit_tail(s.split("-"))) > 14]

    buttons = []
    temp = []

    for string in filtered_strings1:
        button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string)
        temp.append(button)

        # 每两个按钮一组
        if len(temp) == 2:
            buttons.append(temp)
            temp = []

    # 如果最后一组不足两个，也添加进去
    if temp:
        buttons.append(temp)

    for string in filtered_strings2:
        button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string)
        buttons.append([button])

    return buttons

initial_model = [
    "gpt-4o",
    "gpt-4-turbo-2024-04-09",
    "gpt-3.5-turbo",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]

if GROQ_API_KEY:
    initial_model.extend([
        "mixtral-8x7b-32768",
        "llama3-70b-8192",
    ])
if GOOGLE_AI_API_KEY:
    initial_model.extend([
        "gemini-1.5-pro-latest",
    ])

if CUSTOM_MODELS_LIST:
    delete_models = [model[1:] for model in CUSTOM_MODELS_LIST if model[0] == "-"]
    for target in delete_models:
        for model in initial_model:
            if target in model:
                initial_model.remove(model)

    initial_model.extend([model for model in CUSTOM_MODELS_LIST if model not in initial_model and model[0] != "-"])

def update_model_buttons():
    buttons = create_buttons(initial_model)
    if LANGUAGE == "Simplified Chinese":
        lang = "zh"
    else:
        lang = "en"
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data="BACK"),
        ],
    )
    return buttons

def get_current_lang():
    if LANGUAGE == "Simplified Chinese":
        lang = "zh"
    else:
        lang = "en"
    return lang

def update_first_buttons_message():
    history = "✅" if PASS_HISTORY else "☑️"

    if LANGUAGE == "Simplified Chinese":
        lang = "zh"
    else:
        lang = "en"


    first_buttons = [
        [
            InlineKeyboardButton(strings["button_change_model"][lang], callback_data="MODEL"),
            InlineKeyboardButton(strings['button_language'][lang], callback_data="language"),
            InlineKeyboardButton(f"{strings['button_history'][lang]} {history}", callback_data="PASS_HISTORY"),
        ],
        [
            InlineKeyboardButton(f"{strings['button_search'][lang]} {get_plugins_status('SEARCH')}", callback_data='SEARCH'),
            InlineKeyboardButton(f"{strings['button_current_time'][lang]} {get_plugins_status('DATE')}", callback_data='DATE'),
        ],
        [
            InlineKeyboardButton(f"{strings['button_url'][lang]} {get_plugins_status('URL')}", callback_data='URL'),
            InlineKeyboardButton(f"{strings['button_version'][lang]} {get_plugins_status('VERSION')}", callback_data='VERSION'),
        ],
    ]
    return first_buttons