import os
from dotenv import load_dotenv
load_dotenv()

from utils.i18n import strings
from datetime import datetime
from ModelMerge.utils import prompt
from ModelMerge.utils.scripts import get_encode_image
from ModelMerge.models import chatgpt, claude, groq, claude3, gemini
from telegram import InlineKeyboardButton

NICK = os.environ.get('NICK', None)
PORT = int(os.environ.get('PORT', '8080'))
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)

def replace_with_asterisk(string, start=10, end=45):
    return string[:start] + '*' * (end - start - 8) + string[end:]

GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4o')
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
API = os.environ.get('API', None)
WEB_HOOK = os.environ.get('WEB_HOOK', None)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', None)

current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")

PREFERENCES = {
    "PASS_HISTORY": (os.environ.get('PASS_HISTORY', "True") == "False") == False,
    "LONG_TEXT"   : (os.environ.get('LONG_TEXT', "True") == "False") == False,
    "FOLLOW_UP"   : (os.environ.get('FOLLOW_UP', "False") == "False") == False,
    "TITLE"       : (os.environ.get('TITLE', "False") == "False") == False,
}

LANGUAGE = os.environ.get('LANGUAGE', 'English')

LANGUAGES = {
    "English": False,
    "Simplified Chinese": False,
    "Traditional Chinese": False,
}

LANGUAGES_TO_CODE = {
    "English": "en",
    "Simplified Chinese": "zh",
    "Traditional Chinese": "zh-hk",
}
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))
claude_systemprompt = os.environ.get('SYSTEMPROMPT', prompt.claude_system_prompt.format(LANGUAGE))

class UserConfig:
    def __init__(self, user_id: str = None, language="English", engine="gpt-4o", mode="global"):
        self.user_id = user_id
        self.language = language
        self.engine = engine
        self.users = {
            "global": {
                "language": self.language,
                "engine": self.engine,
            }
        }
        self.mode = mode
        self.parameter_name_list = list(self.users["global"].keys())
    def user_init(self, user_id = None):
        if user_id == None:
            user_id = "global"
        self.user_id = user_id
        if self.user_id not in self.users.keys():
            self.users[self.user_id] = {"language": LANGUAGE, "engine": self.engine}

    def get_config(self, user_id = None, parameter_name = None):
        if parameter_name not in self.parameter_name_list:
            raise ValueError("parameter_name is not in the parameter_name_list")
        if self.mode == "global":
            return self.users["global"][parameter_name]
        if self.mode == "multiusers":
            self.user_init(user_id)
            return self.users[self.user_id][parameter_name]

    def set_config(self, user_id = None, parameter_name = None, value = None):
        if parameter_name not in self.parameter_name_list:
            raise ValueError("parameter_name is not in the parameter_name_list")
        if self.mode == "global":
            self.users["global"][parameter_name] = value
        if self.mode == "multiusers":
            self.user_init(user_id)
            self.users[self.user_id][parameter_name] = value

CHAT_MODE = os.environ.get('CHAT_MODE', "global")
if GPT_ENGINE != "gpt-4o":
    Users = UserConfig(mode=CHAT_MODE, engine=GPT_ENGINE)
else:
    Users = UserConfig(mode=CHAT_MODE)

def get_ENGINE(user_id = None):
    return Users.get_config(user_id, "engine")

temperature = float(os.environ.get('temperature', '0.5'))
CLAUDE_API = os.environ.get('claude_api_key', None)

ChatGPTbot, SummaryBot, translate_bot, claudeBot, claude3Bot, groqBot, gemini_Bot = None, None, None, None, None, None, None
def update_ENGINE(data = None, chat_id=None):
    global Users, ChatGPTbot, SummaryBot, translate_bot, claudeBot, claude3Bot, groqBot, gemini_Bot
    if data:
        Users.set_config(chat_id, "engine", data)
    engine = Users.get_config(chat_id, "engine")
    if API:
        ChatGPTbot = chatgpt(api_key=f"{API}", engine=engine, system_prompt=systemprompt, temperature=temperature)
        SummaryBot = chatgpt(api_key=f"{API}", engine="gpt-3.5-turbo", system_prompt=systemprompt, temperature=temperature)
        translate_bot = chatgpt(api_key=f"{API}", engine=engine, system_prompt=systemprompt, temperature=temperature)
    if CLAUDE_API and "claude-2.1" in engine:
        claudeBot = claude(api_key=f"{CLAUDE_API}", engine=engine, system_prompt=claude_systemprompt, temperature=temperature)
    if CLAUDE_API and "claude-3" in engine:
        claude3Bot = claude3(api_key=f"{CLAUDE_API}", engine=engine, system_prompt=claude_systemprompt, temperature=temperature)
    if GROQ_API_KEY and ("mixtral" in engine or "llama" in engine):
        groqBot = groq(api_key=f"{GROQ_API_KEY}", engine=engine, system_prompt=systemprompt, temperature=temperature)
    if GOOGLE_AI_API_KEY and "gemini" in engine:
        gemini_Bot = gemini(api_key=f"{GOOGLE_AI_API_KEY}", engine=engine, system_prompt=systemprompt, temperature=temperature)

def update_language_status(language, chat_id=None):
    global LANGUAGES, LANGUAGE, systemprompt, claude_systemprompt
    LAST_LANGUAGE = LANGUAGE
    LANGUAGE = language
    for lang in LANGUAGES:
        LANGUAGES[lang] = False

    LANGUAGES[language] = True
    try:
        systemprompt = systemprompt.replace(LAST_LANGUAGE, LANGUAGE)
        claude_systemprompt = claude_systemprompt.replace(LAST_LANGUAGE, LANGUAGE)
    except Exception as e:
        print("error:", e)
        pass
    update_ENGINE()
    # Users.set_config(chat_id, "language", language)

