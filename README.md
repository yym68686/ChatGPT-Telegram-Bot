# ChatGPT Telegram Bot

Join the [Telegram Group](https://t.me/+_01cz9tAkUc1YzZl) chat to share your user experience or report Bugs.

[英文](./README.md) | [简体中文](./README.zh-CN.md) ｜ [繁体中文](./README.zh-TW.md)

## ✨ Features

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持 duckduckgo，Google 联网搜索🔍。默认提供 duckduckgo 搜索，google 搜索需要自行申请官方 API。可以回答之前 gpt 回答不了的实时信息，比如今天的微博热搜，今天某地的天气，某某人或新闻的进展

✅ 支持基于嵌入向量数据库的文档问答。在搜索中，对于搜索到的 pdf，可以自动对 PDF 文档进行向量化语义搜索，并基于向量数据库提取 pdf 相关的内容。支持使用 qa 命令对含有 sitemap.xml 文件的网站整体向量化，并基于向量数据库回答问题，特别适合一些项目的文档网站，wiki 网站

✅ 支持在聊天框内使用 info 命令通过点击按钮自由切换 gpt3.5，gpt4 等模型

✅ 异步处理消息，多线程回答问题，支持对话隔离，不同用户不同对话

✅ 支持精准的消息 Markdown 渲染，用的是我的另一个[项目](https://github.com/yym68686/md2tgmd)

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，防止滥用与信息泄漏

✅ 全平台，随时随地，只要有 telegram 就可以打破知识壁垒

✅ 支持一键 Zeabur，Replit 部署，真正的零成本，傻瓜式部署，支持 kuma 防睡眠。同时支持 docker，fly.io 部署

## 环境变量

| 变量名称               | 备注                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN（必填）**  | telegram 机器人令牌，在 [BotFather](https://t.me/BotFather) 创建一个 bot 以获取 BOT_TOKEN。 |
| **WEB_HOOK（必填）**   | telegram bot 每次收到用户消息，都会把消息传给 WEB_HOOK，机器人会在此监听，及时处理 telegram 里面收到的消息。 |
| **API（必填）**        | OpenAI 或者第三方的 api key。                                |
| API_URL（可选）        | 如果使用 OpenAI 官方 API，不需要设置此项。如果使用第三方API，需要填写第三方代理网址，默认值为：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选）     | 设置默认的问答模型，默认为：`gpt-3.5-turbo`，该项可以使用机器人 info 命令自由切换，原则上不需要设置。 |
| NICK（可选）           | 默认为空，NICK 是机器人的名字。当用户输入消息以 NICK 开头，机器人才会回答，否则机器人会回答任何消息。尤其在群聊里，没有 NICK，机器人会对所有消息进行回复。 |
| PASS_HISTORY（可选）   | 默认为真，表示机器人会记住对话历史，下次回复时会考虑上下文。如果设置为假，机器人会忘记对话历史，只考虑当前对话。 |
| GOOGLE_API_KEY（可选） | 如果需要谷歌搜索，则需要设置。如果不设置此环境变量，机器人默认提供 duckduckgo 搜索。在 Google cloud 的 [API 与服务](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中创建凭据，在凭据页面 API Key 就是 GOOGLE_API_KEY。Google 搜索一天可以查询 100 次，轻度使用完全足够，达到限额，机器人会自动关闭 Google 搜索。 |
| GOOGLE_CSE_ID（可选）  | 如果需要谷歌搜索，则需要与 GOOGLE_API_KEY 一起设置。在[可编程搜索引擎](https://programmablesearchengine.google.com/) 中新建搜索引擎，其中 搜索引擎 ID 就是 GOOGLE_CSE_ID 的值。 |
| whitelist（可选）      | 设置哪些用户可以访问机器人，将授权使用机器人的用户 ID 用`,`连接起来。默认值为`None`，即对所有人开放机器人。 |

## Zeabur 远程部署 (推荐)

一键部署：

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果需要后续功能更新，则推荐以下部署方式：

先 fork 本仓库，再注册 [Zeabur](https://zeabur.com)，免费额度足够轻度使用，从自己的 Github 仓库导入，设置好域名（必须与 WEB_HOOK 一致）和环境变量后，重新部署即可。后续需要功能更新只需要在自己的仓库里同步本仓库并在 Zeabur 重新部署即可获得最新功能。

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在左边栏 Tools 里面选择 Secrets，添加机器人需要的环境变量，其中：

- WEB_HOOK: 在 Replit 会自动分配一个域名给你，填入 `https://appname.username.repl.co`

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

启动容器

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者你想使用 Docker Compose，下面是 docker-compose.yml 示例:

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

后台运行 Docker Compose 容器

```bash
docker-compose up -d
```

仓库打包 Docker 镜像，推送到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
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

## Star History

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>