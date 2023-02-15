#!/bin/bash
git clone --depth 1 https://github.com/yym68686/ChatGPT-Telegram-Bot.git > /dev/null
echo "code downloaded..." >> /home/log 2>&1
cd ChatGPT-Telegram-Bot
pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt > /dev/null
echo "python env downloaded..." >> /home/log 2>&1
# python -m playwright install --with-deps
touch /home/log
nohup python -u /home/ChatGPT-Telegram-Bot/webhook.py >> /home/log 2>&1 &
echo "web is starting..." >> /home/log 2>&1
tail -f /home/log