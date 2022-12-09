# ChatGPT Telegram Bot in fly.io

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
pip install -r /home/ChatGPT-Telegram-Bot/requirements.txt > /dev/null
echo "python env downloaded..." >> /home/log 2>&1
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
RUN apt-get update && apt -y install git \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/setup.sh"]
```

构建

```bash
docker build --no-cache -t chatgpt:1.0 --platform linux/amd64 .
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
- URL 是 bot 的 webhook 地址，注意 url 后面跟一个斜杠。
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

## 部署到 fly.io

官方文档：https://fly.io/docs/

mac 安装 flyctl

```bash
brew install flyctl
```

登陆 fly.io，提示输入信用卡，绑定信用卡后有免费服务器提供。

```bash
flyctl auth login
```

使用 Docker 镜像部署 fly.io 应用

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

输入应用的名字。

按照提示部署。在官网控制面板会提供一个二级域名，可以使用这个二级域名访问到服务。

设置环境变量

```bash
flyctl secrets set URL=https://*****.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set session_token=****
flyctl secrets set MODE=prod
```

查看所有环境变量

```bash
flyctl secrets list
```

移除环境变量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

查看 webhook url 是否正确

```
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Reference

参考项目：https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless
