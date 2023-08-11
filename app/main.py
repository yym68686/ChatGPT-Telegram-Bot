import telegram
import threading
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import setup
from urllib import parse
from waitress import serve
from runasync import run_async
from flask import Flask, request, jsonify
from config import BOT_TOKEN, WEB_HOOK, PORT

app = Flask(__name__)
application = setup(BOT_TOKEN)

@app.route('/', methods=['GET'])
def hello():
    print("", end="")
    return 'Bot has connected!'

@app.route(rf'/{BOT_TOKEN}'.format(), methods=['POST'])
async def respond():
    update = telegram.Update.de_json(request.get_json(force=True), application.bot)
    run_async(application.initialize())
    thread = threading.Thread(target=run_async, args=(application.process_update(update),))
    thread.start()
    return jsonify({'status': 'success', 'message': 'Received message successfully.'})

@app.route('/setwebhook', methods=['GET', 'POST'])
async def configure_webhook():
    webhookUrl = parse.urljoin(WEB_HOOK,rf"/{BOT_TOKEN}")
    result = await application.bot.setWebhook(webhookUrl)
    if result:
        print(rf"webhook configured: {webhookUrl}")
        return rf"webhook configured: {webhookUrl}"
    else:
        print("webhook setup failed")
        return "webhook setup failed"

if __name__ == '__main__':
    run_async(configure_webhook())
    serve(app, host="0.0.0.0", port=PORT)