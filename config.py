import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

import re
from utils.i18n import strings
from datetime import datetime

# We expose variables for access from other modules

from aient.src.aient.utils import prompt
from aient.src.aient.core.utils import update_initial_model, BaseAPI
from aient.src.aient.models import chatgpt, groq, claude3, gemini, vertex, PLUGINS, whisper, DuckChat

from telegram import InlineKeyboardButton

NICK = os.environ.get('NICK', None)
PORT = int(os.environ.get('PORT', '8080'))
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
RESET_TIME = int(os.environ.get('RESET_TIME', '3600'))
if RESET_TIME < 60:
    RESET_TIME = 60

GPT_ENGINE = os.environ.get('GPT_ENGINE', 'gpt-5')
API_URL = os.environ.get('API_URL', 'https://api.openai.com/v1/chat/completions')
GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY', None)

API = os.environ.get('API', None)
WEB_HOOK = os.environ.get('WEB_HOOK', None)
CHAT_MODE = os.environ.get('CHAT_MODE', "global")
GET_MODELS = (os.environ.get('GET_MODELS', "False") == "False") == False

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)

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
        engine="gpt-5",
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

        # 定义旧键名到新键名的映射关系 old_key -> new_key
        key_mapping = {
            "SEARCH": "get_search_results",
            "URL": "get_url_content",
            "ARXIV": "download_read_arxiv_pdf",
            "CODE": "run_python_script",
            "IMAGE": "generate_image",
            "get_date_time_weekday": "get_time"
        }

        for filename in os.listdir(CONFIG_DIR):
            if filename.endswith('.json'):
                user_id = filename[:-5]  # 移除 '.json' 后缀
                user_config = load_user_config(user_id)
                self.users[user_id] = NestedDict()

                # 检查并进行键名映射转换
                updated_config = False
                for old_key, new_key in key_mapping.items():
                    if old_key in user_config:
                        user_config[new_key] = user_config.pop(old_key)
                        updated_config = True

                # 如果配置有更新，保存回文件
                if updated_config:
                    save_user_config(user_id, user_config)

                # 正常处理配置项
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

ChatGPTbot, SummaryBot, groqBot, vertexBot, whisperBot, duckBot = None, None, None, None, None, None
def InitEngine(chat_id=None):
    global Users, ChatGPTbot, SummaryBot, groqBot, vertexBot, whisperBot, duckBot
    api_key = Users.get_config(chat_id, "api_key")
    api_url = Users.get_config(chat_id, "api_url")
    if api_key or GOOGLE_AI_API_KEY or CLAUDE_API:
        ChatGPTbot = chatgpt(temperature=temperature, print_log=True, api_url=api_url, api_key=api_key)
        SummaryBot = chatgpt(temperature=temperature, use_plugins=False, print_log=True, api_url=api_url, api_key=api_key)
        whisperBot = whisper(api_key=api_key, api_url=api_url)
    if GROQ_API_KEY:
        groqBot = groq(temperature=temperature)
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

def replace_with_asterisk(string):
    if string:
        if len(string) <= 4:  # 如果字符串长度小于等于4，则不进行替换
            return string[0] + '*' * 10
        else:
            return string[:10] + '*' * 10 + string[-2:]
    else:
        return None

def update_info_message(user_id = None):
    api_key = Users.get_config(user_id, "api_key")
    api_url = Users.get_config(user_id, "api_url")
    if GOOGLE_AI_API_KEY and os.environ.get('API_URL') == None:
        api_url = "https://generativelanguage.googleapis.com/v1beta"
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
    global ChatGPTbot, groqBot, vertexBot
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
    if GROQ_API_KEY and groqBot:
        groqBot.reset(convo_id=str(chat_id), system_prompt=systemprompt)
    if VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID and vertexBot:
        vertexBot.reset(convo_id=str(chat_id), system_prompt=systemprompt)

