import os
MODE = os.environ.get('MODE', 'prod')
URL = os.environ["URL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get('PORT', '8080'))
config = {
    "Authorization": "",
    "session_token": os.environ["session_token"]
}