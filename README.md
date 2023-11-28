# ChatGPT Telegram Bot

Join the [Telegram Group](https://t.me/+_01cz9tAkUc1YzZl) chat to share your user experience or report Bugs.

[English](./README.md) | [Simplified Chinese](./README.zh-CN.md) | [Traditional Chinese](./README.zh-TW.md)

## ✨ Features

✅ Supports GPT3.5 and GPT4/GPT4 Turbo API, DALLE 3

✅ Supports online search using duckduckgo and Google🔍. DuckDuckGo search is provided by default, and the official API for Google search needs to be applied by the user. It can provide real-time information that GPT could not answer before, such as Weibo hot search today, weather in a certain place today, and the progress of a certain person or news.

✅ Supports document QA based on the embedded vector database. In the search, for the searched PDF, automatic vector semantic search of PDF documents is performed, and pdf-related content is extracted based on the vector database. Supports using the "qa" command to vectorize the entire website with the "sitemap.xml" file, and answer questions based on the vector database, which is especially suitable for document websites and wiki websites of some projects.

✅ Supports switching between GPT3.5, GPT4 and other models through the "info" command in the chat window

✅ Asynchronously processes messages, multi-threadedly answers questions, supports isolated dialogues, and different users have different dialogues

✅ Supports accurate Markdown rendering of messages, using another [project](https://github.com/yym68686/md2tgmd) of mine

✅ Supports streaming output, achieving typewriter effect

✅ Supports whitelisting to prevent abuse and information leakage

✅ Cross-platform, breaking knowledge barriers anytime and anywhere with Telegram

✅ Supports one-click Zeabur, Replit deployment, true zero cost, idiotic deployment, and supports kuma anti-sleep. Also supports Docker, fly.io deployment

## Environment variables

| Variable Name           | Comment                                                      |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (required)** | Telegram bot token. Create a bot on [BotFather](https://t.me/BotFather) to get the BOT_TOKEN. |
| **API (required)**       | OpenAI or third-party API key.                              |
| WEB_HOOK (optional)  | Whenever the telegram bot receives a user message, the message will be passed to WEB_HOOK, where the bot will listen to it and process the received messages in a timely manner. |
| API_URL(optional)       | If you are using the OpenAI official API, you don't need to set this. If you using a third-party API, you need to fill in the third-party proxy website. The default is: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (optional)    | Set the default QA model; the default is:`gpt-3.5-turbo`. This item can be freely switched using the bot's "info" command, and it doesn't need to be set in principle. |
| NICK (optional)          | The default is empty, and NICK is the name of the bot. The bot will only respond when the message starts with NICK that the user inputs, otherwise the bot will respond to any message. Especially in group chats, if there is no NICK, the bot will reply to all messages. |
| PASS_HISTORY (optional)  | The default is true. The bot remembers the conversation history and considers the context when replying next time. If set to false, the bot will forget the conversation history and only consider the current conversation. |
| GOOGLE_API_KEY (optional)| If you need to use Google search, you need to set it. If you do not set this environment variable, the bot will default to provide duckduckgo search. Create credentials in Google Cloud's [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) and the API Key will be GOOGLE_API_KEY on the credentials page. Google search can be queried 100 times a day, which is completely sufficient for light use. When the usage limit has been reached, the bot will automatically turn off Google search. |
| GOOGLE_CSE_ID (optional) | If you need to use Google search, you need to set it together with GOOGLE_API_KEY. Create a search engine in [Programmable Search Engine](https://programmablesearchengine.google.com/), where the search engine ID is the value of GOOGLE_CSE_ID. |
| whitelist (optional)     | Set which users can access the bot, and connect the user IDs authorized to use the bot with ','. The default value is `None`, which means that the bot is open to everyone. |

## Zeabur Remote Deployment (Recommended)

One-click deployment:

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

If you need follow-up function updates, the following deployment method is recommended:

Fork this repository first, then register for [Zeabur](https://zeabur.com). The free quota is sufficient for light use. Import from your own Github repository, set the domain name (which must be consistent with WEB_HOOK) and environment variables, and redeploy. If you need function updates in the follow-up, just synchronize this repository in your own repository and redeploy in Zeabur to get the latest functions.

## Replit Remote Deployment

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

After importing the Github repository, set the running command

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

Select Secrets in the Tools sidebar, add the environment variables required by the bot, where:

- WEB_HOOK: Replit will automatically assign a domain name to you, fill in `https://appname.username.repl.co`
- Remember to open "Always On"

Click the run button on the top of the screen to run the bot.

## fly.io Remote Deployment

Official documentation: https://fly.io/docs/

Use Docker image to deploy fly.io application

```bash
flyctl launch --image yym68686/chatgpt:1.0
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
    -e BOT_TOKEN="telegram bot token" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

Or if you want to use Docker Compose, here is a docker-compose.yml example:

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:1.0
    environment:
      - BOT_TOKEN=
      - API=
      - API_URL=
    ports:
      - 80:8080
```

Run Docker Compose container in the background

```bash
docker-compose up -d
```

Package the Docker image in the repository and upload it to Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## Reference

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

The markdown rendering of the message used is another [project](https://github.com/yym68686/md2tgmd) of mine.

## Star History

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>

## Sponsor

[![Deployed on Zeabur](https://zeabur.com/deployed-on-zeabur-dark.svg)](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss)

## License

This project is licensed under GPLv3, which means you are free to copy, distribute, and modify the software, as long as all modifications and derivative works are also released under the same license.