#!/bin/bash
set -eu
git clone --depth 1 -b main https://github.com/yym68686/ChatGPT-Telegram-Bot.git
cd ChatGPT-Telegram-Bot
pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt
nohup python -u /home/ChatGPT-Telegram-Bot/main.py 2>&1 &