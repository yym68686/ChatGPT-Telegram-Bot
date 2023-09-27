# ChatGPT 电报机器人

加入[电报群](https://t.me/+_01cz9tAkUc1YzZl)以分享用户体验或报告错误。

[英文](./ README.md) | [简体中文](./ README.zh-CN.md) | [繁體中文](./ README.zh-TW.md)

## ✨ 特性

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google 进行在线搜索。默认提供 DuckDuckGo 搜索，并且用户需要申请 Google 搜索的官方 API 才能使用。它可以提供 GPT 之前无法回答的实时信息，例如今天的微博热门搜索，某个地方今天的天气以及某个人或新闻的进展情况。

✅ 支持基于嵌入向量数据库的文档 QA。在搜索中，针对搜索的 PDF，会执行 PDF 文档的自动向量语义搜索，并根据向量数据库提取与 PDF 相关的内容。支持使用“qa”命令对带有“sitemap.xml”文件的整个网站进行矢量化处理，并基于向量数据库回答问题，特别适用于一些项目的文档网站和维基网站。

✅ 支持通过聊天窗口中的“info”命令在 GPT3.5、GPT4 和其他模型之间切换

✅ 异步处理消息，支持多线程回答问题，支持隔离对话，不同的用户有不同的对话

✅ 支持准确的消息 Markdown 渲染，使用我的另一个 [项目](https://github.com/yym68686/md2tgmd)

✅ 支持流输出，实现打字机效果

✅ 支持白名单功能，以防止滥用和信息泄露

✅ 跨平台，在 Telegram 上随时随地打破知识壁垒

✅ 支持一键 Zeabur、Replit 部署，真正的零成本、白痴化部署，同时支持 Kuma 防睡眠。还支持 Docker、 fly.io 部署

## 环境变量

| 变量名称                | 注释                                                         |
| ----------------------| ------------------------------------------------------------ |
| **BOT_TOKEN（必需）**   | 电报机器人令牌。在 [BotFather](https://t.me/BotFather) 上创建机器人即可获得 BOT_TOKEN。|
| **WEB_HOOK（必需）**    | 每当电报机器人接收到用户消息时，消息都会传递到 WEB_HOOK，机器人将在其中监听并及时处理接收到的消息。 |
| **API（必需）**           | OpenAI 或第三方 API 密钥。                                |
| API_URL（可选）           | 如果您正在使用 OpenAI 官方 API，则不需要设置此项。如果您使用第三方 API，则需要填写第三方代理网站。默认值为：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选）        | 设置默认的 QA 模型；默认值为:`gpt-3.5-turbo`。该项可以使用机器人的“信息”命令自由切换，原则上不需要设置 |
| NICK（可选）              | 默认为空，NICK 是机器人的名称。当用户输入的消息以 NICK 开头时，机器人才会回复，否则机器人将回复任何消息。特别是在群聊中，如果没有 NICK，则机器人会回复所有消息。 |
| PASS_HISTORY（可选）      | 默认为 true。机器人会记住会话历史记录，并在下次回复时考虑上下文。如果设置为 false，则机器人会忘记会话历史记录，仅考虑当前会话。|
| GOOGLE_API_KEY（可选）    | 如果您需要使用 Google 搜索，则需要设置它。如果您没有设置此环境变量，则机器人将默认提供 duckduckgo 搜索。在 Google Cloud 的 [APIs＆Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 上创建凭据，API 密钥将是凭据页面上的 GOOGLE_API_KEY。Google 搜索可以查询 100 次，完全可以满足轻量级使用。达到使用限制后，机器人将自动关闭 Google 搜索。|
| GOOGLE_CSE_ID（可选）     | 如果您需要使用 Google 搜索，则需要与 GOOGLE_API_KEY 一起设置。在[可编程搜索引擎](https://programmablesearchengine.google.com/)上创建一个搜索引擎，其中搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| 白名单（可选）            | 设置哪些用户可以访问机器人，并使用“，”将授权使用机器人的用户 ID 连接起来。默认值为 `None`，这意味着机器人向所有人打开。 |

## Zeabur 远程部署（推荐）

一键部署:

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要后续功能更新，建议使用以下部署方法：

首先 fork 此仓库，然后注册[Zeabur](https://zeabur.com)。免费配额对轻量级使用来说足够了。从您自己的 Github 仓库导入，设置域名（必须与 WEB_HOOK 一致）和环境变量，然后重新部署。如果您需要后续的功能更新，只需在自己的仓库中同步此仓库并在 Zeabur 中重新部署即可获得最新的功能。

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

选择工具边栏中的 Secrets，添加机器人所需的环境变量，其中：

- WEB_HOOK：Replit 将自动为您分配一个域名，请填写`https://appname.username.repl.co`
- 记得开启“始终开着”

单击屏幕顶部的运行按钮运行机器人。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

在提示时输入应用程序名称，选择否以初始化 Postgresql 或 Redis。

按照提示进行部署。在官方控制面板中提供一个辅助域名，可用于访问服务。

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
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者如果您想使用 Docker Compose，这里有一个 docker-compose.yml 示例：

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

将 Docker 镜像打包到仓库中，并将其上传到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 参考文献

参考项目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 markdown 渲染使用了我的另一个[项目](https://github.com/yym68686/md2tgmd)。

## 星标历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>