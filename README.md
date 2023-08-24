# ChatGPT Telegram Bot

## ✨ Features

✅ 支持 ChatGPT API 和 GPT4 API

✅ 异步处理消息，多线程回答问题，支持对话隔离，不同用户不同对话

✅ 支持精准的消息 Markdown 渲染，用的是我的另一个[项目](https://github.com/yym68686/md2tgmd)

✅ 支持 ChatGPT 流式输出，实现打字机效果

✅ 增加一键 Replit 部署，真正的零成本，傻瓜式部署，支持 kuma 防睡眠

✅ 全平台，随时随地，只要有 telegram 就可以打破知识壁垒

✅ 支持 docker，fly.io 部署

## Zeabur 远程部署 (推荐)

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

设置好域名和环境变量后，重新部署即可。

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt --index-url https://pypi.python.org/simple/ > /dev/null && python3 main.py
```

在左边栏 Tools 里面选择 Secrets，添加机器人需要的环境变量，一共四个：

- BOT_TOKEN: 你需要在 [BotFather](https://t.me/BotFather) 创建一个 bot 以获取 BOT_TOKEN
- WEB_HOOK: 在 Replit 会自动分配一个域名给你，填入 `https://appname.username.repl.co`
- API: openai 的 api key。
- API4: openai gpt4 的 api key。
- API_URL: 调用 api 的地址，默认是：https://api.openai.com/v1/chat/completions
- GPT_ENGINE：模型名字，默认是 `gpt-3.5-turbo`
- NICK: 可选，默认为空，NICK 是机器人的名字。当用户输入消息以 NICK 开头，机器人才会回答，否则机器人会回答任何消息。尤其在群聊里，没有 NICK，机器人会对所有消息进行回复。
- PASS_HISTORY: 可选，默认为真，表示机器人会记住对话历史，下次回复时会考虑上下文。如果设置为假，机器人会忘记对话历史，只考虑当前对话。

点击屏幕上方的 run，即可运行机器人。记得打开 Always On。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

输入应用的名字，若提示初始化 Postgresql 或 Redis，一律选择否。

按照提示部署。在官网控制面板会提供一个二级域名，可以使用这个二级域名访问到服务。

设置环境变量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
flyctl secrets set COOKIES=
# 可选
flyctl secrets set NICK=javis
```

查看所有环境变量

```bash
flyctl secrets list
```

移除环境变量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh 连接 fly.io 容器

```bash
# 生成密钥
flyctl ssh issue --agent
# ssh 连接
flyctl ssh establish
```

查看 webhook url 是否正确

```
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker 本地部署

下载镜像

```bash
docker pull yym68686/chatgpt:1.0
```

启动容器

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e COOKIES= \
    chatgpt:1.0
```

或者你想使用 Docker Compose，下面是 docker-compose.yml 示例:

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:1.0
    environment:
      - NICK=
      - BOT_TOKEN=
      - WEB_HOOK=
      - API=
      - COOKIES=
    ports:
      - 80:8080
```

仓库打包 Docker 镜像

```bash
docker build --no-cache -t chatgpt:1.0 --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## Reference

参考项目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 markdown 渲染用的是我的另一个项目：https://github.com/yym68686/md2tgmd