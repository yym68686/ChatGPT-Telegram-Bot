#!/bin/bash
set -eu
rm -rf /home/ChatGPT-Telegram-Bot
git clone --depth 1 -b main https://github.com/yym68686/ChatGPT-Telegram-Bot.git
pip install -U md2tgmd
python -u /home/ChatGPT-Telegram-Bot/bot.py