<p align="center">
<img src="./assets/logo-3071751.jpg">
</p>

# 🤖️ TeleChat

[英文](README.md) | [中文](README_CN.md)

<p align="center">
  <a href="https://t.me/+_01cz9tAkUc1YzZl">
    <img src="https://img.shields.io/badge/Join Telegram Group-blue?&logo=telegram">
  </a>
  <a href="https://t.me/chatgpt68_bot">
    <img src="https://img.shields.io/badge/Telegram Bot-grey?&logo=Probot">
  </a>
   <a href="https://hub.docker.com/repository/docker/yym68686/chatgpt">
    <img src="https://img.shields.io/docker/pulls/yym68686/chatgpt?color=blue" alt="docker pull">
  </a>
</p>

ChatGPT Telegram 机器人是一个强大的 Telegram 机器人，可以使用多种主流的大语言模型 API，包括 GPT-3.5/4/4 Turbo/4o/5/o1，DALL·E 3，Claude2.1/3/3.5 API，Gemini 1.5 Pro/Flash，Vertex AI（Claude系列/Gemini系列），Groq Mixtral-8x7b/LLaMA2-70b 和 DuckDuckGo(gpt-4o-mini, claude-3-haiku, Meta-Llama-3.1-70B, Mixtral-8x7B)。它使用户能够在 Telegram 上进行高效的对话和信息搜索。

## ✨ 功能

