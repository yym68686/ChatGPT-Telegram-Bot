import os
MODE = os.environ.get('MODE', 'prod')
WEB_HOOK = os.environ["WEB_HOOK"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get('PORT', '8080'))
NICK = os.environ.get('NICK', None)
config = {
    "Authorization": "",
    "session_token": os.environ["session_token"]
}