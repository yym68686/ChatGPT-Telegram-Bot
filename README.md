# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 聊天，分享您的用戶體驗或報告錯誤。

[英文](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google 进行在线搜索🔍。默认提供 DuckDuckGo 搜索，而 Google 搜索需要用户申请官方 API。它可以提供 GPT 以前无法回答的即时信息，例如今日微博热搜，某个地方今天的天气和某个人或新闻的进展情况。

✅ 支持基于嵌入式向量数据库的文档 QA。在搜索中，对于已搜索的 PDF，执行自动矢量语义搜索PDF文档，并根据矢量数据库提取与PDF相关的内容。支持使用“qa”命令向量化带有“sitemap.xml”文件的整个网站，并基于矢量数据库回答问题，特别适用于某些项目的文档网站和 wiki 网站。

✅ 支持通过聊天窗口中的“info”命令在 GPT3.5，GPT4 和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持孤立的对话，不同的用户有不同的对话

✅ 支持准确的消息 Markdown 渲染，使用我另一个 [项目](https://github.com/yym68686/md2tgmd)

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，以防止滥用和信息泄漏

✅ 跨平台，在 Telegram 上随时随地突破知识障碍

✅ 支持一键 Zeabur、Replit 部署，真正的零费用，傻瓜式部署，并支持 kuma 防睡眠。还支持 Docker、fly.io 部署

## 环境变量

| 变量名              | 注释                                     |
| ------------------- | ---------------------------------------- |
| *BOT_TOKEN (required)* | Telegram 机器人令牌。在 [BotFather](https://t.me/BotFather)上创建一个机器人以获取 BOT_TOKEN。 |
| *WEB_HOOK (required)* | 每当 Telegram 机器人接收到用户的消息，该消息将被传递给 WEB_HOOK，机器人将在那里侦听并及时处理收到的消息。 |
| *API (required)* | OpenAI 或第三方 API 密钥。 |
| API_URL（可选） | 如果使用 OpenAI 官方 API，则不需要设置此选项。如果使用第三方 API，则需要填写第三方代理网站。默认值为：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选） | 设置默认的 QA 模型；默认值为：`gpt-3.5-turbo`。此项可以使用机器人的“info”命令随意切换，并且原则上不需要设置。 |
| NICK（可选） | 默认为空，NICK 是机器人的名称。只有当用户输入的消息以 NICK 开头时，机器人才会响应，否则机器人将响应所有消息。特别是在群聊中，如果没有 NICK，则机器人将回复所有消息。 |
| PASS_HISTORY（可选） | 默认为 true。机器人记住对话历史记录，并在下次回复时考虑上下文。如果设置为 false，则机器人会忘记对话历史记录，只考虑当前对话。 |
| GOOGLE_API_KEY（可选） | 如果需要使用 Google 搜索，则需要设置它。如果未设置此环境变量，则机器人将默认提供 duckduckgo 搜索。在 Google Cloud 的 [APIs＆Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中创建凭据，API 密钥将是凭据页面上的 GOOGLE_API_KEY。Google 搜索每天可以查询 100 次，对于轻度使用完全足够。使用量达到限制时，机器人将自动关闭 Google 搜索。 |
| GOOGLE_CSE_ID（可选） | 如果需要使用 Google 搜索，则需要与 GOOGLE_API_KEY 一起设置。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中创建搜索引擎，搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| 万能钥匙（可选） | 设置哪些用户可以访问机器人，并将授权使用机器人的用户 ID 与“，”连接起来。默认值为`无`，这意味着机器人向所有人开放。 |

## Zeabur 远程部署（推荐）

一键部署：

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要后续功能更新，则建议使用以下部署方法：

首先，Fork 此存储库，然后注册 [Zeabur](https://zeabur.com)。在轻度使用的情况下，免费配额是足够的。从您自己的 Github 存储库导入后，设置域名（必须与 WEB_HOOK 一致）和环境变量，并重新部署。如果需要随后的功能更新，请在自己的存储库中同步此存储库，然后在 Zeabur 中重新部署以获取最新功能。

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 GitHub 存储库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

选择 Tools 侧边栏中的 Secrets，添加机器人所需的环境变量，其中：

- WEB_HOOK：Replit 将为您自动分配一个域名，填写“https://appname.username.repl.co”
- 记住要打开“始终开启”

单击屏幕顶部的运行按钮以运行机器人。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

提示输入应用程序名称，然后选择“不”以初始化 PostgreSQL 或 Redis。

按照提示进行部署。官方控制面板中将提供第二个域名，可用于访问服务。

设置环境变量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# 可选
flyctl secrets set NICK=javis
```

查看所有环境变量

```bash
flyctl secrets list
```

删除环境变量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh 到 fly.io 容器

```bash
flyctl ssh issue --agent
# ssh 连接
flyctl ssh establish
```

检查 Webhook URL 是否正确

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker 本地部署

启动容器

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者，如果要使用 Docker Compose，以下是 docker-compose.yml 示例：

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:1.0
    environment:
      - BOT_TOKEN=
      - WEB_HOOK=
      - API=
      - API_URL=
    ports:
      - 80:8080
```

在后台运行 Docker Compose 容器

```bash
docker-compose up -d
```

在存储库中打包 Docker 镜像并将其上传到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 参考

参考项目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 Markdown 渲染使用了我另一个 [项目](https://github.com/yym68686/md2tgmd)。 

## Star 历史记录

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>