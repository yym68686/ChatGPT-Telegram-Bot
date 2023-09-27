# ChatGPT 电报机器人

加入 [电报群](https://t.me/+_01cz9tAkUc1YzZl) 分享您的用户体验或报告错误。

[英语](./README.md) | [简体中文](./README.zh-CN.md) | [繁体中文](./README.zh-TW.md)

## ✨ 特征

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google🔍 进行在线搜索。 duckduckgo 搜索是默认提供的，而 Google 搜索的官方 API 需要用户申请。它可以提供 GPT 以前无法回答的实时信息，例如微博热搜今天，某地今天的天气，以及某人或新闻的进展。

✅ 支持基于嵌入式向量数据库的文档 QA。在搜索中，对于搜索的 PDF，会执行 PDF 文档的自动向量语义搜索，并基于向量数据库提取 pdf 相关内容。支持使用“qa”命令对“sitemap.xml”文件的整个网站进行向量化，并根据向量数据库回答问题，特别适用于某些项目的文档网站和 wiki 网站。

✅ 支持通过聊天窗口中的“info”命令在 GPT3.5、GPT4 和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持隔离对话，不同用户有不同的对话

✅ 支持消息的精确 Markdown 渲染，使用我另一个 [项目](https://github.com/yym68686/md2tgmd)

✅ 支持流输出，实现打字机效果

✅ 支持白名单防止滥用和信息泄露

✅ 跨平台，在Telegram上随时随地打破知识障碍

✅ 支持一键 Zeabur、Replit 部署，真正的零成本，白痴化部署，并支持 kuma 防睡眠。也支持 Docker、fly.io 部署

## 环境变量

| 变量名称                  | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **BOT_TOKEN (必需)**      | Telegram 机器人令牌。在 [BotFather](https://t.me/BotFather) 上创建机器人以获取 BOT_TOKEN。 |
| **WEB_HOOK (必需)**       | 电报机器人每当收到用户消息都会将消息传递给 WEB_HOOK，在那里机器人将会监听并及时处理收到的消息。 |
| **API (必需)**            | OpenAI 或第三方 API 密钥。                                |
| API_URL（可选）           | 如果您使用的是 OpenAI 官方 API，则不需要设置此项。如果您使用的是第三方 API，则需要填写第三方代理网站。默认为: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选）        | 设置默认的 QA 模型；默认值为：`gpt-3.5-turbo`。可以使用机器人的“info”命令自由切换此项，原则上不需要设置。 |
| NICK（可选）              | 默认为空，NICK 是机器人的名字。仅当用户输入的消息以 NICK 开头时，机器人才会回答，否则机器人将回答任何消息。特别是在群聊中，如果没有 NICK，则机器人将对所有消息进行回答。 |
| PASS_HISTORY（可选）      | 默认为 true。机器人会记住对话历史记录，并在下次回答时考虑上下文。如果设置为 false，则机器人将忘记对话历史记录，并且仅考虑当前对话。 |
| GOOGLE_API_KEY（可选）    | 如果需要使用 Google 搜索，则需要设置。如果不设置此环境变量，则机器人默认提供 duckduckgo 搜索。在 Google Cloud 的 [API 和服务](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中创建凭据，API 密钥将在凭据页面上是 GOOGLE_API_KEY。Google 搜索一天可以查询 100 次，这对于轻度使用完全足够。当使用限制已达到时，机器人将自动关闭 Google 搜索。 |
| GOOGLE_CSE_ID（可选）     | 如果需要使用 Google 搜索，则需要与 GOOGLE_API_KEY 一起设置。在 [可编程搜索引擎](https://programmablesearchengine.google.com/) 中创建一个搜索引擎，搜寻引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist（可选）        | 设置哪些用户可以访问机器人，并使用“，”将授权使用机器人的用户 ID 连接起来。默认值为 `None`，这意味着机器人向所有人开放。 |

## Zeabur 远程部署（推荐）

一键部署：

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要后续功能更新，则建议使用以下部署方法：

首先 fork 本仓库，然后注册 [Zeabur](https://zeabur.com)。免费配额足够轻度使用。从您自己的 Github 仓库导入，设置域名（必须与 WEB_HOOK 一致）和环境变量，并重新部署。如果您需要后续的功能更新，只需将此存储库同步到您自己的存储库中，并在 Zeabur 重新部署以获得最新的功能即可。

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在 Tools 侧边栏中选择 Secrets，添加机器人所需的环境变量，其中：

- WEB_HOOK：Replit 将自动为您分配一个域名，填写 `https://appname.username.repl.co`
- 记得打开“始终保持活动状态”

单击屏幕顶部的运行按钮以运行机器人。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

提示输入应用程序名称，并选择是否初始化 PostgreSQL 或 Redis。

按提示部署。在官方控制面板中提供一个次级域名，可用于访问服务。

设置环境变量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# optional
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

ssh 到 fly.io 容器

```bash
flyctl ssh issue --agent
# ssh connection
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

或者如果您想要使用 Docker Compose，这是一个 docker-compose.yml 示例：

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

将 Docker 映像打包到存储库中，并将其上传到 Docker Hub

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

消息的 Markdown 渲染使用了我的另一个 [项目](https://github.com/yym68686/md2tgmd)。

## 星标历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>