import os
WEB_HOOK = os.environ["WEB_HOOK"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get('PORT', '8080'))
NICK = os.environ.get('NICK', None)
API = os.environ.get('API', None)
API4 = os.environ.get('API4', None)
PASS_HISTORY = (os.environ.get('PASS_HISTORY', "True") == "False") == False
temperature = float(os.environ.get('temperature', '0.5'))