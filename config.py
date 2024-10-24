import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

from utils.i18n import strings
from datetime import datetime
from ModelMerge.src.ModelMerge.utils import prompt
from ModelMerge.src.ModelMerge.models import chatgpt, groq, claude3, gemini, vertex, PLUGINS, whisper, DuckChat
from ModelMerge.src.ModelMerge.models.base import BaseAPI

from telegram import InlineKeyboardButton

NICK = os.environ.get('NICK', None)
PORT = int(os.environ.get('PORT', '8080'))
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)

GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-4o')
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
API = os.environ.get('API', None)
WEB_HOOK = os.environ.get('WEB_HOOK', None)
CHAT_MODE = os.environ.get('CHAT_MODE', "global")
GET_MODELS = (os.environ.get('GET_MODELS', "False") == "False") == False

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', None)

VERTEX_PRIVATE_KEY = os.environ.get('VERTEX_PRIVATE_KEY', None)
VERTEX_CLIENT_EMAIL = os.environ.get('VERTEX_CLIENT_EMAIL', None)
VERTEX_PROJECT_ID = os.environ.get('VERTEX_PROJECT_ID', None)

PASS_HISTORY = os.environ.get('PASS_HISTORY', 9999)
if type(PASS_HISTORY) == str:
    if PASS_HISTORY.isdigit():
        PASS_HISTORY = int(PASS_HISTORY)
    elif PASS_HISTORY.lower() == "true":
        PASS_HISTORY = 9999
    elif PASS_HISTORY.lower() == "false":
        PASS_HISTORY = 0
    else:
        PASS_HISTORY = 9999
else:
    PASS_HISTORY = 9999

PREFERENCES = {
    "PASS_HISTORY"      : int(PASS_HISTORY),
    "IMAGEQA"           : (os.environ.get('IMAGEQA', "False") == "True") == False,
    "LONG_TEXT"         : (os.environ.get('LONG_TEXT', "True") == "False") == False,
    "LONG_TEXT_SPLIT"   : (os.environ.get('LONG_TEXT_SPLIT', "True") == "False") == False,
    "FILE_UPLOAD_MESS"  : (os.environ.get('FILE_UPLOAD_MESS', "True") == "False") == False,
    "FOLLOW_UP"         : (os.environ.get('FOLLOW_UP', "False") == "False") == False,
    "TITLE"             : (os.environ.get('TITLE', "False") == "False") == False,
    # "TYPING"            : (os.environ.get('TYPING', "False") == "False") == False,
    "REPLY"             : (os.environ.get('REPLY', "False") == "False") == False,
}

LANGUAGE = os.environ.get('LANGUAGE', 'English')

LANGUAGES = {
    "English": False,
    "Simplified Chinese": False,
    "Traditional Chinese": False,
    "Russian": False,
}

LANGUAGES_TO_CODE = {
    "English": "en",
    "Simplified Chinese": "zh",
    "Traditional Chinese": "zh-hk",
    "Russian": "ru",
}

current_date = datetime.now()
Current_Date = current_date.strftime("%Y-%m-%d")
systemprompt = os.environ.get('SYSTEMPROMPT', prompt.system_prompt.format(LANGUAGE, Current_Date))
claude_systemprompt = os.environ.get('SYSTEMPROMPT', prompt.claude_system_prompt.format(LANGUAGE))


import json
from contextlib import contextmanager

CONFIG_DIR = os.environ.get('CONFIG_DIR', 'user_configs')

import os
from contextlib import contextmanager

@contextmanager
def file_lock(filename):
    if os.name == 'nt':  # Windows系统
        import msvcrt
        with open(filename, 'a+') as f:
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                yield f
            finally:
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass  # 如果解锁失败，我们也不能做太多
    else:  # Unix-like系统
        import fcntl
        with open(filename, 'a+') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                yield f
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

# # 使用示例
# try:
#     with file_lock("myfile.txt") as f:
#         # 在这里进行文件操作
#         f.write("Some data\n")
# except IOError:
#     print("无法获取文件锁，文件可能正被其他进程使用")

def save_user_config(user_id, config):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    filename = os.path.join(CONFIG_DIR, f'{user_id}.json')

    with file_lock(filename):
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

def load_user_config(user_id):
    filename = os.path.join(CONFIG_DIR, f'{user_id}.json')

    if not os.path.exists(filename):
        return {}

    with file_lock(filename):
        with open(filename, 'r') as f:
            content = f.read()
            if not content.strip():
                return {}
            else:
                return json.loads(content)