def get_robot(chat_id = None):
    global ChatGPTbot, groqBot, duckBot
    engine = Users.get_config(chat_id, "engine")
    role = "user"
    if CLAUDE_API and "claude-3" in engine:
        robot = ChatGPTbot
        api_key = CLAUDE_API
        api_url = "https://api.anthropic.com/v1/messages"
    elif ("mixtral" in engine or "llama" in engine) and GROQ_API_KEY:
        robot = groqBot
        api_key = GROQ_API_KEY
        api_url = "https://api.groq.com/openai/v1/chat/completions"
    elif GOOGLE_AI_API_KEY and ("gemini" in engine or os.environ.get('API_URL') == None):
        robot = ChatGPTbot
        api_key = GOOGLE_AI_API_KEY
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/{model}:{stream}?key={api_key}"
        api_url = api_url.format(model=engine, stream="streamGenerateContent", api_key=api_key)
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

    if not button_text:
        button_text = {k:{lang:k} for k in strings_array.keys()}
    filtered_strings1 = {k:v for k, v in strings_array.items() if k in button_text and len(button_text[k][lang]) <= 14}
    filtered_strings2 = {k:v for k, v in strings_array.items() if k in button_text and len(button_text[k][lang]) > 14}


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
    "gpt-5",
    "gpt-4o",
    "gpt-4o-mini",
    "o4-mini",
    "o3",
    "claude-sonnet-4-20250514",
]

if GROQ_API_KEY:
    initial_model.extend([
        "llama-3.1-70b-versatile",
        "llama-3.1-405b-reasoning",
    ])
if GOOGLE_AI_API_KEY or (VERTEX_PRIVATE_KEY and VERTEX_CLIENT_EMAIL and VERTEX_PROJECT_ID):
    initial_model.extend([
        "gemini-2.5-flash",
        "gemini-2.5-pro",
    ])

if duckBot:
    initial_model.extend([
        "claude-3-haiku",
        "Meta-Llama-3.1-70B",
        "Mixtral-8x7B",
    ])

def remove_no_text_model(model_list):
    set_models = set()
    for model_item in model_list:
        if "dalle" in model_item or "dall-e" in model_item:
            continue
        if "whisper" in model_item:
            continue
        if "moderation" in model_item:
            continue
        if "embedding" in model_item:
            continue
        set_models.add(model_item)
    return list(set_models)

if GET_MODELS:
    robot, role, api_key, api_url = get_robot()
    engine = Users.get_config(None, "engine")
    provider = {
        "provider": "openai",
        "base_url": api_url,
        "api": api_key,
        "model": [engine],
        "tools": True,
        "image": True
    }
    initial_model = remove_no_text_model(update_initial_model(provider))
    if ChatGPTbot:
        robot = ChatGPTbot
        api_key = Users.get_config(None, "api_key")
        api_url = Users.get_config(None, "api_url")
        api_url = BaseAPI(api_url=api_url).chat_url
        provider = {
            "provider": "openai",
            "base_url": api_url,
            "api": api_key,
            "model": [engine],
            "tools": True,
            "image": True
        }
        gpt_initial_model = remove_no_text_model(update_initial_model(provider))
        # print("gpt_initial_model", gpt_initial_model)
        initial_model = list(set(gpt_initial_model + initial_model))

# Structure for storing model groups
MODEL_GROUPS = {}
CUSTOM_MODELS_LIST = []

CUSTOM_MODELS = os.environ.get('CUSTOM_MODELS', None)
if CUSTOM_MODELS:
    # We split the line into parts at the semicolon
    parts = CUSTOM_MODELS.split(';')

    # Temporary storage of models without a group
    ungrouped_models = []

    # We process the first part separately (it may contain flags and models without a group)
    first_part = parts[0].split(',') if parts else []
    for item in first_part:
        item = item.strip()
        if item:
            CUSTOM_MODELS_LIST.append(item)
            # Add to ungrouped list if it's not a flag
            if not item.startswith('-'):
                ungrouped_models.append(item)
            print(f"Added to CUSTOM_MODELS_LIST from first part: {item}")

    # Counter of created groups (except OTHERS)
    group_count = 0

    # We process the remaining parts (groups)
    for i in range(1, len(parts)):
        part = parts[i].strip()
        if not part:
            continue

        # We search for the colon, which separates the group name and the list of models
        colon_pos = part.find(':')
        if colon_pos == -1:
            # If there is no colon, add to ungrouped models
            for model in part.split(','):
                model = model.strip()
                if model:
                    CUSTOM_MODELS_LIST.append(model)
                    ungrouped_models.append(model)
                    print(f"Added to CUSTOM_MODELS_LIST from part {i} without colon: {model}")
            continue

        # We extract the group name and the list of models
        group_name = part[:colon_pos].strip()
        models_part = part[colon_pos+1:].strip()

        # Create debug string for this group
        print(f"Processing group: {group_name} with models: {models_part}")

        # We create a group
        MODEL_GROUPS[group_name] = []
        group_count += 1

        # We add models to the group
        for model in models_part.split(','):
            model = model.strip()
            if model:
                MODEL_GROUPS[group_name].append(model)
                CUSTOM_MODELS_LIST.append(model)
                print(f"Added to group {group_name} and CUSTOM_MODELS_LIST: {model}")

    # Create an OTHERS group only if there are other groups and models without a group
    if group_count > 0 and ungrouped_models:
        MODEL_GROUPS["OTHERS"] = ungrouped_models
        print(f"Created OTHERS group with models: {ungrouped_models}")
    else:
        # Add models without group directly to initial_model
        for model in ungrouped_models:
            if model not in initial_model:
                initial_model.append(model)
                print(f"Added ungrouped model to initial_model: {model}")

