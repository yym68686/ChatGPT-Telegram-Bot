<p align="center">
<img src="./assets/logo-3071751.jpg">
</p>

# 🤖️ ChatGPT Telegram Bot

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

The ChatGPT Telegram Bot is a powerful Telegram bot that utilizes the latest GPT models, including GPT-3.5/4/4 Turbo/4o, DALL·E 3, Groq Mixtral-8x7b/LLaMA2-70b, Gemini 1.5 Pro/Flash and the official Claude2.1/3/3.5 API. It enables users to engage in efficient conversations and information searches on Telegram.

## ✨ Features

- **Multiple AI Models**: Supports GPT-3.5/4/4 Turbo/4o, DALL·E 3, Groq Mixtral-8x7b/LLaMA2-70b, Gemini 1.5 Pro/Flash and the official Claude2.1/3/3.5 API. Also supports one-api/new-api. Utilizes a self-developed API request backend [SDK](https://github.com/yym68686/ModelMerge), independent of the OpenAI SDK.
- **Multi-modal Q&A**: Supports Q&A for voice, images and PDF/TXT/MD/python documents. Users can upload files directly in the chat box for use.
- **Group Chat Topic Mode**: Supports enabling topic mode in group chats, isolating APIs, dialogue history, plugin configurations, and preferences between topics.
- **Rich Plugin System**: Supports web search(DuckDuckGo and Google), URL summarization, arXiv paper summarization, and code interpreter.
- **User-friendly Interface**: Allows flexible model switching within the chat window and supports streaming output for a typewriter-like effect.
- **Efficient Message Processing**: Asynchronously processes messages, answers questions in a multi-threaded manner, supports isolated dialogues, and provides unique dialogues for different users.
- **Long Text Message Handling**: Automatically merges long text messages, breaking through Telegram's single message length limit. When the bot's response exceeds the Telegram limit, it will be split into multiple messages.
- **Multi-user Dialogue Isolation**: Supports dialogue isolation and configuration isolation, allowing selection between multi-user and single-user modes.
- **Question Prediction**: Automatically generates follow-up questions, anticipating what users might ask next.
- **Multi-language Interface**: Supports Simplified Chinese, Traditional Chinese, Russian and English interfaces.
- **Whitelist, Blacklist, and Admin Settings**: Supports setting up whitelists, blacklists, and administrators.
- **Inline Mode**: Allows users to @ the bot in any chat window to generate answers without needing to ask questions in the bot's chat window.
- **User-friendly Interface**: Allows flexible model switching within the chat window and supports streaming output for a typewriter-like effect.Supports precise Markdown rendering of messages, utilizing another [project](https://github.com/yym68686/md2tgmd) of mine.
- **Convenient Deployment**: Supports one-click koyeb, Zeabur, Replit deployment with true zero cost and idiot-proof deployment process. It also supports kuma anti-sleep, as well as Docker and fly.io deployment.

## 🍃 Environment variables

The following is a list of environment variables related to the bot's core settings:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| BOT_TOKEN | Telegram bot token. Create a bot on [BotFather](https://t.me/BotFather) to get the BOT_TOKEN. | **Yes** |
| API | OpenAI or third-party API key. | No |
| GPT_ENGINE | Set the default QA model; the default is:`gpt-4o`. This item can be freely switched using the bot's "info" command, and it doesn't need to be set in principle. | No |
| WEB_HOOK | Whenever the telegram bot receives a user message, the message will be passed to WEB_HOOK, where the bot will listen to it and process the received messages in a timely manner. | No |
| API_URL | If you are using the OpenAI official API, you don't need to set this. If you using a third-party API, you need to fill in the third-party proxy website. The default is: https://api.openai.com/v1/chat/completions | No |
| GROQ_API_KEY | Groq official API key. | No |
| GOOGLE_AI_API_KEY | Google AI official API key. | No |
| claude_api_key | Claude official API key. | No |
| CLAUDE_API_URL | If you are using the Anthropic official API, you don't need to set this. If you using a third-party Anthropic API, you need to fill in the third-party proxy website. The default is: https://api.anthropic.com/v1/messages | No |
| NICK | The default is empty, and NICK is the name of the bot. The bot will only respond when the message starts with NICK that the user inputs, otherwise the bot will respond to any message. Especially in group chats, if there is no NICK, the bot will reply to all messages. | No |
| GOOGLE_API_KEY | If you need to use Google search, you need to set it. If you do not set this environment variable, the bot will default to provide duckduckgo search. | No |
| GOOGLE_CSE_ID | If you need to use Google search, you need to set it together with GOOGLE_API_KEY. | No |
| whitelist | Set which users can access the bot, and connect the user IDs authorized to use the bot with ','. The default value is `None`, which means that the bot is open to everyone. | No |
| ADMIN_LIST | Set up an admin list. Only admins can use the `/info` command to configure the bot. | No |
| GROUP_LIST | Set up a list of groups that can use the bot. Connect the group IDs with a comma (','). Even if group members are not on the whitelist, as long as the group ID is in the GROUP_LIST, all members of the group can use the bot. | No |
| CUSTOM_MODELS | Set up a list of custom model names. Connect the model names with a comma (','). If you need to delete the default model, add a hyphen(-) before the default model name. | No |
| CHAT_MODE | Introduce multi-user mode, different users' configurations are not shared. When CHAT_MODE is global, all users share the configuration. When CHAT_MODE is multiusers, user configurations are independent of each other. | No |
| temperature | Specify the temperature for the LLM. Default is `0.5`. | No |
| GET_MODELS | Specify whether to get supported models via API. Default is `False`. | No |
| SYSTEMPROMPT | Specify the system prompt. Default is `None`. | No |

The following is a list of environment variables related to the bot's preference settings:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| PASS_HISTORY | The default is `False`. The bot remembers the conversation history and considers the context when replying next time. If set to `False`, the bot will forget the conversation history and only consider the current conversation. Ensure the first letter of `False` and `True` is capitalized. | No |
| LONG_TEXT | If the user's input exceeds the Telegram limit and is split into multiple messages sent consecutively in a very short time, the bot will treat these multiple messages as one. Default is `True`. | No |
| LONG_TEXT_SPLIT | When the bot's response exceeds the Telegram limit, it will be split into multiple messages. Default is `True`. | No |
| FILE_UPLOAD_MESS | When the file or image is uploaded and the robot has finished processing, the robot will send a message indicating a successful upload. Default is `True`. | No |
| FOLLOW_UP | Automatically generate several related questions for the user to choose from. Default is `False`. | No |
| TITLE | Whether to display the model name at the beginning of the bot's reply. Default is `False`. | No |
| TYPING | Whether to display "typing" status when the bot is replying. Default is `False`. | No |
| REPLY | Whether the bot's reply should be in "reply" format to the user's message. Default is `False`. | No |

The following is a list of environment variables related to the bot's plugin settings:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| SEARCH | Whether to enable the search plugin. Default is `True`. | No |
| URL | Whether to enable the URL summarization plugin. Default is `True`. | No |
| ARXIV | Whether to enable the arXiv paper summarization plugin. Default is `True`. | No |
| CODE | Whether to enable the code interpreter plugin. Default is `False`. | No |
| IMAGE | Whether to enable the image generation plugin. Default is `False`. | No |
| DATE | Whether to enable the date plugin. Default is `False`. | No |


## Koyeb Remote Deployment

One-click deployment:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=docker&image=docker.io/yym68686/chatgpt:latest&name=chatbot)

## Zeabur Remote Deployment

One-click deployment:

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

If you need follow-up function updates, the following deployment method is recommended:

- Fork this repository first, then register for [Zeabur](https://zeabur.com). Currently, Zeabur does not support free Docker container deployment. If you need to use Zeabur to deploy the bot for this project, you will need to upgrade to the Developer Plan. Fortunately, Zeabur has introduced their [sponsorship program](https://zeabur.com/docs/billing/sponsor), which offers a one-month Developer Plan to all contributors of this project. If you have features you'd like to enhance, feel free to submit pull requests to this project.
- Import from your own Github repository.
- Set the required environment variables, and redeploy.
- If you need function updates in the follow-up, just synchronize this repository in your own repository and redeploy in Zeabur to get the latest functions.

## Replit Remote Deployment

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

After importing the Github repository, set the running command

```bash
pip install -r requirements.txt > /dev/null && python3 bot.py
```

Select Secrets in the Tools sidebar, add the environment variables required by the bot, where:

- WEB_HOOK: Replit will automatically assign a domain name to you, fill in `https://appname.username.repl.co`
- Remember to open "Always On"

Click the run button on the top of the screen to run the bot.

## fly.io Remote Deployment

Official documentation: https://fly.io/docs/

Use Docker image to deploy fly.io application

```bash
flyctl launch --image yym68686/chatgpt:latest
```

Enter the name of the application when prompted, and select No for initializing Postgresql or Redis.

Follow the prompts to deploy. A secondary domain name will be provided in the official control panel, which can be used to access the service.

Set environment variables

```bash
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# optional
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set NICK=javis
```

View all environment variables

```bash
flyctl secrets list
```

Remove environment variables

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh to fly.io container

```bash
flyctl ssh issue --agent
# ssh connection
flyctl ssh establish
```

Check whether the webhook URL is correct

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker Local Deployment

Start the container

```bash
docker run -p 80:8080 --name chatbot -dit \
    -e BOT_TOKEN=your_telegram_bot_token \
    -e API= \
    -e API_URL= \
    yym68686/chatgpt:latest
```

Or if you want to use Docker Compose, here is a docker-compose.yml example:

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
    ports:
      - 80:8080
```

Run Docker Compose container in the background

```bash
docker-compose pull
docker-compose up -d

# uni-api
docker-compose -f docker-compose-uni-api.yml up -d
```

Package the Docker image in the repository and upload it to Docker Hub

```bash
docker build --no-cache -t chatgpt:latest -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:latest yym68686/chatgpt:latest
docker push yym68686/chatgpt:latest
```

One-Click Restart Docker Image

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
yym68686/chatgpt:latest
docker logs -f chatbot
```

This script is for restarting the Docker image with a single command. It first removes the existing Docker container named "chatbot" if it exists. Then, it runs a new Docker container with the name "chatbot", exposing port 8080 and setting various environment variables. The Docker image used is "yym68686/chatgpt:latest". Finally, it follows the logs of the "chatbot" container.

## 📄 Q & A

- Why can't I use Google search?

By default, DuckDuckGo search is provided. The official API for Google search needs to be applied for by the user. It can provide real-time information that GPT could not answer before, such as today's trending topics on Weibo, today's weather in a specific location, and the progress of a certain person or news event.

- How do I switch models?

You can switch between GPT3.5/4/4o, and other models using the "/info" command in the chat window.

- Can it be deployed in a group?

Yes, it supports whitelist to prevent abuse and information leakage.

- Why can't the bot talk when I add it to the group?

If this is the first time you add the bot to a group chat, you need to set the group privacy to disable in botfather, then remove the bot from the group chat and re-add it to use it normally.

The second method is to set the bot as an administrator, so the bot can be used normally. However, if you want to add the bot to a group chat where you are not an administrator, the first method is more suitable.

Another possibility is that the GROUP_LIST set is not the current group chat ID. Please check if GROUP_LIST is set; GROUP_LIST is the group ID, not the group name. The group ID starts with a minus sign followed by a string of numbers.

- How do the settings of GROUP_LIST, ADMIN_LIST, and whitelist affect the behavior of the bot?

If whitelist is not set, everyone can use the bot. If whitelist is set, only users in the whitelist can use the bot. If GROUP_LIST is set, only groups in the GROUP_LIST can use the bot. If both whitelist and GROUP_LIST are set, everyone in the group can use the bot, but only users in the whitelist can privately chat with the bot. If ADMIN_LIST is set, only users in the ADMIN_LIST can use the /info command to change the bot's settings. If ADMIN_LIST is not set, everyone can use the /info command to change the bot's configuration.

- How should I set the API_URL?

The API_URL supports all suffixes, including: https://api.openai.com/v1/chat/completions, https://api.openai.com/v1, and https://api.openai.com/. The bot will automatically allocate different endpoints based on different uses.

- Is it necessary to configure the web_hook environment variable?

The web_hook is not a mandatory environment variable. You only need to set the domain name (which must be consistent with WEB_HOOK) and other environment variables as required for your application's functionality.

- I deployed a robot with docker compose. If the documentation is placed on the server locally, which directory should it be mounted to in order to take effect? Do I need to set additional configurations and modify the code?

You can directly send the documentation to the robot through the chat box, and the robot will automatically parse the documentation. To use the documentation dialogue function, you need to enable the historical conversation feature. There is no need for additional processing of the documentation.

- I still can't get it to work... I want to use it in a group, I've set the ADMIN_LIST to myself, and the GROUP_LIST to that group, with the whitelist left empty. However, only I can use it in that group, other members in the group are prompted with no permission, what's going on?

Here's a troubleshooting guide: Please carefully check if the GROUP_LIST is correct. The ID of a Telegram group starts with a negative sign followed by a series of numbers. If it's not, please use this bot [bot](https://t.me/getidsbot) to reacquire the group ID.

- I've uploaded a document, but it's not responding based on the content of the document. What's going on?

To use the document question and answer feature, you must first enable the history record. You can turn on the history record through the `/info` command, or by setting the environment variable `PASS_HISTORY` to `True` to enable the history record by default. Please note that enabling the history record will incur additional costs, so this project does not enable the history record by default. This means that the question and answer feature cannot be used under the default settings. Before using this feature, you need to manually enable the history record.

- After setting the `NICK`, there's no response when I @ the bot, and it only replies when the message starts with the nick. How can I make it respond to both the nick and @botname?

In a group chat scenario, if the environment variable `NICK` is not set, the bot will receive all group messages and respond to all of them. Therefore, it is necessary to set `NICK`. After setting `NICK`, the bot will only respond to messages that start with `NICK`. So, if you want to @ the bot to get a response, you just need to set NICK to @botname. This way, when you @ the bot in the group, the bot will detect that the message starts with @botname, and it will respond to the message.

- How many messages will the history keep?

All other models use the official context length settings, for example, the `gpt-3.5-turbo-16k` context is 16k, the `gpt-4o` context is 128k, and the `Claude3/3.5` context is 200k. This limitation is implemented to save user costs, as most scenarios do not require a high context.

- How to delete the default model name from the model list?

You can use the CUSTOM_MODELS environment variable to complete it. For example, if you want to add gpt-4o and remove the gpt-3.5 model from the model list, please set CUSTOM_MODELS to `gpt-4o,-gpt-3.5`.

- How does conversation isolation specifically work?

Conversations are always isolated based on different windows, not different users. This means that within the same group chat window, the same topic, and the same private chat window, it is considered the same conversation. CHAT_MODE only affects whether configurations are isolated. In multi-user mode, each user's plugin configurations, preferences, etc., are independent and do not affect each other. In single-user mode, all users share the same plugin configurations and preferences. However, conversation history is always isolated. Conversation isolation is to protect user privacy, ensuring that users' conversation history, plugin configurations, preferences, etc., are not visible to other users.

- Why hasn't the Docker image been updated for a long time?

The Docker image only stores the runtime environment of the program. Currently, the runtime environment of the program is stable, and the environment dependencies have hardly changed, so the Docker image has not been updated. Each time the Docker image is redeployed, it will pull the latest code, so there is no need to worry about the Docker image update issue.

- Why does the container report an error "http connect error or telegram.error.TimedOut: Timed out" after starting?

This issue is likely caused by the server deploying Docker being unable to connect to the Telegram server or the instability of the Telegram server.

1. In most cases, restarting the service, checking the server network environment, or waiting for the Telegram service to recover will suffice.
2. Additionally, you might try communicating with the Telegram server via web hook, which might solve the problem.

- How to make docker retry infinitely instead of stop at beginning?

The `--restart unless-stopped` parameter in Docker sets the container's restart policy. Specifically:

1. unless-stopped: This policy means that the container will automatically restart if it stops, except when it is manually stopped. In other words, if the container stops due to an error or system reboot, it will automatically restart. However, if you manually stop the container (e.g., using the docker stop command), it will not restart on its own.
This parameter is particularly useful for services that need to run continuously, as it ensures that the service will automatically recover from unexpected interruptions without requiring manual intervention.

2. Example: Suppose you have a Docker container running a web server, and you want it to restart automatically if it crashes or if the system reboots, but not if you manually stop it. You can use the following command:

```shell
docker run -d --name my-web-server -p 80:80 --restart unless-stopped my-web-server-image
```
In this example, the web server container named my-web-server will restart automatically unless you manually stop it.

- Switching models, do I need to re-enter the prompt?

Yes, because switching models will reset the history, so you need to re-enter the prompt.

- Can Bot tokens have multiple tokens?

No, in the future it will support multiple Bot Tokens.

- How to use robot commands?

1. `/info`: The robot `/info` command can view the robot's configuration information, including the current model in use, API URL, API key, etc. It can also change the robot's display language, preferences, and plugin settings.

2. `/start`: The robot `/start` command can view the robot's usage instructions, usage methods, and function introduction. You can set the API key using the `/start` command. If you have an official OpenAI API key, please use the following command: `/start your_api_key`. If you are using a third-party API key, please use the following command: `/start https://your_api_url your_api_key`.

3. `/reset`: The robot `/reset` command can clear the robot's conversation messages and force the robot to stop generating replies. If you want to reset the system prompt, please use the following command: `/reset your_system_prompt`. However, the `/reset` command will never restore the robot's display language, preferences, plugin settings, model in use, API URL, API key, system prompt, etc.

## References

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

The markdown rendering of the message used is another [project](https://github.com/yym68686/md2tgmd) of mine.

## Sponsors

We are grateful for the support from the following sponsors:
<!-- $300+$250+¥1200+¥300+$30+$25+$20+¥50 -->
- @fasizhuanqian: 300 USDT

- @ZETA: $250

- @yuerbujin: ¥1200

- @RR5AM: ¥300

- @IKUNONHK: 30 USDT

- [@Zeabur](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss): $25

- @Bill_ZKE: 20 USDT

- @wagon_look: ¥50

<!-- [![Deployed on Zeabur](https://zeabur.com/deployed-on-zeabur-dark.svg)](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss) -->

## How to Sponsor Us

If you would like to support our project, you can sponsor us through the following methods:

1. [PayPal](https://www.paypal.me/yym68686)

2. [USDT-TRC20](https://pb.yym68686.top/~USDT-TRC20), USDT-TRC20 Wallet Address: `TLFbqSv5pDu5he43mVmK1dNx7yBMFeN7d8`

3. [WeChat](https://pb.yym68686.top/~wechat)

4. [Alipay](https://pb.yym68686.top/~alipay)

Thank you for your support!

## Star History

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>

## License

This project is licensed under GPLv3, which means you are free to copy, distribute, and modify the software, as long as all modifications and derivative works are also released under the same license.
