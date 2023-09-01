FROM yym68686/chatgpt:1.0
WORKDIR /home
EXPOSE 8080
ENTRYPOINT ["
    rm -rf ChatGPT-Telegram-Bot/ 
    && git clone --depth 1 -b main https://github.com/yym68686/ChatGPT-Telegram-Bot.git
    && python -u /home/ChatGPT-Telegram-Bot/main.py
"]