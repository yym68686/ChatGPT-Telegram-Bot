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
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)

def replace_with_asterisk(string, start=10, end=45):
    return string[:start] + '*' * (end - start) + string[end:]

GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4o')
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
API = os.environ.get('API', None)
WEB_HOOK = os.environ.get('WEB_HOOK', None)

def update_info_message():
    return (
        f"**Default engine:** `{GPT_ENGINE}`\n"
        f"**API_URL:** `{API_URL}`\n\n"
        f"**API:** `{replace_with_asterisk(API)}`\n\n"
        f"**WEB_HOOK:** `{WEB_HOOK}`\n\n"
    )

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', None)

current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")

LANGUAGE = os.environ.get('LANGUAGE', 'English')
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))
claude_systemprompt = os.environ.get('SYSTEMPROMPT', prompt.claude_system_prompt.format(LANGUAGE))

def get_current_lang():
    if LANGUAGE == "Simplified Chinese":
        lang = "zh"
    else:
        lang = "en"
    return lang

def update_language():
    global LANGUAGE, systemprompt, claude_systemprompt
    try:
        if LANGUAGE == "Simplified Chinese":
            LANGUAGE = "English"
            systemprompt = systemprompt.replace("Simplified Chinese", "English")
            claude_systemprompt = claude_systemprompt.replace("Simplified Chinese", "English")
        else:
            LANGUAGE = "Simplified Chinese"
            systemprompt = systemprompt.replace("English", "Simplified Chinese")
            claude_systemprompt = claude_systemprompt.replace("English", "Simplified Chinese")
    except:
        pass

temperature = float(os.environ.get('temperature', '0.5'))
CLAUDE_API = os.environ.get('claude_api_key', None)

def update_ENGINE(data = None):
    global GPT_ENGINE, ChatGPTbot, translate_bot, dallbot, claudeBot, claude3Bot, groqBot, gemini_Bot
    if data:
        GPT_ENGINE = data
    if API:
        ChatGPTbot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
        translate_bot = chatgpt(api_key=f"{API}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
        dallbot = dalle3(api_key=f"{API}")
    if CLAUDE_API and "claude-2.1" in GPT_ENGINE:
        claudeBot = claude(api_key=f"{CLAUDE_API}", engine=GPT_ENGINE, system_prompt=claude_systemprompt, temperature=temperature)
    if CLAUDE_API and "claude-3" in GPT_ENGINE:
        claude3Bot = claude3(api_key=f"{CLAUDE_API}", engine=GPT_ENGINE, system_prompt=claude_systemprompt, temperature=temperature)
    if GROQ_API_KEY and ("mixtral" in GPT_ENGINE or "llama" in GPT_ENGINE):
        groqBot = groq(api_key=f"{GROQ_API_KEY}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)
    if GOOGLE_AI_API_KEY and "gemini" in GPT_ENGINE:
        gemini_Bot = gemini(api_key=f"{GOOGLE_AI_API_KEY}", engine=GPT_ENGINE, system_prompt=systemprompt, temperature=temperature)

update_ENGINE()

whitelist = os.environ.get('whitelist', None)
if whitelist:
    whitelist = [int(id) for id in whitelist.split(",")]
ADMIN_LIST = os.environ.get('ADMIN_LIST', None)
if ADMIN_LIST:
    ADMIN_LIST = [int(id) for id in ADMIN_LIST.split(",")]
GROUP_LIST = os.environ.get('GROUP_LIST', None)
if GROUP_LIST:
    GROUP_LIST = [int(id) for id in GROUP_LIST.split(",")]

class UserConfig:
    def __init__(self, user_id: str = "default", language="English", engine="gpt-4o"):
        self.user_id = user_id
        self.language = language
        self.engine = engine
        self.users = {
            "default": {
                "language": self.language,
                "engine": self.engine,
            }
        }
    def user_init(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {"language": LANGUAGE, "engine": GPT_ENGINE}
    def get_language(self, user_id):
        self.user_init(user_id)
        return self.users[user_id]["language"]
    def set_language(self, user_id, language):
        self.user_init(user_id)
        self.users[user_id]["language"] = language

    def get_engine(self, user_id):
        self.user_init(user_id)
        return self.users[user_id]["engine"]
    def set_engine(self, user_id, engine):
        self.user_init(user_id)
        self.users[user_id]["engine"] = engine

Users = UserConfig()

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
        button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string + "ENGINE")
        temp.append(button)

        # 每两个按钮一组
        if len(temp) == 2:
            buttons.append(temp)
            temp = []

    # 如果最后一组不足两个，也添加进去
    if temp:
        buttons.append(temp)

    for string in filtered_strings2:
        button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string + "ENGINE")
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

CUSTOM_MODELS = os.environ.get('CUSTOM_MODELS', None)
if CUSTOM_MODELS:
    CUSTOM_MODELS_LIST = [id for id in CUSTOM_MODELS.split(",")]
else:
    CUSTOM_MODELS_LIST = None
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

def get_plugins_status(item):
    return "✅" if PLUGINS[item] else "☑️"

PASS_HISTORY = (os.environ.get('PASS_HISTORY', "True") == "False") == False
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
            InlineKeyboardButton(f"{history} {strings['button_history'][lang]}", callback_data="PASS_HISTORY"),
        ],
        [
            InlineKeyboardButton(f"{get_plugins_status('SEARCH')}{strings['button_search'][lang]}", callback_data='SEARCH'),
            InlineKeyboardButton(f"{get_plugins_status('DATE')}{strings['button_current_time'][lang]}", callback_data='DATE'),
        ],
        [
            InlineKeyboardButton(f"{get_plugins_status('URL')}{strings['button_url'][lang]}", callback_data='URL'),
            InlineKeyboardButton(f"{get_plugins_status('VERSION')}{strings['button_version'][lang]}", callback_data='VERSION'),
        ],
    ]
    return first_buttons