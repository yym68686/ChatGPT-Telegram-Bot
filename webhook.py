import telegram
from bot import setup
from urllib import parse
from waitress import serve
from threading import Thread
from flask import Flask, request, jsonify
from config import BOT_TOKEN, WEB_HOOK, PORT
from flask import request
import datetime

app = Flask(__name__)
updater, dispatcher = setup(BOT_TOKEN)

@app.route('/', methods=['GET'])
def hello():
    return 'Bot has connected!'
@app.before_request
def log_request_info():
    now = datetime.datetime.now()
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    print(f'访问ip: {ip_address}, 时间:{now}\n设备： {user_agent}')

@app.route(rf'/{BOT_TOKEN}'.format(), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    thread = Thread(target=dispatcher.process_update, args=(update,))
    thread.start()
    return jsonify({'status': 'success', 'message': 'Received message successfully.'})

@app.route('/setwebhook', methods=['GET', 'POST'])
def configure_webhook():
    webhookUrl = parse.urljoin(WEB_HOOK,rf"/{BOT_TOKEN}")
    result = updater.bot.setWebhook(webhookUrl)
    if result:
        print(rf"webhook configured: {webhookUrl}")
        return rf"webhook configured: {webhookUrl}"
    else:
        print(rf"webhook setup failed")
        return rf"webhook setup failed"

if __name__ == '__main__':
    configure_webhook()
    serve(app, host="0.0.0.0", port=8080)
