# ChatGPT 电报机器人

加入 [Telegram 群组](https://t.me/+_01cz9tAkUc1YzZl)，分享您的用户体验或报告错误。

[英语](./README.md) | [简体中文](./README.zh-CN.md) | [繁体中文](./README.zh-TW.md)

## ✨ 特点

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google🔍 进行在线搜索。默认情况下提供 DuckDuckGo 搜索，需要用户申请 Google 搜索的官方 API。它可以提供 GPT 以前无法回答的实时信息，例如今天的微博热搜、某个地方的天气以及某个人或新闻的进展。

✅ 基于嵌入式向量数据库支持文档 QA。在搜索中，对于搜索到的 PDF，对 PDF 文档执行自动向量语义搜索，并根据向量数据库提取 PDF 相关内容。支持使用 “qa” 命令将整个网站与“sitemap.xml”文件向量化，并基于向量数据库回答问题，特别适用于一些项目的文档网站和 Wiki 网站。

✅ 支持通过聊天窗口中的 “info” 命令在 GPT3.5、GPT4 和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持隔离对话，不同用户有不同的对话

✅ 支持准确的 Markdown 渲染消息，使用我的另一个 [项目](https://github.com/yym68686/md2tgmd)

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，以防止滥用和信息泄露

✅ 跨平台，随时随地打破知识障碍，使用 Telegram

✅ 支持一键 Zeabur、Replit 部署，真正的零成本、白痴化部署，支持 kuma 反眠。还支持 Docker、fly.io 部署

## 环境变量

| 变量名称                 | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **BOT_TOKEN (required)** | Telegram 机器人令牌。在[BotFather](https://t.me/BotFather)上创建一个机器人以获取 BOT_TOKEN。 |
| **WEB_HOOK (required)**  | 每当 Telegram 机器人接收到用户的消息时，消息将传递到 WEB_HOOK，机器人会在 WEB_HOOK 上监听并及时处理所接收的消息。 |
| **API (required)**       | OpenAI 或第三方 API 密钥。                                   |
| API_URL(optional)        | 如果您使用的是 OpenAI 官方 API，则不需要设置此项。如果您使用的是第三方 API，则需要填写第三方代理网站。默认值为: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (optional)    | 设置默认的 QA 模型；默认值为:`gpt-3.5-turbo`。这个项目可以通过机器人的 “info” 命令自由切换，在原则上不需要设置。 |
| NICK (optional)          | 默认为空，NICK 是机器人的名称。只有当用户输入以 NICK 开头的消息时，机器人才会回复，否则机器人会回复任何消息。特别是在群聊中，如果没有 NICK，机器人将回复所有消息。 |
| PASS_HISTORY (optional)  | 默认值为 true。机器人会记住对话历史，并在下次回复时考虑上下文。如果设置为 false，机器人将忘记对话历史，只考虑当前对话。 |
| GOOGLE_API_KEY (optional)| 如果需要使用 Google 搜索，您需要设置它。如果未设置此环境变量，机器人默认提供 duckduckgo 搜索。在 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中创建凭据，并在凭据页面上 GOOGLE_API_KEY。Google 搜索可以查询 100 次/天，这对于轻度使用完全足够。当达到使用限制时，机器人将自动关闭 Google 搜索。 |
| GOOGLE_CSE_ID (optional) | 如果需要使用 Google 搜索，您需要与 GOOGLE_API_KEY 一起设置。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中创建一个搜索引擎，在其搜索引擎 ID 中填写 GOOGLE_CSE_ID 的值。 |
| 白名单 (optional)        | 设置哪些用户可以访问机器人，并连接授权使用机器人的用户 ID，以“，”分隔。默认值为 `None`，这意味着机器人向所有人开放。 |

## Zeabur 远程部署（推荐）

一键部署:

[![在 Zeabur 上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要跟进功能更新，则建议使用以下部署方法:

首先，派生此存储库，然后注册 [Zeabur](https://zeabur.com)。免费额度足以轻度使用。从您自己的 Github 存储库中导入，设置域名（必须与 WEB_HOOK 一致）和环境变量，然后重新部署。如果您需要后续功能更新，只需在自己的存储库中同步此存储库并在 Zeabur 中重新部署以获取最新的功能即可。

## Replit 远程部署

[![在 Repl.it 上运行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

在导入 Github 存储库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在工具侧边栏中选择 Secrets，添加机器人所需的环境变量，其中：

- WEB_HOOK：Replit 将自动为您分配一个域名，请填写 `https://appname.username.repl.co`
- 记得打开 “Always On”

单击屏幕顶部的运行按钮以运行机器人。

## fly.io 远程部署

官方文档：https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

提示时输入应用程序的名称，并选择 “No” 来初始化 Postgresql 或 Redis。

按提示操作进行部署。在官方控制面板中将提供一个次要域名，可用于访问该服务。

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

删除环境变量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh 到 fly.io 容器

```bash
flyctl ssh issue --agent
# ssh connection
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

或者，如果您想使用 Docker Compose，这里是一个 docker-compose.yml 的示例：

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

在存储库中打包 Docker 映像并将其上传到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 参考文献

参考项目:

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

我使用的消息的 Markdown 渲染是我的另一个 [项目](https://github.com/yym68686/md2tgmd)。

## 星星历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>