def update_user_config(user_id, key, value):
    config = load_user_config(user_id)
    config[key] = value
    save_user_config(user_id, config)

class NestedDict:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        if key not in self.data:
            self.data[key] = NestedDict()
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        return str(self.data)

    def keys(self):
        return self.data.keys()

class UserConfig:
    def __init__(self,
        user_id: str = None,
        language="English",
        api_url="https://api.openai.com/v1/chat/completions",
        api_key=None,
        engine="gpt-4o",
        mode="global",
        preferences=None,
        plugins=None,
        languages=None,
        systemprompt=None,
        claude_systemprompt=None
    ):
        self.user_id = user_id
        self.language = language
        self.languages = languages
        self.languages[self.language] = True
        self.api_url = api_url
        self.api_key = api_key
        self.engine = engine
        self.preferences = preferences
        self.plugins = plugins
        self.systemprompt = systemprompt
        self.claude_systemprompt = claude_systemprompt
        self.users = NestedDict()
        self.users["global"] = self.get_init_preferences()
        # self.users = {
        #     "global": self.get_init_preferences()
        # }
        self.users["global"].update(self.preferences)
        self.users["global"].update(self.plugins)
        self.users["global"].update(self.languages)
        self.mode = mode
        self.load_all_configs()
        self.parameter_name_list = list(self.users["global"].keys())
        for key in self.parameter_name_list:
            update_user_config("global", key, self.users["global"][key])


    def load_all_configs(self):
        if not os.path.exists(CONFIG_DIR):
            return

        for filename in os.listdir(CONFIG_DIR):
            if filename.endswith('.json'):
                user_id = filename[:-5]  # 移除 '.json' 后缀
                user_config = load_user_config(user_id)
                self.users[user_id] = NestedDict()
                for key, value in user_config.items():
                    self.users[user_id][key] = value
                    if key == "api_url" and value != self.api_url:
                        self.users[user_id]["api_url"] = self.api_url
                        update_user_config(user_id, "api_url", self.api_url)
                    if key == "api_key" and value != self.api_key:
                        self.users[user_id]["api_key"] = self.api_key
                        update_user_config(user_id, "api_key", self.api_key)
                    if user_id == "global" and key == "systemprompt" and value != self.systemprompt:
                        self.users[user_id]["systemprompt"] = self.systemprompt
                        update_user_config(user_id, "systemprompt", self.systemprompt)

    def get_init_preferences(self):
        return {
            "language": self.language,
            "engine": self.engine,
            "systemprompt": self.systemprompt,
            "claude_systemprompt": self.claude_systemprompt,
            "api_key": self.api_key,
            "api_url": self.api_url,
        }

    def user_init(self, user_id = None):
        if user_id == None or self.mode == "global":
            user_id = "global"
        self.user_id = user_id
        if self.user_id not in self.users.keys():
            self.users[self.user_id] = self.get_init_preferences()
            self.users[self.user_id].update(self.preferences)
            self.users[self.user_id].update(self.plugins)
            self.users[self.user_id].update(self.languages)
            for key in self.users[self.user_id].keys():
                update_user_config(user_id, key, self.users[self.user_id][key])

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
            update_user_config("global", parameter_name, value)
        if self.mode == "multiusers":
            self.user_init(user_id)
            self.users[self.user_id][parameter_name] = value
            update_user_config(self.user_id, parameter_name, value)

    def extract_plugins_config(self, user_id = None):
        self.user_init(user_id)
        if isinstance(self.users[self.user_id], dict):
            user_data = self.users[self.user_id]
        else:
            user_data = self.users[self.user_id].data
        plugins_config = {key: value for key, value in user_data.items() if key in self.plugins}
        return plugins_config

    def to_json(self, user_id=None):
        def nested_dict_to_dict(nd):
            if isinstance(nd, NestedDict):
                return {k: nested_dict_to_dict(v) for k, v in nd.data.items()}
            return nd

        if user_id:
            serializable_config = nested_dict_to_dict(self.users[user_id])
        else:
            serializable_config = nested_dict_to_dict(self.users)

        return json.dumps(serializable_config, ensure_ascii=False, indent=2)

    def __str__(self):
        return str(self.users)

