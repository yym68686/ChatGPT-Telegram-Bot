#!/bin/bash
git clone --depth 1 -b main https://github.com/yym68686/ChatGPT-Telegram-Bot.git
cd ChatGPT-Telegram-Bot
pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt
nohup python -u /home/ChatGPT-Telegram-Bot/main.py 2>&1 &

# echo "code downloaded..." >> /home/log 2>&1
# cd ChatGPT-Telegram-Bot
# pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt > /dev/null
# echo "python env downloaded..." >> /home/log 2>&1
# touch /home/log
# nohup python -u /home/ChatGPT-Telegram-Bot/main.py >> /home/log 2>&1 &
# echo "web is starting..." >> /home/log 2>&1
# tail -f /home/log