- **多种AI模型**：支持GPT-3.5/4/4 Turbo/4o/5/o1，DALL·E 3，Claude2.1/3/3.5 API，Gemini 1.5 Pro/Flash，Vertex AI（Claude系列/Gemini系列），Groq Mixtral-8x7b/LLaMA2-70b 和 DuckDuckGo(gpt-4o-mini, claude-3-haiku, Meta-Llama-3.1-70B, Mixtral-8x7B)。还支持 one-api/new-api/[uni-api](https://github.com/yym68686/uni-api)。利用自研 API 请求后端 [SDK](https://github.com/yym68686/aient)，不依赖 OpenAI SDK。
- **多模态问答**：支持语音、音频、图像和 PDF/TXT/MD/python 文档的问答。用户可以直接在聊天框中上传文件使用。
- **群聊主题模式**: 支持在群聊中启用主题模式，在主题之间隔离API、对话历史、插件配置和偏好设置。
- **丰富的插件系统**：支持网页搜索（DuckDuckGo和Google）、URL 总结、ArXiv 论文总结和代码解释器。
- **用户友好界面**：允许在聊天窗口内灵活切换模型，并支持类似打字机效果的流式输出。支持精确的 Markdown 消息渲染，利用了我的另一个[项目](https://github.com/yym68686/md2tgmd)。
- **高效消息处理**：异步处理消息，多线程回答问题，支持隔离对话，并为不同用户提供独特对话。
- **长文本消息处理**: 自动合并长文本消息，突破Telegram的单条消息长度限制。当机器人的回复超过Telegram的限制时，它将被拆分成多条消息。
- **多用户对话隔离**：支持对话隔离和配置隔离，允许在多用户和单用户模式之间进行选择。
- **问题预测**: 自动生成后续问题，预测用户可能会接下来询问的问题。
- **多语言界面**：支持简体中文、繁体中文、俄文和英文界面。
- **白名单、黑名单和管理员设置**：支持设置白名单、黑名单和管理员。
- **内联模式**：允许用户在任何聊天窗口中 @ 机器人以生成答案，而无需在机器人的聊天窗口中提问。
- **方便部署**：支持一键部署到 koyeb、Zeabur、Replit，真正零成本和傻瓜式部署流程。还支持 kuma 防休眠，以及 Docker 和 fly.io 部署。
- **模型分组系统**: 将AI模型组织成逻辑组，便于选择。模型可以按提供商（GPT、Claude等）或按功能进行分组。没有明确指定组的模型会自动放入"OTHERS"组。这使得模型选择更直观，特别是当有很多模型可用时。

## 🍃 环境变量

以下是与机器人核心设置相关的环境变量列表：

| 变量名称 | 描述 | 是否必需? |
|---------------|-------------|-----------|
| BOT_TOKEN | Telegram 机器人令牌。 在 [BotFather](https://t.me/BotFather) 上创建一个机器人以获取 BOT_TOKEN。 | **是** |
| API | OpenAI 或第三方 API 密钥。 | 是 |
| GPT_ENGINE | 设置默认的QA模型；默认是：`gpt-5`。此项可以使用机器人的"info"命令自由切换，原则上不需要设置。 | 否 |
| WEB_HOOK | 每当电报机器人收到用户消息时，消息将被传递到 WEB_HOOK，机器人将在此监听并及时处理收到的消息。 | 否 |
| API_URL | 如果您使用的是OpenAI官方API，则无需设置此项。如果您使用的是第三方API，则需要填写第三方代理网站。默认值是：https://api.openai.com/v1/chat/completions | 否 |
| GROQ_API_KEY | Groq官方API密钥。 | 否 |
| GOOGLE_AI_API_KEY | Google AI 官方 API 密钥。使用此环境变量访问 Gemini 系列模型，包括 Gemini 1.5 pro 和 Gemini 1.5 flash。| 否 |
| VERTEX_PRIVATE_KEY | 描述: Google Cloud Vertex AI 服务账户的私钥。格式: 包含服务账户私钥信息的 JSON 字符串里面的 private_key 字段的值，请使用双引号包裹私钥。如何获取: 在 Google Cloud 控制台中创建一个服务账户，生成一个 JSON 密钥文件，并将其内容里面的 private_key 字段的值使用双引号包裹后设置为此环境变量的值。 | 否 |
| VERTEX_PROJECT_ID | 描述：您的 Google Cloud 项目 ID。格式：一个字符串，通常由小写字母、数字和连字符组成。如何获取：您可以在 Google Cloud 控制台的项目选择器中找到您的项目 ID。 | 否 |
| VERTEX_CLIENT_EMAIL | 描述：Google Cloud Vertex AI 服务账户的电子邮件地址。格式：通常是 "service-account-name@developer.gserviceaccount.com" 形式的字符串。获取方式：在创建服务账户时生成，或可以在 Google Cloud 控制台的 "IAM & 管理" 部分的服务账户详细信息中查看。 | 否 |
| claude_api_key | Claude 官方 API 密钥。 | 否 |
| CLAUDE_API_URL | 如果您使用的是Anthropic官方API，则无需设置此项。如果您使用的是第三方Anthropic API，则需要填写第三方代理网站。默认值是：https://api.anthropic.com/v1/messages | 否 |
| NICK | 默认是空的，NICK 是机器人的名字。机器人只会在用户输入的消息以 NICK 开头时才会响应，否则机器人会响应任何消息。特别是在群聊中，如果没有 NICK，机器人会回复所有消息。 | 否 |
| GOOGLE_API_KEY | 如果你需要使用谷歌搜索，你需要设置它。如果你不设置这个环境变量，机器人将默认提供duckduckgo搜索。 | No |
| GOOGLE_CSE_ID | 如果你需要使用谷歌搜索，你需要和 GOOGLE_API_KEY 一起设置。 | 否 |
| whitelist | 设置哪些用户可以访问机器人，并用 ',' 连接被授权使用机器人的用户ID。默认值是 `None`，这意味着机器人对所有人开放。 | 否 |
| BLACK_LIST | 设置哪些用户禁止访问机器人，并用 ',' 连接被授权使用机器人的用户ID。默认值是 `None` | 否 |
| ADMIN_LIST | 设置管理员列表。只有管理员可以使用 `/info` 命令配置机器人。 | 否 |
| GROUP_LIST | 设置可以使用机器人的群组列表。使用逗号（'，'）连接群组ID。即使群组成员不在白名单中，只要群组ID在GROUP_LIST中，群组的所有成员都可以使用机器人。 | 否 |
| CUSTOM_MODELS | 设置自定义模型名称列表。使用逗号（','）连接模型名称。如果需要删除默认模型，请在默认模型名称前添加连字符（-）。如果要删除所有默认模型，请使用 `-all`。要创建模型组，使用分号（';'）分隔组，使用冒号（':'）定义组名及其模型，例如：`CUSTOM_MODELS=-all,command,grok-2;GPT:gpt-5,gpt-3.5-turbo;Claude:claude-3-opus,claude-3-sonnet;OTHERS`。没有特定组的模型将自动放入"OTHERS"组。 | 否 |
| CHAT_MODE | 引入多用户模式，不同用户的配置不共享。当 CHAT_MODE 为 `global` 时，所有用户共享配置。当 CHAT_MODE 为 `multiusers` 时，用户配置彼此独立。 | 否 |
| temperature | 指定 LLM 的温度。默认值是 `0.5`。 | 否 |
| GET_MODELS | 指定是否通过 API 获取支持的模型。默认值为 `False`。 | 否 |
| SYSTEMPROMPT | 指定系统提示，系统提示是字符串，例如：`SYSTEMPROMPT=You are ChatGPT, a large language model trained by OpenAI. Respond conversationally`。默认是 `None`。系统提示的设置仅在 `CHAT_MODE` 为 `global` 时，系统提示的设置才会有效。当 `CHAT_MODE` 为 `multiusers` 时，系统提示的环境变量无论是任何值都不会修改任何用户的系统提示，因为用户不希望自己设置的系统系统被修改为全局系统提示。 | 否 |
| LANGUAGE | 指定机器人显示的默认语言，包括按钮显示语言和对话语言。默认是 `English`。目前仅支持设置为下面四种语言：`English`，`Simplified Chinese`，`Traditional Chinese`，`Russian`。同时也可以在机器人部署后使用 `/info` 命令设置显示语言 | 否 |
| CONFIG_DIR | 指定存储用户配置文件夹。CONFIG_DIR 是用于存储用户配置的文件夹。每次机器人启动时，它都会从 CONFIG_DIR 文件夹读取配置，因此用户每次重新启动时不会丢失之前的设置。您可以在本地使用 Docker 部署时，通过使用 `-v` 参数挂载文件夹来实现配置持久化。默认值是 `user_configs`。 | 否 |
| RESET_TIME | 指定机器人每隔多少秒重置一次聊天历史记录，每隔 RESET_TIME 秒，机器人会重置除了管理员列表外所有用户的聊天历史记录，每个用户重置时间不一样，根据每个用户最后的提问时间来计算下一次重置时间。而不是所有用户在同一时间重置。默认值是 `3600` 秒，最小值是 `60` 秒。 | 否 |

以下是与机器人偏好设置相关的环境变量列表，偏好设置也可以通过机器人启动后使用 `/info` 命令，点击 `偏好设置` 按钮来设置：

| 变量名称 | 描述 | 必需的? |
|---------------|-------------|-----------|
| PASS_HISTORY | 默认值是 `9999`。机器人会记住对话历史，并在下次回复时考虑上下文。如果设置为 `0`，机器人将忘记对话历史，只考虑当前对话。PASS_HISTORY 的值必须大于或等于 0。对应于偏好设置里面的名为 `对话历史` 的按钮。 | 否 |
| LONG_TEXT | 如果用户的输入消息的文本长度超出了 Telegram 的限制，并在很短的时间内连续发送多个消息，机器人会将这些多个消息视为一个。默认值是 `True`。对应于偏好设置里面的名为 `长文本合并` 的按钮。 | 否 |
| IMAGEQA | 是否启用图像问答，默认设置是模型可以回答图像内容，默认值为 `True`。对应于偏好设置里面的名为 `图片问答` 的按钮。 | 否 |
| LONG_TEXT_SPLIT | 当机器人的回复超过Telegram限制时，它将被拆分为多个消息。默认值是 `True`。对应于偏好设置里面的名为 `长文本分割` 的按钮。 | 否 |
| FILE_UPLOAD_MESS | 当文件或图像上传成功并且机器人处理完成时，机器人将发送一条消息，提示上传成功。默认值为 `True`。对应于偏好设置里面的名为 `文件上传成功提示消息` 的按钮。 | 否 |
| FOLLOW_UP | 自动生成多个相关问题供用户选择。默认值为 `False`。对应于偏好设置里面的名为 `猜你想问` 的按钮。 | 否 |
| TITLE | 是否在机器人回复的开头显示模型名称。默认值为 `False`。对应于偏好设置里面的名为 `模型标题` 的按钮。 | 否 |
| REPLY | 机器人是否应以"回复"格式回复用户的消息。默认值为 `False`。对应于偏好设置里面的名为 `回复消息` 的按钮。 | 否 |
<!-- | TYPING | 是否在机器人回复时显示"正在输入"状态。默认值为 `False`。 | 否 | -->


以下是与机器人插件设置相关的环境变量列表：

| 变量名称 | 描述 | 必需的？ |
|---------------|-------------|-----------|
| get_search_results | 是否启用搜索插件。默认值为 `False`。 | 否 |
| get_url_content | 是否启用URL摘要插件。默认值为 `False`。 | 否 |
| download_read_arxiv_pdf | 是否启用arXiv论文摘要插件。默认值为 `False`。 | 否 |
| run_python_script | 是否启用代码解释器插件。默认值为 `False`。 | 否 |
| generate_image | 是否启用图像生成插件。默认值为 `False`。 | 否 |
| get_time | 是否启用日期插件。默认值为 `False`。 | 否 |


## Koyeb 远程部署

可以使用两种方式部署在 koyeb 上部署，一种是使用 Koyeb 提供的 docker 镜像一键部署，另一种是导入本仓库部署。这两种方式都是免费的。第一种方式部署简单，但是无法自动更新，第二种方式部署稍微复杂，但是可以自动更新。

### 一键部署

点击下面的按钮可以自动使用构建好的 docker 镜像一键部署：

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=chatgpt&type=docker&image=docker.io%2Fyym68686%2Fchatgpt%3Alatest&instance_type=free&regions=was&instances_min=0&autoscaling_sleep_idle_delay=300&env%5BAPI%5D=&env%5BAPI_URL%5D=&env%5BBOT_TOKEN%5D=&env%5BWEB_HOOK%5D=https%3A%2F%2F%7B%7B+KOYEB_PUBLIC_DOMAIN+%7D%7D%2F)

在环境变量里面补全 BOT_TOKEN，API，API_URL 后直接点击部署按钮即可。WEB_HOOK 环境变量维持默认即可，不用修改，Koyeb 会自动分配一个二级域名。

### 仓库部署

1. fork 本仓库 [点击 fork 本仓库](https://github.com/yym68686/ChatGPT-Telegram-Bot/fork)

2. 部署时候需要选择以仓库的方式，`Run command` 设置为 `python3 bot.py`，`Exposed ports` 设置为 `8080`。

3. [安装 pull](https://github.com/apps/pull) 自动同步本仓库。

## Zeabur 远程部署

一键部署：

[![在 Zeabur 上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要后续功能更新，建议采用以下部署方法：

- 首先 fork 这个仓库，然后注册 [Zeabur](https://zeabur.com)。目前，Zeabur 不支持免费的 Docker 容器部署。如果你需要使用 Zeabur 来部署这个项目的机器人，你需要升级到 Developer Plan。幸运的是，Zeabur 推出了他们的[赞助计划](https://zeabur.com/docs/billing/sponsor)，为这个项目的所有贡献者提供一个月的 Developer Plan。如果你有想要增强的功能，欢迎提交 pull requests 到这个项目。
- 从您自己的Github仓库导入。
- 设置所需的环境变量，并重新部署。
- 如果您需要后续的功能更新，只需在您自己的代码库中同步此代码库，并在 Zeabur 中重新部署以获取最新功能。

## Replit 远程部署

[![在 Repl.it 上运行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入 Github 仓库后，设置运行命令

```bash
pip install -r requirements.txt > /dev/null && python3 bot.py
```

在工具侧边栏中选择"Secrets"，添加机器人所需的环境变量，其中：

- WEB_HOOK: Replit 会自动为您分配一个域名，填写 `https://appname.username.repl.co`
- 记得打开"始终开启"

点击屏幕顶部的运行按钮来运行机器人。

## fly.io 远程部署

官方文档: https://fly.io/docs/

使用 Docker 镜像部署 fly.io 应用程序

```bash
flyctl launch --image yym68686/chatgpt:latest
```

在提示时输入应用程序的名称，并选择"否"以初始化 Postgresql 或 Redis。

按照提示进行部署。官方控制面板将提供一个二级域名，可用于访问服务。

设置环境变量

```bash
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# 可选
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
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
    -e BOT_TOKEN=your_telegram_bot_token \
    -e API= \
    -e API_URL= \
    -v ./user_configs:/home/user_configs \
    yym68686/chatgpt:latest
```

或者如果你想使用 Docker Compose，这里有一个 docker-compose.yml 示例：

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:latest
    environment:
      - BOT_TOKEN=
      - API=
      - API_URL=
    volumes:
      - ./user_configs:/home/user_configs
    ports:
      - 80:8080
```

在后台运行 Docker Compose 容器

```bash
docker-compose pull
docker-compose up -d

# uni-api
docker-compose -f docker-compose-uni-api.yml up -d
```

将存储库中的Docker镜像打包并上传到Docker Hub

```bash
docker build --no-cache -t chatgpt:latest -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:latest yym68686/chatgpt:latest
docker push yym68686/chatgpt:latest
```

一键重启 Docker 镜像

```bash
set -eu
docker pull yym68686/chatgpt:latest
docker rm -f chatbot
docker run -p 8080:8080 -dit --name chatbot \
-e BOT_TOKEN= \
-e API= \
-e API_URL= \
-e GOOGLE_API_KEY= \
-e GOOGLE_CSE_ID= \
-e claude_api_key= \
-v ./user_configs:/home/user_configs \
yym68686/chatgpt:latest
docker logs -f chatbot
```

该脚本用于通过单个命令重启Docker镜像。它首先删除名为"chatbot"的现有Docker容器（如果存在）。然后，它运行一个名为"chatbot"的新Docker容器，暴露端口8080并设置各种环境变量。使用的Docker镜像是"yym68686/chatgpt:latest"。最后，它跟踪"chatbot"容器的日志。

## 🚀 源代码本地部署

python >= 3.10

直接从源代码运行机器人而不使用docker，克隆仓库：

```bash
git clone --recurse-submodules --depth 1 -b main --quiet https://github.com/yym68686/ChatGPT-Telegram-Bot.git
```

安装依赖项：

```bash
pip install -r requirements.txt
```

设置环境变量：

```bash
./configure_env.sh
```

运行：

```bash
python bot.py
```

## 🧩 插件

本项目支持多种插件，包括：DuckDuckGo 和 Google 搜索、URL 摘要、ArXiv 论文摘要、DALLE-3 画图和代码解释器等。您可以通过设置环境变量来启用或禁用这些插件。

- 如何开发插件？

插件相关的代码全部在本仓库 git 子模块 aient 里面，aient 是我开发的一个独立的仓库，用于处理 API 请求，对话历史记录管理等功能。当你使用 git clone 的 --recurse-submodules 参数克隆本仓库后，aient 会自动下载到本地。插件所有的代码在本仓库中的相对路径为 `aient/src/aient/plugins`。你可以在这个目录下添加自己的插件代码。插件开发的流程如下：

1. 在 `aient/src/aient/plugins` 目录下创建一个新的 Python 文件，例如 `myplugin.py`。通过在函数上面添加 `@register_tool()` 装饰器注册插件。`register_tool` 通过 `from .registry import register_tool` 导入。

4. utils/i18n.py 文件中添加插件名字各种语言的翻译。

完成上面的步骤，你的插件就可以使用了。🎉

## 📄 常见问题

- WEB_HOOK 环境变量有什么用？应该如何使用？

WEB_HOOK 是一个 webhook 地址。具体来说，当 Telegram 机器人收到用户消息时，它会将消息发送到 Telegram 服务器，然后 Telegram 服务器将消息转发到机器人设置的 WEB_HOOK 地址的服务器。因此，当消息发送到机器人时，机器人几乎立即执行处理程序。通过 WEB_HOOK 接收消息比未设置 WEB_HOOK 时的响应时间更快。

当使用 Zeabur、Replit 或 Koyeb 等平台部署机器人时，这些平台会提供一个域名，你需要将其填写在 WEB_HOOK 中，以便机器人接收用户消息。当然，不设置 WEB_HOOK 也是可以的，但机器人的响应时间会稍长一些，虽然差别不大，所以一般来说不需要设置 WEB_HOOK。

当在服务器上部署一个机器人时，你需要使用像nginx或caddy这样的反向代理工具，将Telegram服务器发送的消息转发到你的服务器，这样机器人才能接收到用户消息。因此，你需要将WEB_HOOK设置为你服务器的域名，并将请求WEB_HOOK的流量转发到机器人所在的服务器和相应端口。例如，在caddy中，你可以在caddy配置文件/etc/caddy/Caddyfile中这样配置：

```caddy
your_webhook_domain.com {
    reverse_proxy localhost:8082
}
```

- 为什么我不能使用谷歌搜索？

默认情况下，提供DuckDuckGo搜索。Google搜索的官方API需要用户申请。它可以提供GPT之前无法回答的实时信息，例如今天微博的热门话题、特定地点的今日天气，以及某个人或新闻事件的进展。

- 为什么即使我添加了Google搜索API，我还是不能使用搜索功能？

有两种可能性：

1. 只有支持工具使用的大型语言模型（LLM）API才能使用搜索功能。目前，本项目仅支持 OpenAI、Claude 和 Gemini 系列模型的 API 进行搜索功能。其他模型提供商的 API 目前不支持在本项目中使用工具。如果您有希望适配的模型提供商，可以联系维护者。

2. 如果您使用了 OpenAI、Claude 和 Gemini 系列模型的 API，但无法使用搜索功能，可能是因为搜索功能未启用。您可以通过 `/info` 命令点击偏好设置来检查搜索功能是否启用。

3. 如果您使用了 OpenAI、Claude 和 Gemini 系列模型的 API，请确保你使用的是官方 API，如果你使用的是第三方中转 API，提供商可能通过网页逆向的方式向你提供 API，通过网页逆向的方式提供 API 无法使用 tools use，即不能使用本项目所有的插件。如果你确认你使用的是官方 API，仍然无法成功搜索，请联系开发人员。

- 如何切换模型？

您可以在聊天窗口中使用 "/info" 命令在 GPT3.5/4/4o 和其他模型之间切换。

- 如何将模型组织成组？

你可以使用`CUSTOM_MODELS`环境变量，通过特殊语法来组织模型：
1. 使用分号（`;`）分隔不同的组
2. 使用冒号（`:`）定义组名及其包含的模型
3. 组内的模型使用逗号（`,`）分隔

例如：
```
CUSTOM_MODELS=-all;GPT:gpt-5,gpt-4,gpt-3.5-turbo;Claude:claude-3-opus,claude-3-sonnet,claude-3-haiku;Gemini:gemini-1.5-pro,gemini-1.0-pro;command,grok-2
```

这创建了三个组："GPT"、"Claude"和"Gemini"，每个组包含各自的模型。模型"command"和"grok-2"没有明确的组，所以它们会自动放入"OTHERS"组。

如果想创建一个空的"OTHERS"组（即使没有未分组的模型），可以在最后添加"OTHERS"：
```
CUSTOM_MODELS=-all;GPT:gpt-5;Claude:claude-3-opus;OTHERS
```

- 它可以在一个群组中部署吗？

是的，它支持群组白名单以防止滥用和信息泄露。

- 为什么我把机器人添加到群组后它不能说话？

如果这是您第一次将机器人添加到群聊中，您需要在botfather中将群组隐私设置为禁用，然后将机器人从群聊中移除并重新添加，以便正常使用。

第二种方法是将机器人设置为管理员，这样机器人就可以正常使用了。然而，如果你想将机器人添加到你不是管理员的群聊中，第一种方法更为合适。

另一种可能性是 GROUP_LIST 集不是当前的群聊 ID。请检查是否设置了 GROUP_LIST；GROUP_LIST 是群 ID，而不是群名称。群 ID 以减号开头，后跟一串数字。

- GROUP_LIST、ADMIN_LIST 和白名单的设置如何影响机器人的行为？

如果未设置白名单，所有人都可以使用机器人。如果设置了白名单，只有白名单中的用户可以使用机器人。如果设置了GROUP_LIST，只有GROUP_LIST中的群组可以使用机器人。如果同时设置了白名单和GROUP_LIST，群组中的所有人都可以使用机器人，但只有白名单中的用户可以私聊机器人。如果设置了ADMIN_LIST，只有ADMIN_LIST中的用户可以使用/info命令来更改机器人的设置。如果未设置ADMIN_LIST，所有人都可以使用/info命令来更改机器人的配置。GROUP_LIST 也可以包含频道，频道ID以减号开头，后跟一串数字。

- 我应该如何设置 API_URL？

API_URL 支持所有后缀，包括：https://api.openai.com/v1/chat/completions、https://api.openai.com/v1 和 https://api.openai.com/。机器人将根据不同的用途自动分配不同的端点。

- 是否有必要配置 web_hook 环境变量？

web_hook 不是强制性的环境变量。你只需要设置域名（必须与 WEB_HOOK 一致）和其他根据你的应用功能所需的环境变量。

- 我用docker compose部署了一个机器人。如果文档放在本地服务器上，应该挂载到哪个目录才能生效？我需要设置额外的配置和修改代码吗？

您可以直接通过聊天框将文档发送给机器人，机器人会自动解析文档。要使用文档对话功能，您需要启用历史对话功能。无需对文档进行额外处理。

- 我还是无法让它正常工作……我想在一个群组中使用它，我已经将 ADMIN_LIST 设置为我自己，并将 GROUP_LIST 设置为那个群组，白名单留空。但是，只有我可以在那个群组中使用它，群组中的其他成员被提示没有权限，这是怎么回事？

这是一个故障排除指南：请仔细检查 GROUP_LIST 是否正确。Telegram 群组的 ID 以负号开头，后跟一系列数字。如果不是，请使用此机器人 [bot](https://t.me/getidsbot) 重新获取群组 ID。

- 我上传了一个文档，但它没有根据文档的内容做出响应。怎么回事？

要使用文档问答功能，您必须先启用历史记录。您可以通过 `/info` 命令开启历史记录，或者通过将环境变量 `PASS_HISTORY` 设置为大于2来默认启用历史记录。请注意，启用历史记录将会产生额外费用，因此该项目默认不启用历史记录。这意味着在默认设置下无法使用问答功能。在使用此功能之前，您需要手动启用历史记录。

- 设置 `NICK` 后，当我 @ 机器人时没有响应，它只在消息以昵称开头时才回复。我怎样才能让它同时响应昵称和 @机器人名？

在群聊场景中，如果环境变量 `NICK` 未设置，机器人将接收所有群消息并回应所有消息。因此，有必要设置 `NICK`。设置 `NICK` 后，机器人只会回应以 `NICK` 开头的消息。所以，如果你想 @ 机器人以获得回应，你只需将 NICK 设置为 @botname。这样，当你在群里 @ 机器人时，机器人会检测到消息是以 @botname 开头的，并会回应该消息。

- 历史会保留多少条消息？

所有其他模型使用官方上下文长度设置，例如，`gpt-3.5-turbo-16k` 的上下文是 16k，`gpt-5` 的上下文是 128k，`Claude3/3.5` 的上下文是 200k。此限制是为了节省用户成本，因为大多数场景不需要高上下文。

- 如何从模型列表中删除默认模型名称？

你可以使用 `CUSTOM_MODELS` 环境变量来完成它。例如，如果你想添加 gpt-5 并从模型列表中移除 gpt-3.5 模型，请将 `CUSTOM_MODELS` 设置为 `gpt-5,-gpt-3.5`。如果你想一次性删除所有默认模型，你可以将 `CUSTOM_MODELS` 设置为 `-all,gpt-5`。

- 对话隔离具体是如何工作的？

对话总是基于不同的窗口隔离，而不是不同的用户。这意味着在同一个群聊窗口、同一个主题和同一个私聊窗口内，都会被视为同一个对话。CHAT_MODE 只影响配置是否隔离。在多用户模式下，每个用户的插件配置、偏好等都是独立的，互不影响。在单用户模式下，所有用户共享相同的插件配置和偏好。然而，对话历史总是隔离的。对话隔离是为了保护用户隐私，确保用户的对话历史、插件配置、偏好等不被其他用户看到。

- 为什么 Docker 镜像很久没有更新了？

Docker 镜像只存储程序的运行环境。目前，程序的运行环境是稳定的，环境依赖几乎没有变化，所以 Docker 镜像没有更新。每次重新部署 Docker 镜像时，它会拉取最新的代码，因此不需要担心 Docker 镜像更新的问题。

- 为什么容器在启动后报告错误 "http connect error or telegram.error.TimedOut: Timed out"?

此问题可能是由于部署 Docker 的服务器无法连接到 Telegram 服务器或 Telegram 服务器的不稳定性引起的。

1. 在大多数情况下，重新启动服务，检查服务器网络环境，或等待 Telegram 服务恢复即可。
2. 此外，您可以尝试通过网络钩子与Telegram服务器进行通信，这可能会解决问题。

- 如何让 docker 无限重试而不是一开始就停止？

Docker 中的 `--restart unless-stopped` 参数设置容器的重启策略。具体来说：

1. unless-stopped: 这个策略意味着容器如果停止了会自动重启，除非它是被手动停止的。换句话说，如果容器由于错误或系统重启而停止，它会自动重启。然而，如果你手动停止了容器（例如，使用docker stop命令），它将不会自行重启。
此参数对于需要连续运行的服务特别有用，因为它确保服务能够在意外中断后自动恢复，而无需手动干预。

2. 示例：假设你有一个运行 web 服务器的 Docker 容器，并且你希望它在崩溃或系统重启时自动重启，但在你手动停止它时不重启。你可以使用以下命令：

```shell
docker run -d --name my-web-server -p 80:80 --restart unless-stopped my-web-server-image
```
在此示例中，名为 my-web-server 的 web 服务器容器将自动重新启动，除非您手动停止它。

- 切换模型，我需要重新输入提示吗？

是的，因为切换模型会重置历史记录，所以您需要重新输入提示。

- PASS_HISTORY 的适当值是什么？

PASS_HISTORY的数量严格等于对话历史中的消息数量。推荐值是2，因为系统提示占用了一个消息计数。如果设置为0，PASS_HISTORY将自动重置为2，以确保对话正常进行。当PASS_HISTORY小于或等于2时，机器人的行为可以被视为只记住当前对话，即一个问题和一个答案，并且下次不会记住之前的问答内容。PASS_HISTORY的最大值没有限制，但请注意，对话历史中的消息越多，每次对话的成本就越高。当未设置PASS_HISTORY时，默认值为9999，表示对话历史中的消息数量为9999。

- 机器人令牌可以有多个令牌吗？

不，将来它会支持多个机器人令牌。

- 如何使用机器人命令？

1. `/info`: 机器人 `/info` 命令可以查看机器人的配置信息，包括当前使用的模型、API URL、API 密钥等。它还可以更改机器人的显示语言、偏好设置和插件设置。

2. `/start`: 机器人 `/start` 命令可以查看机器人的使用说明、使用方法和功能介绍。您可以使用 `/start` 命令设置 API 密钥。如果您有官方的 OpenAI API 密钥，请使用以下命令：`/start your_api_key`。如果您使用的是第三方 API 密钥，请使用以下命令：`/start https://your_api_url your_api_key`。

3. `/reset`: 机器人 `/reset` 命令可以清除机器人的对话消息，并强制机器人停止生成回复。如果你想重置系统提示，请使用以下命令：`/reset your_system_prompt`。但是，`/reset` 命令永远不会恢复机器人的显示语言、偏好设置、插件设置、使用中的模型、API URL、API 密钥、系统提示等。

4. `/model`: 机器人的 `/model` 命令允许你快速切换AI模型，无需通过 `/info` 菜单。只需使用 `/model model_name` 即可切换到特定模型。例如：`/model gpt-5` 切换到GPT-5或 `/model claude-3-opus` 切换到Claude 3 Opus。这个命令提供了在对话过程中更快捷的模型切换方式。

- 如果 Koyeb 部署失败怎么办？

Koyeb 的免费服务可能有点不稳定，所以部署失败是很常见的。你可以尝试重新部署，如果还是不行的话，考虑换到另一个平台。😊

- 为什么我使用 CUSTOM_MODELS 删除默认模型名称后，再使用 /info 命令检查时它又重新出现了？

如果你使用 `docker-compose.yml` 部署，不要在 `CUSTOM_MODELS` 的值周围添加引号。错误用法：`CUSTOM_MODELS="gpt-5,-gpt-3.5"`，否则会导致环境变量解析错误，导致默认模型名称再次出现。错误的方式会被解析为删除 `gpt-3.5"` 模型，这将导致默认模型名称 `gpt-3.5` 未被删除。正确的写法是：`CUSTOM_MODELS=gpt-5,-gpt-3.5`。

对于模型组也是如此。错误写法：`CUSTOM_MODELS="GPT:gpt-5;Claude:claude-3-opus"`。正确写法：`CUSTOM_MODELS=GPT:gpt-5;Claude:claude-3-opus`。如果你的组名或模型名包含特殊字符，请注意正确转义。

## 参考文献

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息使用的markdown渲染是我的另一个[项目](https://github.com/yym68686/md2tgmd)。

duckduckgo AI: https://github.com/mrgick/duck_chat

## 赞助商

我们感谢以下赞助商的支持：
<!-- $300+$380+¥1200+¥300+$30+$25+$20+¥50 -->
- @fasizhuanqian: 300 USDT

- @ZETA: $380

- @yuerbujin: ¥1200

- @RR5AM: ¥300

- @IKUNONHK: 30 USDT

- @miya0v0: 30 USDT

- [@Zeabur](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss): $25

- @Bill_ZKE: 20 USDT

- @wagon_look：¥50

<!-- [![Deployed on Zeabur](https://zeabur.com/deployed-on-zeabur-dark.svg)](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss) -->

## 如何赞助我们

如果您想支持我们的项目，您可以通过以下方式赞助我们：

1. [PayPal](https://www.paypal.me/yym68686)

2. [USDT-TRC20](https://pb.yym68686.top/~USDT-TRC20)，USDT-TRC20 钱包地址：`TLFbqSv5pDu5he43mVmK1dNx7yBMFeN7d8`

3. [微信](https://pb.yym68686.top/~wechat)

4. [支付宝](https://pb.yym68686.top/~alipay)

感谢您的支持！

## 星星历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="星历史图表" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>

## 许可证

本项目根据 GPLv3 许可证授权，这意味着您可以自由复制、分发和修改该软件，只要所有修改和衍生作品也以相同的许可证发布。