Users = UserConfig(mode=CHAT_MODE, api_key=API, api_url=API_URL, engine=GPT_ENGINE, preferences=PREFERENCES, plugins=PLUGINS, language=LANGUAGE, languages=LANGUAGES, systemprompt=systemprompt, claude_systemprompt=claude_systemprompt)

temperature = float(os.environ.get('temperature', '0.5'))
CLAUDE_API = os.environ.get('claude_api_key', None)

ChatGPTbot, SummaryBot, claude3Bot, groqBot, gemini_Bot, vertexBot, whisperBot, duckBot = None, None, None, None, None, None, None, None
def InitEngine(chat_id=None):
    global Users, ChatGPTbot, SummaryBot, claude3Bot, groqBot, gemini_Bot, vertexBot, whisperBot, duckBot
    api_key = Users.get_config(chat_id, "api_key")
    api_url = Users.get_config(chat_id, "api_url")
    if api_key:
        ChatGPTbot = chatgpt(temperature=temperature, print_log=True)
        SummaryBot = chatgpt(temperature=temperature, use_plugins=False, print_log=True)
        whisperBot = whisper(api_key=api_key, api_url=api_url)
    if CLAUDE_API:
        claude3Bot = claude3(temperature=temperature, print_log=True)
    if GROQ_API_KEY:
        groqBot = groq(temperature=temperature)
    if GOOGLE_AI_API_KEY:
        gemini_Bot = gemini(temperature=temperature, print_log=True)
    if VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID:
        vertexBot = vertex(temperature=temperature, print_log=True)

    duckBot = DuckChat()

def update_language_status(language, chat_id=None):
    global Users
    systemprompt = Users.get_config(chat_id, "systemprompt")
    claude_systemprompt = Users.get_config(chat_id, "claude_systemprompt")
    LAST_LANGUAGE = Users.get_config(chat_id, "language")
    Users.set_config(chat_id, "language", language)
    for lang in LANGUAGES:
        Users.set_config(chat_id, lang, False)

    Users.set_config(chat_id, language, True)
    systemprompt = systemprompt.replace(LAST_LANGUAGE, Users.get_config(chat_id, "language"))
    claude_systemprompt = claude_systemprompt.replace(LAST_LANGUAGE, Users.get_config(chat_id, "language"))
    Users.set_config(chat_id, "systemprompt", systemprompt)
    Users.set_config(chat_id, "claude_systemprompt", claude_systemprompt)

InitEngine(chat_id=None)
update_language_status(LANGUAGE)