# Remove OTHERS group if it's empty
if "OTHERS" in MODEL_GROUPS and not MODEL_GROUPS["OTHERS"]:
    del MODEL_GROUPS["OTHERS"]

# print("Final CUSTOM_MODELS_LIST:", CUSTOM_MODELS_LIST)
# print("Final MODEL_GROUPS:", MODEL_GROUPS)

# We remove duplicates in the list of models
CUSTOM_MODELS_LIST = list(dict.fromkeys(CUSTOM_MODELS_LIST))
# print("After removing duplicates, CUSTOM_MODELS_LIST:", CUSTOM_MODELS_LIST)

# We remove models if there are deletion flags
if CUSTOM_MODELS_LIST:
    delete_models = [model[1:] for model in CUSTOM_MODELS_LIST if model.startswith('-')]
    for target in delete_models:
        if target == "all":
            initial_model = []
            break
        for model in list(initial_model):  # We create a copy of the list for safe deletion
            if target in model:
                initial_model.remove(model)

    # We add only models, not groups and not deletion flags
    for model in CUSTOM_MODELS_LIST:
        if not model.startswith('-') and model not in MODEL_GROUPS.keys() and model not in initial_model:
            initial_model.append(model)
            print(f"Added to initial_model: {model}")

# We output information about groups for debugging
# print("MODEL_GROUPS:", MODEL_GROUPS)
for group, models in MODEL_GROUPS.items():
    print(f"Group {group}: {len(models)} models - {models}")
# print("Final initial_model:", initial_model)

# Function to get all available models (with groups)
def get_all_available_models():
    return initial_model

# Function to get all model groups
def get_model_groups():
    return MODEL_GROUPS

# Function to get models in a specific group
def get_models_in_group(group_name):
    return MODEL_GROUPS.get(group_name, [])

def get_current_lang(chatid=None):
    current_lang = Users.get_config(chatid, "language")
    return LANGUAGES_TO_CODE[current_lang]

def update_models_buttons(chatid=None, group=None):
    lang = get_current_lang(chatid)
    back_button_data = "BACK"  # Default value

    if group and group in MODEL_GROUPS:
        # Showing models in the selected group
        models_in_group = MODEL_GROUPS[group]
        buttons = create_buttons(models_in_group, Suffix="_MODELS")
        back_button_data = "MODELS"  # To return to model groups
    elif MODEL_GROUPS and not group:
        # Showing groups
        groups_list = list(MODEL_GROUPS.keys())

        # Creating buttons manually
        buttons = []
        temp = []

        for g in groups_list:
            # For the OTHERS group we use the localized name
            if g == "OTHERS":
                display_name = strings["OTHERS"][lang]
            else:
                display_name = g

            button = InlineKeyboardButton(display_name, callback_data=g + "_GROUP")
            temp.append(button)

            # Two buttons in a row
            if len(temp) == 2:
                buttons.append(temp)
                temp = []

        # Add the remaining buttons
        if temp:
            buttons.append(temp)

        back_button_data = "BACK"  # To return to the main menu
    else:
        # Showing all models (if there are no groups)
        buttons = create_buttons(initial_model, Suffix="_MODELS")
        back_button_data = "BACK"  # To return to the main menu

    # Adding a "Back" button with appropriate callback_data
    buttons.append(
        [
            InlineKeyboardButton(strings['button_back'][lang], callback_data=back_button_data),
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