update_language_status(LANGUAGE)



def update_info_message(user_id = None):
    return (
        f"**Model:** `{get_ENGINE(user_id)}`\n\n"
        f"**API_URL:** `{API_URL}`\n\n"
        f"**API:** `{replace_with_asterisk(API)}`\n\n"
        f"**WEB_HOOK:** `{WEB_HOOK}`\n\n"
        f"**tokens usage:** `{get_robot(user_id)[0].tokens_usage[str(user_id)]}`\n\n"
    )

def reset_ENGINE(chat_id, message=None):
    global ChatGPTbot, translate_bot, claudeBot, claude3Bot, groqBot, gemini_Bot, systemprompt, claude_systemprompt
    if message:
        systemprompt = message
        claude_systemprompt = message
    if API and ChatGPTbot:
        ChatGPTbot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if CLAUDE_API and claudeBot:
        claudeBot.reset(convo_id=str(chat_id), system_prompt=claude_systemprompt)
    if CLAUDE_API and claude3Bot:
        claude3Bot.reset(convo_id=str(chat_id), system_prompt=claude_systemprompt)
    if GROQ_API_KEY and groqBot:
        groqBot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if GOOGLE_AI_API_KEY and gemini_Bot:
        gemini_Bot.reset(convo_id=str(chat_id), system_prompt=systemprompt)

def get_robot(chat_id = None):
    global ChatGPTbot, claudeBot, claude3Bot, groqBot, gemini_Bot
    engine = Users.get_config(chat_id, "engine")
    if CLAUDE_API and "claude-2.1" in engine:
        robot = claudeBot
        role = "Human"
    elif CLAUDE_API and "claude-3" in engine:
        robot = claude3Bot
        role = "user"
    elif ("mixtral" in engine or "llama" in engine) and GROQ_API_KEY:
        robot = groqBot
    elif GOOGLE_AI_API_KEY and "gemini" in engine:
        robot = gemini_Bot
        role = "user"
    else:
        robot = ChatGPTbot
        role = "user"

    return robot, role

def get_image_message(image_url, message, chatid = None):
    engine = get_ENGINE(chatid)
    if image_url:
        base64_image = get_encode_image(image_url)
        if "gpt-4" in engine or (CLAUDE_API is None and "claude-3" in engine):
            message.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": base64_image
                    }
                }
            )
        if CLAUDE_API and "claude-3" in engine:
            message.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image.split(",")[1],
                    }
                }
            )
    return message

whitelist = os.environ.get('whitelist', None)
if whitelist:
    whitelist = [int(id) for id in whitelist.split(",")]
ADMIN_LIST = os.environ.get('ADMIN_LIST', None)
if ADMIN_LIST:
    ADMIN_LIST = [int(id) for id in ADMIN_LIST.split(",")]
GROUP_LIST = os.environ.get('GROUP_LIST', None)
if GROUP_LIST:
    GROUP_LIST = [int(id) for id in GROUP_LIST.split(",")]

def delete_model_digit_tail(lst):
    for i in range(len(lst) - 1, -1, -1):
        if not lst[i].isdigit():
            if i == len(lst) - 1:
                return "-".join(lst)
            else:
                return "-".join(lst[:i + 1])

def get_status(setting, item):
    return "✅ " if setting[item] else "☑️ "

def create_buttons(strings, plugins_status=False, lang="English", button_text=None, Suffix="", setting=""):
    # 过滤出长度小于15的字符串
    filtered_strings1 = [s for s in strings if len(delete_model_digit_tail(s.split("-"))) <= 14]
    filtered_strings2 = [s for s in strings if len(delete_model_digit_tail(s.split("-"))) > 14]

    buttons = []
    temp = []

    for string in filtered_strings1:
        if plugins_status:
            button = InlineKeyboardButton(f"{get_status(setting, string)}{button_text[string][lang]}", callback_data=string + Suffix)
        else:
            button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string + Suffix)
        temp.append(button)

        # 每两个按钮一组
        if len(temp) == 2:
            buttons.append(temp)
            temp = []

    # 如果最后一组不足两个，也添加进去
    if temp:
        buttons.append(temp)

    for string in filtered_strings2:
        if plugins_status:
            button = InlineKeyboardButton(f"{get_status(setting, string)}{button_text[string][lang]}", callback_data=string + Suffix)
        else:
            button = InlineKeyboardButton(delete_model_digit_tail(string.split("-")), callback_data=string + Suffix)
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

def get_current_lang():
    for lang, is_active in LANGUAGES.items():
        if is_active:
            return LANGUAGES_TO_CODE[lang]

def update_models_buttons():
    lang = get_current_lang()
    buttons = create_buttons(initial_model, Suffix="_MODELS")
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data="BACK"),
        ],
    )
    return buttons

def update_first_buttons_message():
    lang = get_current_lang()
    first_buttons = [
        [
            InlineKeyboardButton(strings["button_change_model"][lang], callback_data="MODELS"),
            InlineKeyboardButton(strings['button_preferences'][lang], callback_data="PREFERENCES"),
        ],
        [
            InlineKeyboardButton(strings['button_language'][lang], callback_data="LANGUAGE"),
            InlineKeyboardButton(strings['button_plugins'][lang], callback_data="PLUGINS"),
        ],
    ]
    return first_buttons

def update_menu_buttons(setting, _strings):
    lang = get_current_lang()
    setting_list = list(setting.keys())
    buttons = create_buttons(setting_list, plugins_status=True, lang=lang, button_text=strings, setting=setting, Suffix=_strings)
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data="BACK"),
        ],
    )
    return buttons