def get_local_version_info():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(['git', '-C', current_directory, 'log', '-1'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    return output.split('\n')[0].split(' ')[1]  # 获取本地最新提交的哈希值

def get_remote_version_info():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(['git', '-C', current_directory, 'ls-remote', 'origin', 'HEAD'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    return output.split('\t')[0]  # 获取远程最新提交的哈希值

def check_for_updates():
    local_version = get_local_version_info()
    remote_version = get_remote_version_info()

    if local_version == remote_version:
        return "Up to date."
    else:
        return "A new version is available! Please redeploy."

def replace_with_asterisk(string, start=10, end=45):
    if string:
        return string[:start] + '*' * (end - start - 8) + string[end:]
    else:
        return None

def update_info_message(user_id = None):
    api_key = Users.get_config(user_id, "api_key")
    api_url = Users.get_config(user_id, "api_url")
    return "".join([
        f"**🤖 Model:** `{Users.get_config(user_id, 'engine')}`\n\n",
        f"**🔑 API:** `{replace_with_asterisk(api_key)}`\n\n" if api_key else "",
        f"**🔗 API URL:** `{api_url}`\n\n" if api_url else "",
        f"**🛜 WEB HOOK:** `{WEB_HOOK}`\n\n" if WEB_HOOK else "",
        f"**🚰 Tokens usage:** `{get_robot(user_id)[0].tokens_usage[str(user_id)]}`\n\n" if get_robot(user_id)[0] else "",
        f"**🃏 NICK:** `{NICK}`\n\n" if NICK else "",
        f"**📖 Version:** `{check_for_updates()}`\n\n",
    ])

def reset_ENGINE(chat_id, message=None):
    global ChatGPTbot, claude3Bot, groqBot, gemini_Bot, vertexBot
    api_key = Users.get_config(chat_id, "api_key")
    api_url = Users.get_config(chat_id, "api_url")
    engine = Users.get_config(chat_id, "engine")
    if message:
        if "claude" in engine:
            Users.set_config(chat_id, "claude_systemprompt", message)
        else:
            Users.set_config(chat_id, "systemprompt", message)
    systemprompt = Users.get_config(chat_id, "systemprompt")
    claude_systemprompt = Users.get_config(chat_id, "claude_systemprompt")
    if api_key and ChatGPTbot:
        if "claude" in engine:
            ChatGPTbot.reset(convo_id=str(chat_id), system_prompt=claude_systemprompt)
        else:
            ChatGPTbot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if CLAUDE_API and claude3Bot:
        claude3Bot.reset(convo_id=str(chat_id), system_prompt=claude_systemprompt)
    if GROQ_API_KEY and groqBot:
        groqBot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if GOOGLE_AI_API_KEY and gemini_Bot:
        gemini_Bot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID and vertexBot:
        vertexBot.reset(convo_id=str(chat_id), system_prompt=systemprompt)

def get_robot(chat_id = None):
    global ChatGPTbot, claude3Bot, groqBot, gemini_Bot, duckBot
    engine = Users.get_config(chat_id, "engine")
    role = "user"
    if CLAUDE_API and "claude-3" in engine:
        robot = claude3Bot
        api_key = CLAUDE_API
        api_url = "https://api.anthropic.com/v1/messages"
    elif ("mixtral" in engine or "llama" in engine) and GROQ_API_KEY:
        robot = groqBot
        api_key = GROQ_API_KEY
        api_url = "https://api.groq.com/openai/v1/chat/completions"
    elif GOOGLE_AI_API_KEY and "gemini" in engine:
        robot = gemini_Bot
        api_key = GOOGLE_AI_API_KEY
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/{model}:{stream}?key={api_key}"
    elif VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID and "gemini" in engine:
        robot = vertexBot
        api_key = VERTEX_PRIVATE_KEY
        api_url = "https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/{MODEL_ID}:{stream}"
    elif ChatGPTbot:
        robot = ChatGPTbot
        api_key = Users.get_config(chat_id, "api_key")
        api_url = Users.get_config(chat_id, "api_url")
        api_url = BaseAPI(api_url=api_url).chat_url
    else:
        robot = duckBot
        api_key = "duckduckgo"
        api_url = None

    return robot, role, api_key, api_url

whitelist = os.environ.get('whitelist', None)
if whitelist == "":
    whitelist = None
if whitelist:
    whitelist = [id for id in whitelist.split(",")]

BLACK_LIST = os.environ.get('BLACK_LIST', None)
if BLACK_LIST == "":
    BLACK_LIST = None
if BLACK_LIST:
    BLACK_LIST = [id for id in BLACK_LIST.split(",")]

ADMIN_LIST = os.environ.get('ADMIN_LIST', None)
if ADMIN_LIST == "":
    ADMIN_LIST = None
if ADMIN_LIST:
    ADMIN_LIST = [id for id in ADMIN_LIST.split(",")]
GROUP_LIST = os.environ.get('GROUP_LIST', None)
if GROUP_LIST == "":
    GROUP_LIST = None
if GROUP_LIST:
    GROUP_LIST = [id for id in GROUP_LIST.split(",")]

def delete_model_digit_tail(lst):
    if len(lst) == 2:
        return "-".join(lst)
    for i in range(len(lst) - 1, -1, -1):
        if not lst[i].isdigit():
            if i == len(lst) - 1:
                return "-".join(lst)
            else:
                return "-".join(lst[:i + 1])

def get_status(chatid = None, item = None):
    if item == "PASS_HISTORY":
        return "✅ " if int(Users.get_config(chatid, item)) > 2 else "☑️ "
    return "✅ " if Users.get_config(chatid, item) else "☑️ "

def create_buttons(strings, plugins_status=False, lang="English", button_text=None, Suffix="", chatid=None):
    if plugins_status:
        strings_array = {kv:kv for kv in strings}
    else:
        # 过滤出长度小于15的字符串
        abbreviation_strings = [delete_model_digit_tail(s.split("-")) for s in strings]
        from collections import Counter
        counter = Counter(abbreviation_strings)
        filtered_counter = {key: count for key, count in counter.items() if count > 1}
        # print(filtered_counter)

        strings_array = {}
        for s in strings:
            if delete_model_digit_tail(s.split("-")) in filtered_counter:
                strings_array[s] = s
            else:
                strings_array[delete_model_digit_tail(s.split('-'))] = s

    filtered_strings1 = {k:v for k, v in strings_array.items() if len(k) <= 14}
    # print(filtered_strings1)
    filtered_strings2 = {k:v for k, v in strings_array.items() if len(k) > 14}
    # print(filtered_strings2)

    buttons = []
    temp = []

    for k, v in filtered_strings1.items():
        if plugins_status:
            button = InlineKeyboardButton(f"{get_status(chatid, k)}{button_text[k][lang]}", callback_data=k + Suffix)
        else:
            button = InlineKeyboardButton(k, callback_data=v + Suffix)
        temp.append(button)

        # 每两个按钮一组
        if len(temp) == 2:
            buttons.append(temp)
            temp = []

    # 如果最后一组不足两个，也添加进去
    if temp:
        buttons.append(temp)

    for k, v in filtered_strings2.items():
        if plugins_status:
            button = InlineKeyboardButton(f"{get_status(chatid, k)}{button_text[k][lang]}", callback_data=k + Suffix)
        else:
            button = InlineKeyboardButton(k, callback_data=v + Suffix)
        buttons.append([button])

    return buttons

initial_model = [
    "gpt-4o",
    "gpt-4o-mini",
    "o1-mini",
    "o1-preview",
    "claude-3-opus-20240229",
    "claude-3-5-sonnet-20240620",
    # "gpt-4-turbo-2024-04-09",
    # "gpt-3.5-turbo",
    # "claude-3-haiku-20240307",
]

if GROQ_API_KEY:
    initial_model.extend([
        "llama-3.1-70b-versatile",
        "llama-3.1-405b-reasoning",
    ])
if GOOGLE_AI_API_KEY or (VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID):
    initial_model.extend([
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ])

if duckBot:
    initial_model.extend([
        "claude-3-haiku",
        "Meta-Llama-3.1-70B",
        "Mixtral-8x7B",
    ])

def update_initial_model():
    global initial_model
    try:
        endpoint = BaseAPI(api_url=API_URL)
        endpoint_models_url = endpoint.v1_models
        import requests
        response = requests.get(
            endpoint_models_url,
            headers={"Authorization": f"Bearer {API}"},
        )
        models = response.json()
        # print(models)
        models_list = models["data"]
        models_id = [model["id"] for model in models_list]
        set_models = set()
        for model_item in models_id:
            if "dalle" in model_item or "dall-e" in model_item:
                continue
            if "whisper" in model_item:
                continue
            if "moderation" in model_item:
                continue
            set_models.add(model_item)
            # parts = [part for segment in model_item.split("-") for part in segment.split("@")]
            # set_models.add(delete_model_digit_tail(parts))
        models_id = list(set_models)
        # print(models_id)
        initial_model = models_id
    except Exception as e:
        print("error:", e)
        pass

if GET_MODELS:
    update_initial_model()

CUSTOM_MODELS = os.environ.get('CUSTOM_MODELS', None)
if CUSTOM_MODELS:
    CUSTOM_MODELS_LIST = [id for id in CUSTOM_MODELS.split(",")]
    # print("CUSTOM_MODELS_LIST", CUSTOM_MODELS_LIST)
else:
    CUSTOM_MODELS_LIST = None
if CUSTOM_MODELS_LIST:
    delete_models = [model[1:] for model in CUSTOM_MODELS_LIST if model[0] == "-"]
    for target in delete_models:
        if target == "all":
            initial_model = []
            break
        for model in initial_model:
            if target in model:
                initial_model.remove(model)

    initial_model.extend([model for model in CUSTOM_MODELS_LIST if model not in initial_model and model[0] != "-"])

def get_current_lang(chatid=None):
    current_lang = Users.get_config(chatid, "language")
    return LANGUAGES_TO_CODE[current_lang]

def update_models_buttons(chatid=None):
    lang = get_current_lang(chatid)
    buttons = create_buttons(initial_model, Suffix="_MODELS")
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data="BACK"),
        ],
    )
    return buttons

def update_first_buttons_message(chatid=None):
    lang = get_current_lang(chatid)
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

def update_menu_buttons(setting, _strings, chatid):
    lang = get_current_lang(chatid)
    setting_list = list(setting.keys())
    buttons = create_buttons(setting_list, plugins_status=True, lang=lang, button_text=strings, chatid=chatid, Suffix=_strings)
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data="BACK"),
        ],
    )
    return buttons