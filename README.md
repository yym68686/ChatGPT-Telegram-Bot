# ChatGPT Telegram Bot

## Docker

拉取镜像

```bash
docker pull yym68686/chatgpt:1.0
```

导出环境

```bash
pip freeze > requirements.txt
```

setup.sh

```bash
#!/bin/bash
git clone --depth 1 https://github.com/yym68686/ChatGPT-Telegram-Bot.git > /dev/null
echo "code downloaded..." >> /home/log 2>&1
cd ChatGPT-Telegram-Bot
touch /home/log
nohup python -u /home/ChatGPT-Telegram-Bot/webhook.py >> /home/log 2>&1 &
echo "web is starting..." >> /home/log 2>&1
tail -f /home/log
```

dockerfile

```dockerfile
FROM python:3.9.15-slim-bullseye
WORKDIR /home
EXPOSE 8080
COPY ./setup.sh /
COPY ./requirements.txt /
RUN apt-get update && apt -y install git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r /requirements.txt
ENTRYPOINT ["/setup.sh"]
```

构建

```bash
docker build -t chatgpt:1.0 --platform linux/amd64 .
```

运行

```bash
docker exec -it $(docker run -p 8080:8080 -dit \
-e BOT_TOKEN="5569***********FybvZJOmGrST_w" \
-e session_token="token" \
-e URL="https://test.com/" \
-e MODE="prod" \
chatgpt:1.0) bash
```

- 添加 telegram bot token 作为 BOT_TOKEN 变量
- URL 是 bot 的 webhook 地址
- MODE 设置生产环境 prod
- session_token 是 ChatGPT 的 cookie 中 `__Secure-next-auth.session-token` 的值

进入容器后查看日志

```bash
tail -f /home/log
```

关闭所有容器

```bash
docker rm -f $(docker ps -aq)
```

## Reference

参考项目：https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless
