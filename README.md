# ChatGPT & New Bing Telegram Bot

本项目测试所用 openai api key 由🦄️[独角兽GPT](https://freeopenai.xyz/) “开发者扶持计划”免费提供。

## 特性

✅ 同时集成 ChatGPT 和 New Bing

✅ 异步处理消息，多线程回答问题

✅ 支持消息 Markdown 渲染

✅ 支持 New Bing 流式输出，实现打字机效果

✅ 同时对比 ChatGPT 和 New Bing 的消息

✅ 增加 Replit 部署，真正的零成本，傻瓜式部署，支持 kuma 防睡眠

✅ 全平台，随时随地，只要有 telegram 就可以打破知识壁垒

✅ 支持 docker，fly.io 部署

## Replit 远程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Bing-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Bing-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt --index-url https://pypi.python.org/simple/ > /dev/null && python3 webhook.py
```

在左边栏 Tools 里面选择 Secrets，添加机器人需要的环境变量，一共四个：

- BOT_TOKEN: 你需要在 [BotFather](https://t.me/BotFather) 创建一个 bot 以获取 BOT_TOKEN
- WEB_HOOK: 在 Replit 会自动分配一个域名给你，填入 `https://appname.username.repl.co`
- API: openai 的 api key.
- COOKIES: bing.com 的 cookies。可以用 [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 点击链接安装插件，点导出会自动复制到剪贴板。有效期两周，一个对话有 20 次提问，过期后每个对话提问次数限制在 5 次。
- NICK: 可选，默认为空，NICK 是机器人的名字。当用户输入消息以 NICK 开头，机器人才会回答，否则机器人会回答任何消息。尤其在群聊里，没有 NICK，机器人会对所有消息进行回复。

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

## Reference

参考项目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

[acheong08/EdgeGPT: Reverse engineered API of Microsoft&#39;s Bing Chat AI (github.com)](https://github.com/acheong08/EdgeGPT)

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 markdown 渲染用的是我的另一个项目：https://github.com/yym68686/md2tgmd
