import telegram
from bot import setup
from urllib import parse
from waitress import serve
# from chat import refreshSession
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from config import BOT_TOKEN, WEB_HOOK, PORT


app = Flask(__name__)
updater, dispatcher = setup(BOT_TOKEN)
scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))

# @app.before_first_request
# def setup_scheduler():
#     # 在应用初始化时添加定时任务
#     scheduler.add_job(func=refreshSession, trigger="interval", hours=1, id="myscheduler")

@app.route('/', methods=['GET'])
def hello():
    return 'hello world!'

@app.route(rf'/{BOT_TOKEN}'.format(), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    print("flask: Get a POST, send to bot.")
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return jsonify({"status": "ok"})

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
    scheduler.start()
    configure_webhook()
    serve(app, host="0.0.0.0", port=8080)
    # app.run(host='127.0.0.1', port=PORT, debug=False)