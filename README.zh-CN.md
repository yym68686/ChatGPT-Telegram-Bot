# ChatGPT Telegram Bot

加入 [Telegram 群组](https://t.me/+_01cz9tAkUc1YzZl) 聊天，分享您的用户体验或报告错误。

[英文](./README.md) | [简体中文](./README.zh-CN.md) | [繁体中文](./README.zh-TW.md)

## ✨ 特性

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google 进行在线搜索🔍。默认提供 DuckDuckGo 搜索，用户需要申请使用 Google 搜索的官方 API。它可以提供 GPT 以前无法回答的实时信息，例如今天的微博热搜、某地的天气以及某个人或新闻的进展。

✅ 支持基于嵌入向量数据库的文档 QA。在搜索中，对搜索到的 PDF 进行自动向量语义搜索，基于向量数据库提取与 PDF 相关的内容。支持使用 "qa" 命令使用 "sitemap.xml" 文件对整个网站进行向量化，并基于向量数据库回答问题，特别适用于一些项目的文档网站和维基网站。

✅ 支持通过聊天窗口中的 "info" 命令在 GPT3.5、GPT4 和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持隔离对话，不同用户有不同的对话

✅ 支持准确的消息 Markdown 渲染，使用我另一个 [项目](https://github.com/yym68686/md2tgmd) 进行渲染

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，防止滥用和信息泄露

✅ 跨平台，在任何时候、任何地方打破知识壁垒，使用 Telegram

✅ 支持一键 Zeabur、Replit 部署，真正的零成本、白痴化部署，支持 kuma 防睡眠。还支持 Docker、fly.io 部署

## 环境变量

| 变量名                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必填)**     | Telegram 机器人令牌。在 [BotFather](https://t.me/BotFather) 上创建一个机器人以获取 BOT_TOKEN。 |
| **WEB_HOOK (必填)**      | 每当 Telegram 机器人接收到用户消息时，消息将传递给 WEB_HOOK，机器人将监听并及时处理接收到的消息。 |
| **API (必填)**           | OpenAI 或第三方 API 密钥。                                  |
| API_URL(可选)           | 如果使用 OpenAI 官方 API，则不需要设置此项。如果使用第三方 API，则需要填写第三方代理网站。默认值为：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE(可选)        | 设置默认的 QA 模型；默认值为：`gpt-3.5-turbo`。可以使用机器人的 "info" 命令自由切换此项，原则上不需要设置。 |
| NICK(可选)              | 默认为空，NICK 是机器人的名称。只有当用户输入的消息以 NICK 开头时，机器人才会回复，否则机器人会对任何消息都回复。特别是在群聊中，如果没有 NICK，机器人将回复所有消息。 |
| PASS_HISTORY(可选)      | 默认为 true。机器人记住对话历史，并在下次回复时考虑上下文。如果设置为 false，机器人将忘记对话历史，只考虑当前对话。 |
| GOOGLE_API_KEY(可选)    | 如果需要使用 Google 搜索，需要设置此项。如果不设置此环境变量，机器人将默认提供 duckduckgo 搜索。在 Google Cloud 的 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中创建凭据，API 密钥将在凭据页面上的 GOOGLE_API_KEY 中。Google 搜索每天可以查询 100 次，对于轻度使用完全足够。当达到使用限制时，机器人将自动关闭 Google 搜索。 |
| GOOGLE_CSE_ID(可选)     | 如果需要使用 Google 搜索，需要与 GOOGLE_API_KEY 一起设置此项。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中创建一个搜索引擎，搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist(可选)         | 设置哪些用户可以访问机器人，并使用 ',' 连接授权使用机器人的用户 ID。默认值为 `None`，表示机器人对所有人开放。 |

## Zeabur 远程部署（推荐）

一键部署：

[![在 Zeabur 上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要后续的功能更新，建议使用以下部署方法：

首先 fork 此存储库，然后注册 [Zeabur](https://zeabur.com)。免费配额对于轻度使用足够。从您自己的 Github 存储库导入，设置域名（必须与 WEB_HOOK 一致）和环境变量，然后重新部署。如果您需要后续的功能更新，只需在您自己的存储库中同步此存储库，并在 Zeabur 中重新部署以获取最新的功能。

## Replit 远程部署

[![在 Repl.it 上运行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 存储库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在 Tools 侧边栏中选择 Secrets，添加机器人所需的环境变量，其中：

- WEB_HOOK：Replit 会自动为您分配一个域名，填写 `https://appname.username.repl.co`
- 记得打开 "Always On"

单击屏幕顶部的运行按钮来运行机器人。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

在提示时输入应用程序的名称，并选择 No 来初始化 Postgresql 或 Redis。

按照提示部署。在官方控制面板中提供了一个辅助域名，可以用来访问服务。

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

检查 webhook URL 是否正确

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker 本地部署

启动容器

```bash
docker run -p 80:8080 --name chatbot -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者如果您想使用 Docker Compose，这是一个 docker-compose.yml 示例：

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

将 Docker 镜像打包到存储库并上传到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 参考资料

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 Markdown 渲染使用了我另一个 [项目](https://github.com/yym68686/md2tgmd)。

## Star 历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>