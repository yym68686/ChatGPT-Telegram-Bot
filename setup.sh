#!/bin/bash
set -eu
git clone --depth 1 -b main https://github.com/yym68686/ChatGPT-Telegram-Bot.git
cd ChatGPT-Telegram-Bot
pip install --upgrade pip
pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt
python -u /home/ChatGPT-Telegram-Bot/main.py