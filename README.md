<p align="center">
<img src="./assets/logo-3071751.jpg">
</p>

# 🤖️ ChatGPT Telegram Bot

<p align="center">
    <a href="https://hub.docker.com/repository/docker/yym68686/chatgpt">
    <img src="https://img.shields.io/docker/pulls/yym68686/chatgpt?color=blue" alt="docker pull"></a>
  <a href="https://t.me/+_01cz9tAkUc1YzZl">
    <img src="https://img.shields.io/badge/Join Telegram Group-blue?&logo=telegram">
  </a>
</p>

The ChatGPT Telegram Bot is a powerful Telegram bot that utilizes the latest GPT models, including GPT3.5, GPT4, GPT4 Turbo, GPT4 Vision, DALLE 3, and the official Claude2.1 API. It enables users to engage in efficient conversations and information searches on Telegram.

## ✨ Features

- **Multiple AI Models**: Integrates a variety of AI models including GPT3.5, GPT4, GPT4 Turbo, GPT4 Vision, DALLE 3, and Claude2.1 API.
- **Powerful Online Search**: Supports online search with DuckDuckGo and Google, providing users with a robust information retrieval tool.
- **User-friendly Interface**: Allows flexible model switching within the chat window and supports streaming output for a typewriter-like effect.
- **Efficient Message Processing**: Asynchronously processes messages, answers questions in a multi-threaded manner, supports isolated dialogues, and provides unique dialogues for different users.
- **Document Interaction**: Supports Q&A for PDF and TXT documents. Users can upload files directly in the chat box for use.
- **Accurate Markdown Rendering**: Supports precise Markdown rendering of messages, utilizing another [project](https://github.com/yym68686/md2tgmd) of mine.
- **Convenient Deployment**: Supports one-click Zeabur, Replit deployment with true zero cost and idiot-proof deployment process. It also supports kuma anti-sleep, as well as Docker and fly.io deployment.

## 🍃 Environment variables

| Variable Name           | Comment                                                      | required? |
| ---------------------- | ------------------------------------------------------------ | ---------------------- |
| **BOT_TOKEN** | Telegram bot token. Create a bot on [BotFather](https://t.me/BotFather) to get the BOT_TOKEN. | **Yes** |
| **API**       | OpenAI or third-party API key.                              | **Yes** |
| GPT_ENGINE    | Set the default QA model; the default is:`gpt-4-1106-preview`. This item can be freely switched using the bot's "info" command, and it doesn't need to be set in principle. | No |
| WEB_HOOK  | Whenever the telegram bot receives a user message, the message will be passed to WEB_HOOK, where the bot will listen to it and process the received messages in a timely manner. | No |
| API_URL       | If you are using the OpenAI official API, you don't need to set this. If you using a third-party API, you need to fill in the third-party proxy website. The default is: https://api.openai.com/v1/chat/completions | No |
| NICK          | The default is empty, and NICK is the name of the bot. The bot will only respond when the message starts with NICK that the user inputs, otherwise the bot will respond to any message. Especially in group chats, if there is no NICK, the bot will reply to all messages. | No |
| PASS_HISTORY  | The default is `False`. The bot remembers the conversation history and considers the context when replying next time. If set to `False`, the bot will forget the conversation history and only consider the current conversation. Ensure the first letter of `False` and `True` is capitalized. | No |
| GOOGLE_API_KEY | If you need to use Google search, you need to set it. If you do not set this environment variable, the bot will default to provide duckduckgo search. Create credentials in Google Cloud's [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) and the API Key will be GOOGLE_API_KEY on the credentials page. Google search can be queried 100 times a day, which is completely sufficient for light use. When the usage limit has been reached, the bot will automatically turn off Google search. | No |
| GOOGLE_CSE_ID | If you need to use Google search, you need to set it together with GOOGLE_API_KEY. Create a search engine in [Programmable Search Engine](https://programmablesearchengine.google.com/), where the search engine ID is the value of GOOGLE_CSE_ID. | No |
| whitelist     | Set which users can access the bot, and connect the user IDs authorized to use the bot with ','. The default value is `None`, which means that the bot is open to everyone. You can obtain your own Telegram ID and group ID through this [bot](https://t.me/getidsbot). Please note that here we are referring to the Telegram ID, not the Telegram username, as they are different. The whitelist cannot contain group IDs, to authorize specific groups for use, the environment variable GROUP_LIST must be used. | No |
| ADMIN_LIST | Set up an admin list. Only admins can use the `info` command to configure the bot. When `GROUP_LIST` is set, only admins can have private chats with the bot. If `ADMIN_LIST` is not set, all users can modify the basic settings of the bot through the `info` command by default. Connect the admin IDs with a comma (','). You can obtain your own Telegram ID and group ID through this [bot](https://t.me/getidsbot). | No |
| GROUP_LIST | Set up a list of groups that can use the bot. Connect the group IDs with a comma (','). After setting `GROUP_LIST`, except for the admin, no one else can have a private chat with the bot.You can obtain your own Telegram ID and group ID through this [bot](https://t.me/getidsbot). | No |

## 🔌 Plugins

Our plugin system has been successfully developed and is now fully operational. We welcome everyone to contribute their code to enrich our plugin library. All plugins can be activated or deactivated using the `/info` command. The following plugins are currently supported:

- **Web Search**: By default, DuckDuckGo search is provided. Google search is automatically activated when the `GOOGLE_CSE_ID` and `GOOGLE_API_KEY` environment variables are set.
- **Time Retrieval**: Retrieves the current time, date, and day of the week in the GMT+8 time zone.
- **URL Summary**: Automatically extracts URLs from queries and responds based on the content of the URLs.
- **Version Information**: Displays the current version of the bot, commit hash, update time, and developer name.

To develop plugins, please follow the steps outlined below:

- Initially, you need to add the environment variable for the plugin in the `config.PLUGINS` dictionary located in the `config.py` file. The value can be customized to be either enabled or disabled by default. It is advisable to use uppercase letters for the entire environment variable.
- Subsequently, append the function's name and description in the `utils/function_call.py` file.
- Then, enhance the `ask_stream` function in the `utils/chatgpt2api.py` file with the function's processing logic. You can refer to the existing examples within the `ask_stream` method for guidance on how to write it.
- Following that, write the function, as mentioned in the `utils/function_call.py` file, in the `utils/plugins.py` file.
- Next, in the `bot.py` file, augment the `update_first_buttons_message` function with buttons, enabling users to freely toggle plugins using the `info` command.
- Lastly, don't forget to add the plugin's description in the plugins section of the README.

Please note that the above steps are a general guide and may need to be adjusted based on the specific requirements of your plugin.

## Zeabur Remote Deployment (Recommended)

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

One-Click Restart Docker Image

```bash
set -eu
docker rm -f chatbot
docker pull yym68686/chatgpt:1.0
docker run -p 8080:8080 -dit --name chatbot \
-e BOT_TOKEN= \
-e API= \
-e API_URL= \
-e GOOGLE_API_KEY= \
-e GOOGLE_CSE_ID= \
-e claude_api_key= \
yym68686/chatgpt:1.0
docker logs -f chatbot
```

This script is for restarting the Docker image with a single command. It first removes the existing Docker container named "chatbot" if it exists. Then, it runs a new Docker container with the name "chatbot", exposing port 8080 and setting various environment variables. The Docker image used is "yym68686/chatgpt:1.0". Finally, it follows the logs of the "chatbot" container.

## 📄 Q & A

- Why can't I use Google search?

By default, DuckDuckGo search is provided. The official API for Google search needs to be applied for by the user. It can provide real-time information that GPT could not answer before, such as today's trending topics on Weibo, today's weather in a specific location, and the progress of a certain person or news event.

- How do I switch models?

You can switch between GPT3.5, GPT4, and other models using the "info" command in the chat window.

- Does it support a vector database?

No, previous versions did support it, but after installing unstructured[md,pdf] dependencies for parsing PDFs, the docker image size reached 9GB, so the support for the vector database was removed in the current version. Since the vector database is just a transitional product when the context of large language models is relatively short and there is significant information loss. With the introduction of claude2.1 200k and gpt4 Turbo 128k, vector databases have become less and less important. Although their price is lower, by comparison, I would prefer better performance.

- Can it be deployed in a group?

Yes, it supports whitelisting to prevent abuse and information leakage.

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

<!-- - What is gpt4free in the `/info` command? Do I need to enable it?

gpt4free is an open-source project that reverse-engineers multiple platforms to use models like gpt4/gpt3 for free. As it's a free API, it may be unstable, so please use it with caution. If you have your own API, it is recommended to use that as a priority.

You can enable gpt4free by simply clicking on it in the `/info` command. Please note that gpt4free does not support all models. You can check the gpt4free documentation to see which models it supports. Once gpt4free is enabled, all questions and searches will use the gpt4free API. If you encounter any errors, please copy the robot's backend log to @yym68686, or open an issue on GitHub. Our developers will resolve it as soon as possible. -->

- After setting the `NICK`, there's no response when I @ the bot, and it only replies when the message starts with the nick. How can I make it respond to both the nick and @botname?

In a group chat scenario, if the environment variable `NICK` is not set, the bot will receive all group messages and respond to all of them. Therefore, it is necessary to set `NICK`. After setting `NICK`, the bot will only respond to messages that start with `NICK`. So, if you want to @ the bot to get a response, you just need to set NICK to @botname. This way, when you @ the bot in the group, the bot will detect that the message starts with @botname, and it will respond to the message.

- How many messages will the history keep?

Apart from the latest `gpt-4-turbo-preview` model, the official context supports 128k tokens, but this project limits it to 16k tokens. All other models use the official context length settings, for example, the `gpt-3.5-turbo-16k` context is 16k, the `gpt-4-32k` context is 32k, and the `Claude2` context is 200k. This limitation is implemented to save user costs, as most scenarios do not require a high context. If you have specific needs, you can modify the context limits for each model in the `utils/chatgpt2api.py` file.

## References

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