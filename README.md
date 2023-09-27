# ChatGPT Telegram Bot

Join the [Telegram Group](https://t.me/+_01cz9tAkUc1YzZl) chat to share your user experience or report Bugs.

## ✨ Features

✅ Supports ChatGPT and GPT4 API

✅ Supports duckduckgo, Google network search🔍. The default search is duckduckgo. Google search requires application of the official API separately. It can answer real-time information that gpt couldn't answer before, such as today's hot Weibo, the weather in a certain place today, the progress of a certain person or news.

✅ Supports document question answering based on embedding vector database. In searching, for the searched PDF, it can automatically perform vector semantic search on the PDF document, and extract the relevant content of PDF based on the vector database. It supports using the qa command to vectorize the entire website with the sitemap.xml file and answer questions based on the vector database. It is especially suitable for some project document websites, wiki websites.

✅ Supports switching freely between models such as gpt3.5, gpt4, etc. using the info command in the chat box by clicking the button.

✅ Asynchronous processing of messages, answering questions in multiple threads, supporting conversation isolation, different users have different conversations

✅ Supports accurate message Markdown rendering, using my another [project](https://github.com/yym68686/md2tgmd)

✅ Supports streaming output, achieving typewriter effect

✅ Supports whitelist to prevent abuse and information leakage

✅ Cross-platform, breaking knowledge barriers anytime, anywhere with Telegram

✅ Supports one-click Zeabur, Replit deployment, zero cost, fool-style deployment, and kuma anti-sleepy. Supports Docker, fly.io deployment

## Environmental Variables

| Variable Name          | Remarks                                                                                                                   |
| ----------------------| --------------------------------------------------------------------------------------------------------------------------|
| **BOT_TOKEN(required)**| Telegram bot token, create a bot at [BotFather](https://t.me/BotFather) to obtain the bot token                            |
| **WEB_HOOK(required)** | Telegram bot forwards the message received from the user to WEB_HOOK, and the bot listens here and processes the message |
| **API(required)**      | OpenAI or third-party API key                                                                                              |
| API_URL(optional)      | If you use OpenAI official API, you do not need to set this item. If you use third-party API, you need to fill in the third-party proxy website. The default value is: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE(optional)   | Sets the default question-answering model. The default is:`gpt-3.5-turbo`, this item can be freely switched using the robot info command, and does not need to be set in principle. |
| NICK(optional)         | The default is empty. NICK is the name of the bot. When the user enters the message starting with NICK, the bot will answer. Otherwise, the bot will answer any message. Especially in group chats, if there is no NICK, the bot will reply to all messages. |
| PASS_HISTORY(optional) | The default is true, which means that the bot will remember the conversation history and consider the context when replying next time. If set to false, the bot will forget the conversation history and only consider the current conversation. |
| GOOGLE_API_KEY(optional)| If you need Google search, you need to set it. If this environment variable is not set, the bot will default to providing duckduckgo search. Create credentials in the [API and Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) of Google Cloud, and the API Key on the credentials page is GOOGLE_API_KEY. Google search can query 100 times a day, which is completely sufficient for light use. If the limit is reached, the bot will automatically close the Google search. |
| GOOGLE_CSE_ID(optional)| If you need Google search, you need to set it together with GOOGLE_API_KEY. Create a search engine in the [Programmable Search Engine](https://programmablesearchengine.google.com/), where the search engine ID is the value of GOOGLE_CSE_ID. |
| whitelist(optional)    | Set which users can access the bot. Connect the user ID authorized to use the bot with `,`. The default value is `None`, which means that the bot is open to everyone. |

## Zeabur Remote Deployment (Recommended)

One-click deployment:

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

If subsequent functional updates are required, the following deployment method is recommended:

First fork this repository, then register [Zeabur](https://zeabur.com), the free quota is sufficient for light use. Import from your own Github repository, set the domain name (must be consistent with WEB_HOOK) and environment variables, and then redeploy. The latest functions can be obtained by synchronizing this repository in your own repository and redeploying on Zeabur.

## Replit Remote Deployment

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

After importing the Github repository, set the running command

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

Select Secrets in the Tools in the left sidebar and add the environment variables required by the bot, among which:

- WEB_HOOK: Replit will automatically assign a domain name to you, fill in `https://appname.username.repl.co`

Click run above the screen to start the bot. Remember to turn on Always On.

## fly.io Remote Deployment

Official documentation: https://fly.io/docs/

Deploy fly.io application using Docker image

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

Enter the name of the application. If prompted to initialize Postgresql or Redis, choose No.

Deploy according to the prompts. A secondary domain name will be provided in the official website control panel, which can be used to access the service using this secondary domain name.

Set environment variables

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
flyctl secrets set COOKIES=
# Optional
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

SSH to fly.io container

```bash
# Generate keys
flyctl ssh issue --agent
# ssh connection
flyctl ssh establish
```

Check if the webhook url is correct

```
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker Local Deployment

Start the container

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

Or if you want to use Docker Compose, here is an example docker-compose.yml:

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

Run Docker Compose container in the background

```bash
docker-compose up -d
```

Repository package Docker image and push it to Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## Reference

Reference projects:

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

The markdown rendering of messages uses my another project: https://github.com/yym68686/md2tgmd

## Star History

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>