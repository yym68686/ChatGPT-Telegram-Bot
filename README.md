<p align="center">
<img src="./assets/logo-3071751.jpg">
</p>

# 🤖️ TeleChat

[English](README.md) | [Chinese](README_CN.md)

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

ChatGPT Telegram Bot is a powerful Telegram bot that supports OpenAI-compatible large language model APIs. It enables users to have efficient conversations and information searches on Telegram. For support of other models from providers such as Anthropic, Gemini, Vertex AI, Azure, AWS, XAI, Cohere, Groq, Cloudflare, OpenRouter, etc., please use my other project, [uni-api](https://github.com/yym68686/uni-api), to integrate them. This helps reduce maintenance costs. Thank you for your understanding.

## ✨ Features

- **Multiple AI Models**: Supports APIs compatible with the OpenAI format. For other models from providers such as Anthropic, Gemini, Vertex AI, Azure, AWS, XAI, Cohere, Groq, Cloudflare, OpenRouter, etc., please integrate them using [uni-api](https://github.com/yym68686/uni-api). Also supports one-api/new-api. Utilizes self-developed API to request backend [SDK](https://github.com/yym68686/aient), does not rely on OpenAI SDK.
- **Multimodal Question Answering**: Supports question answering for voice, audio, images, and PDF/TXT/MD/python documents. Users can directly upload files in the chat box for use.
- **Model Grouping System**: Organize AI models into logical groups for easier selection. Models can be grouped by provider (GPT, Claude, etc.) or by capability. Models without an explicit group are automatically placed in an "OTHERS" group. This makes model selection more intuitive, especially when many models are available.
- **Group Chat Topic Mode**: Supports enabling topic mode in group chats, isolating APIs, dialogue history, plugin configurations, and preferences between topics.
- **Rich plugin system**: Supports web search (DuckDuckGo and Google), URL summarization, ArXiv paper summarization, and code interpreter.
- **User-friendly interface**: Allows flexible switching of models within the chat window and supports streaming output similar to a typewriter effect. Supports precise Markdown message rendering, utilizing another of my [projects](https://github.com/yym68686/md2tgmd).
- **Efficient Message Processing**: Asynchronously processes messages, answers questions in a multi-threaded manner, supports isolated dialogues, and provides unique dialogues for different users.
- **Long Text Message Handling**: Automatically merges long text messages, breaking through Telegram's single message length limit. When the bot's response exceeds the Telegram limit, it will be split into multiple messages.
- **Multi-user Dialogue Isolation**: Supports dialogue isolation and configuration isolation, allowing selection between multi-user and single-user modes.
- **Question Prediction**: Automatically generates follow-up questions, anticipating what users might ask next.
- **Multi-language Interface**: Supports Simplified Chinese, Traditional Chinese, Russian and English interfaces.
- **Whitelist, Blacklist, and Admin Settings**: Supports setting up whitelists, blacklists, and administrators.
- **Inline Mode**: Allows users to @ the bot in any chat window to generate answers without needing to ask questions in the bot's chat window.
- **Convenient Deployment**: Supports one-click koyeb, Zeabur, Replit deployment with true zero cost and idiot-proof deployment process. It also supports kuma anti-sleep, as well as Docker and fly.io deployment.

## 🍃 Environment variables

The following is a list of environment variables related to the bot's core settings:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| BOT_TOKEN | Telegram bot token. Create a bot on [BotFather](https://t.me/BotFather) to get the BOT_TOKEN. | **Yes** |
| API_KEY | OpenAI or third-party API key. | **Yes** |
| MODEL | Set the default QA model; the default is:`gpt-5`. This item can be freely switched using the bot's "info" command, and it doesn't need to be set in principle. | No |
| WEB_HOOK | Whenever the telegram bot receives a user message, the message will be passed to WEB_HOOK, where the bot will listen to it and process the received messages in a timely manner. | No |
| BASE_URL | If you are using the OpenAI official API, you don't need to set this. If you using a third-party API, you need to fill in the third-party proxy website. The default is: https://api.openai.com/v1/chat/completions | No |
| NICK | The default is empty, and NICK is the name of the bot. The bot will only respond when the message starts with NICK that the user inputs, otherwise the bot will respond to any message. Especially in group chats, if there is no NICK, the bot will reply to all messages. | No |
| GOOGLE_API_KEY | If you need to use Google search, you need to set it. If you do not set this environment variable, the bot will default to provide duckduckgo search. | No |
| GOOGLE_CSE_ID | If you need to use Google search, you need to set it together with GOOGLE_API_KEY. | No |
| whitelist | Set which users can access the bot, and connect the user IDs authorized to use the bot with ','. The default value is `None`, which means that the bot is open to everyone. | No |
| BLACK_LIST | Set which users are prohibited from accessing the bot, and connect the user IDs authorized to use the bot with ','. The default value is `None` | No |
| ADMIN_LIST | Set up an admin list. Only admins can use the `/info` command to configure the bot. | No |
| GROUP_LIST | Set up a list of groups that can use the bot. Connect the group IDs with a comma (','). Even if group members are not on the whitelist, as long as the group ID is in the GROUP_LIST, all members of the group can use the bot. | No |
| CUSTOM_MODELS | Set a list of custom model names. Use commas (',') to connect model names. If you need to remove a default model, add a hyphen (-) before the default model name. To remove all default models, use `-all`. To create model groups, use semicolons (';') to separate groups and use colon (':') to define group name with its models, e.g., `CUSTOM_MODELS=-all,command,grok-2;GPT:gpt-5,gpt-3.5-turbo;Claude:claude-3-opus,claude-3-sonnet;OTHERS`. Models without specific groups will be automatically placed in the "OTHERS" group. | No |
| CHAT_MODE | Introduce multi-user mode, different users' configurations are not shared. When CHAT_MODE is `global`, all users share the configuration. When CHAT_MODE is `multiusers`, user configurations are independent of each other. | No |
| temperature | Specify the temperature of the LLM. The default value is `0.5`. | No |
| GET_MODELS | Specify whether to get supported models via API. Default is `False`. | No |
| SYSTEMPROMPT | Specify system prompt, the system prompt is a string, for example: `SYSTEMPROMPT=You are ChatGPT, a large language model trained by OpenAI. Respond conversationally`. The default is `None`. The setting of the system prompt is only effective when `CHAT_MODE` is `global`. When `CHAT_MODE` is `multiusers`, the system prompt environment variable will not modify any user's system prompt regardless of its value, because users do not want their set system to be changed to a global system prompt. | No |
| LANGUAGE | Specifies the default language displayed by the bot, including button display language and dialogue language. The default is `English`. Currently, it only supports setting to the following four languages: `English`, `Simplified Chinese`, `Traditional Chinese`, `Russian`. You can also use the `/info` command to set the display language after the bot is deployed. | No |
| CONFIG_DIR | Specify storage user profile folder. CONFIG_DIR is the folder for storing user configurations. Each time the bot starts, it reads the configurations from the CONFIG_DIR folder, so users won't lose their previous settings every time they restart. you can achieve configuration persistence by mounting folders using the `-v` parameter when deploying locally with Docker. Default is `user_configs`. | No |
| RESET_TIME | Specifies how many seconds the bot resets the chat history. Every RESET_TIME seconds, the bot will reset the chat history for all users except the admin list. The reset time for each user is different, calculated based on the last question time of each user to determine the next reset time. It is not all users resetting at the same time. The default value is `3600` seconds, and the minimum value is `60` seconds. | No |

The following is a list of environment variables related to robot preferences. Preferences can also be set after the robot is started by using the `/info` command and clicking the `Preferences` button:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| PASS_HISTORY | The default value is `9999`. The bot will remember the conversation history and consider the context in the next reply. If set to `0`, the bot will forget the conversation history and only consider the current conversation. The value of PASS_HISTORY must be greater than or equal to 0. It corresponds to the button named `Chat history` in the preferences. | No |
| LONG_TEXT | If the length of the user's input message exceeds Telegram's limit and multiple messages are sent consecutively in a short period, the bot will treat these multiple messages as one. The default value is `True`. Corresponds to the button named `Long text merge` in the preferences. | No |
| IMAGEQA | Enable image question answering, the default setting is that the model can answer image content, the default value is `True`. Corresponds to the button named `Image Q&A` in the preferences. | No |
| LONG_TEXT_SPLIT | When the bot's reply exceeds Telegram's limit, it will be split into multiple messages. The default value is `True`. Corresponds to the button named `Long text split` in the preferences. | No |
| FILE_UPLOAD_MESS | When a file or image upload is successful and the bot has finished processing, the bot will send a message indicating that the upload was successful. The default value is `True`. This corresponds to the button named `File uploaded message` in the preferences. | No |
| FOLLOW_UP | Automatically generate multiple related questions for the user to choose from. The default value is `False`. Corresponds to the button named `Question suggestions` in the preferences. | No |
| TITLE | Whether to display the model name at the beginning of the robot's reply. The default value is `False`. Corresponds to the button named `Model title` in the preferences. | No |
| REPLY | Should the robot reply to the user's message in the "reply" format. The default value is `False`. Corresponds to the button named `Reply message` in the preferences. | No |
<!-- | TYPING | Whether to show "typing" status when the bot is replying. The default value is `False`. | No | -->
The following is a list of environment variables related to the bot's plugin settings:

| Variable Name | Description | Required? |
|---------------|-------------|-----------|
| get_search_results | Whether to enable the search plugin. Default is `False`. | No |
| get_url_content | Whether to enable the URL summarization plugin. Default is `False`. | No |
| download_read_arxiv_pdf | Whether to enable the arXiv paper summarization plugin. Default is `False`. | No |
| run_python_script | Whether to enable the code interpreter plugin. Default is `False`. | No |
| generate_image | Whether to enable the image generation plugin. Default is `False`. | No |
| get_time | Whether to enable the date plugin. Default is `False`. | No |


## Koyeb Remote Deployment

There are two ways to deploy on Koyeb, one is to use the one-click deployment with the Docker image provided by Koyeb, and the other is to import this repository for deployment. Both methods are free. The first method is simple to deploy but cannot update automatically, while the second method is slightly more complex but can update automatically.

### One-click deployment

Click the button below to automatically deploy using the pre-built Docker image with one click:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=chatgpt&type=docker&image=docker.io%2Fyym68686%2Fchatgpt%3Alatest&instance_type=free&regions=was&instances_min=0&autoscaling_sleep_idle_delay=300&env%5BAPI%5D=&env%5BBASE_URL%5D=&env%5BBOT_TOKEN%5D=&env%5BWEB_HOOK%5D=https%3A%2F%2F%7B%7B+KOYEB_PUBLIC_DOMAIN+%7D%7D%2F)

In the environment variables, fill in BOT_TOKEN, API, BASE_URL, and click the deploy button. WEB_HOOK environment variable can be left as is, and Koyeb will automatically assign a subdomain.

### Repository deployment

1. Fork this repository [Click to fork this repository](https://github.com/yym68686/ChatGPT-Telegram-Bot/fork)

2. When deploying, you need to choose the repository method, set `Run command` to `python3 bot.py`, and set `Exposed ports` to `8080`.

3. [Install pull](https://github.com/apps/pull) to automatically sync this repository.

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
    -e BASE_URL= \
    -v ./user_configs:/home/user_configs \
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
      - BASE_URL=
      - CUSTOM_MODELS=-all;GPT:gpt-5,gpt-3.5-turbo;Claude:claude-3-opus,claude-3-sonnet
    volumes:
      - ./user_configs:/home/user_configs
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
-e BASE_URL= \
-e GOOGLE_API_KEY= \
-e GOOGLE_CSE_ID= \
-e claude_api_key= \
-v ./user_configs:/home/user_configs \
yym68686/chatgpt:latest
docker logs -f chatbot
```

This script is for restarting the Docker image with a single command. It first removes the existing Docker container named "chatbot" if it exists. Then, it runs a new Docker container with the name "chatbot", exposing port 8080 and setting various environment variables. The Docker image used is "yym68686/chatgpt:latest". Finally, it follows the logs of the "chatbot" container.

## 🚀 Source code Local Deployment

python >= 3.10

Run the robot directly from the source code without using docker, Clone the repository:

```bash
git clone --recurse-submodules --depth 1 -b main --quiet https://github.com/yym68686/ChatGPT-Telegram-Bot.git
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Configure Environment Variables:

```bash
./configure_env.sh
```

Run:

```bash
python bot.py
```

## 🧩 Plugin

This project supports multiple plugins, including: DuckDuckGo and Google search, URL summary, ArXiv paper summary, DALLE-3 drawing, and code interpreter, etc. You can enable or disable these plugins by setting environment variables.

- How to develop a plugin?

All the code related to plugins is in the git submodule aient within this repository. aient is an independent repository that I developed to handle API requests, conversation history management, and other functions. When you clone this repository using the `--recurse-submodules` parameter with git clone, aient will be automatically downloaded to your local machine. All the plugin code in this repository is located at the relative path `aient/src/aient/plugins`. You can add your own plugin code in this directory. The plugin development process is as follows:

1. Create a new Python file in the `aient/src/aient/plugins` directory, for example, `myplugin.py`. Register the plugin by adding the `@register_tool()` decorator above your function. Import `register_tool` via `from .registry import register_tool`.

2. Add translations for the plugin name in various languages in the utils/i18n.py file.

After completing the above steps, your plugin is ready to use. 🎉

## 📄 Frequently Asked Questions

- What is the use of the WEB_HOOK environment variable? How should it be used?

WEB_HOOK is a webhook address. Specifically, when a Telegram bot receives a user message, it sends the message to the Telegram server, which then forwards the message to the server at the WEB_HOOK address set by the bot. Therefore, when a message is sent to the bot, the bot executes the processing program almost immediately. Receiving messages via WEB_HOOK results in faster response times than when WEB_HOOK is not set.

When deploying a bot using platforms like Zeabur, Replit, or Koyeb, these platforms provide you with a domain name that you need to fill in the WEB_HOOK, so the bot can receive user messages. Of course, not setting WEB_HOOK is also possible, but the bot's response time will be slightly longer, although the difference is not significant, so generally setting WEB_HOOK is not necessary.

When deploying a bot on a server, you need to use reverse proxy tools like nginx or caddy to forward messages sent by the Telegram server to your server, so the bot can receive user messages. Therefore, you need to set WEB_HOOK to your server's domain name and forward the traffic requesting WEB_HOOK to the server and corresponding port where the bot is located. For example, in caddy, you can configure it like this in the caddy configuration file /etc/caddy/Caddyfile:

```caddy
your_webhook_domain.com {
    reverse_proxy localhost:8082
}
```

- Why can't I use Google search?

By default, DuckDuckGo search is provided. The official API for Google search needs to be applied for by the user. It can provide real-time information that GPT could not answer before, such as today's trending topics on Weibo, today's weather in a specific location, and the progress of a certain person or news event.

- Why can't I use the search function even though I added the Google search API?

There are two possibilities:

1. Only large language model (LLM) APIs that support tool usage can use the search function. Currently, this project only supports the search function for APIs of the OpenAI, Claude, and Gemini series models. APIs from other model providers are not supported for tool usage in this project at the moment. If you have a model provider you wish to adapt, you can contact the maintainer.

2. If you are using the APIs of OpenAI, Claude, and Gemini series models but cannot use the search function, it may be because the search function is not enabled. You can check whether the search function is enabled by clicking on preferences through the `/info` command.

3. If you are using the API of OpenAI, Claude, and Gemini series models, please ensure you are using the official API. If you are using a third-party relay API, the provider may be offering you the API through web scraping. APIs provided through web scraping cannot use tools use, meaning that all plugins of this project cannot be used. If you confirm that you are using the official API and still cannot search successfully, please contact the developer.

- How do I switch models?

You can switch between GPT3.5/4/4o, and other models using the "/info" command in the chat window.

- Can it be deployed in a group?

Yes, it supports whitelist to prevent abuse and information leakage.

- Why can't the bot talk when I add it to the group?

If this is the first time you add the bot to a group chat, you need to set the group privacy to disable in botfather, then remove the bot from the group chat and re-add it to use it normally.

The second method is to set the bot as an administrator, so the bot can be used normally. However, if you want to add the bot to a group chat where you are not an administrator, the first method is more suitable.

Another possibility is that the GROUP_LIST set is not the current group chat ID. Please check if GROUP_LIST is set; GROUP_LIST is the group ID, not the group name. The group ID starts with a minus sign followed by a string of numbers.

- How do the settings of GROUP_LIST, ADMIN_LIST, and whitelist affect the behavior of the bot?

If whitelist is not set, everyone can use the bot. If whitelist is set, only users in the whitelist can use the bot. If GROUP_LIST is set, only groups in the GROUP_LIST can use the bot. If both whitelist and GROUP_LIST are set, everyone in the group can use the bot, but only users in the whitelist can privately chat with the bot. If ADMIN_LIST is set, only users in the ADMIN_LIST can use the /info command to change the bot's settings. If ADMIN_LIST is not set, everyone can use the /info command to change the bot's configuration. GROUP_LIST can also contain channels, channel IDs start with a minus sign followed by a string of numbers.

- How should I set the BASE_URL?

The BASE_URL supports all suffixes, including: https://api.openai.com/v1/chat/completions, https://api.openai.com/v1, and https://api.openai.com/. The bot will automatically allocate different endpoints based on different uses.

- Is it necessary to configure the web_hook environment variable?

The web_hook is not a mandatory environment variable. You only need to set the domain name (which must be consistent with WEB_HOOK) and other environment variables as required for your application's functionality.

- I deployed a robot with docker compose. If the documentation is placed on the server locally, which directory should it be mounted to in order to take effect? Do I need to set additional configurations and modify the code?

You can directly send the documentation to the robot through the chat box, and the robot will automatically parse the documentation. To use the documentation dialogue function, you need to enable the historical conversation feature. There is no need for additional processing of the documentation.

- I still can't get it to work... I want to use it in a group, I've set the ADMIN_LIST to myself, and the GROUP_LIST to that group, with the whitelist left empty. However, only I can use it in that group, other members in the group are prompted with no permission, what's going on?

Here's a troubleshooting guide: Please carefully check if the GROUP_LIST is correct. The ID of a Telegram group starts with a negative sign followed by a series of numbers. If it's not, please use this bot [bot](https://t.me/getidsbot) to reacquire the group ID.

- I've uploaded a document, but it's not responding based on the content of the document. What's going on?

To use the document question and answer feature, you must first enable the history record. You can turn on the history record through the `/info` command, or by setting the environment variable `PASS_HISTORY` to be greater than to 2 to enable the history record by default. Please note that enabling the history record will incur additional costs, so this project does not enable the history record by default. This means that the question and answer feature cannot be used under the default settings. Before using this feature, you need to manually enable the history record.

- After setting the `NICK`, there's no response when I @ the bot, and it only replies when the message starts with the nick. How can I make it respond to both the nick and @botname?

In a group chat scenario, if the environment variable `NICK` is not set, the bot will receive all group messages and respond to all of them. Therefore, it is necessary to set `NICK`. After setting `NICK`, the bot will only respond to messages that start with `NICK`. So, if you want to @ the bot to get a response, you just need to set NICK to @botname. This way, when you @ the bot in the group, the bot will detect that the message starts with @botname, and it will respond to the message.

- How many messages will the history keep?

All other models use the official context length settings, for example, the `gpt-3.5-turbo-16k` context is 16k, the `gpt-5` context is 128k, and the `Claude3/3.5` context is 200k. This limitation is implemented to save user costs, as most scenarios do not require a high context.

- How to delete the default model name from the model list?

You can use the `CUSTOM_MODELS` environment variable to complete it. For example, if you want to add gpt-5 and remove the gpt-3.5 model from the model list, please set `CUSTOM_MODELS` to `gpt-5,-gpt-3.5`. If you want to delete all default models at once, you can set `CUSTOM_MODELS` to `-all,gpt-5`.

- How do I organize models into groups?

You can use the `CUSTOM_MODELS` environment variable with a special syntax:
1. Use semicolons (`;`) to separate groups
2. Use a colon (`:`) to define a group name and its models
3. List models within a group separated by commas (`,`)

For example:
```
CUSTOM_MODELS=-all;GPT:gpt-5,gpt-4,gpt-3.5-turbo;Claude:claude-3-opus,claude-3-sonnet,claude-3-haiku;Gemini:gemini-1.5-pro,gemini-1.0-pro;command,grok-2
```

This creates three groups: "GPT", "Claude", and "Gemini", each containing their respective models. The models "command" and "grok-2" have no explicit group, so they'll automatically be placed in the "OTHERS" group.

To include an empty "OTHERS" group even if there are no ungrouped models, add "OTHERS" at the end:
```
CUSTOM_MODELS=-all;GPT:gpt-5;Claude:claude-3-opus;OTHERS
```

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

- What is the appropriate value for PASS_HISTORY?

The number of PASS_HISTORY is strictly equal to the number of messages in the conversation history. The recommended value is 2, because the system prompt occupies one message count. If set to 0, PASS_HISTORY will automatically reset to 2 to ensure the conversation proceeds normally. When PASS_HISTORY is less than or equal to 2, the bot's behavior can be regarded as only remembering the current conversation, i.e., one question and one answer, and it will not remember the content of the previous Q&A next time. There is no limit to the maximum value of PASS_HISTORY, but please note that the more messages in the conversation history, the higher the cost of each conversation will be. When PASS_HISTORY is not set, the default value is 9999, indicating that the number of messages in the conversation history is 9999.

- Can Bot tokens have multiple tokens?

No, in the future it will support multiple Bot Tokens.

- How to use robot commands?

1. `/info`: The robot `/info` command can view the robot's configuration information, including the current model in use, API URL, API key, etc. It can also change the robot's display language, preferences, and plugin settings.

2. `/start`: The robot `/start` command can view the robot's usage instructions, usage methods, and function introduction. You can set the API key using the `/start` command. If you have an official OpenAI API key, please use the following command: `/start your_api_key`. If you are using a third-party API key, please use the following command: `/start https://your_api_url your_api_key`.

3. `/reset`: The robot `/reset` command can clear the robot's conversation messages and force the robot to stop generating replies. If you want to reset the system prompt, please use the following command: `/reset your_system_prompt`. However, the `/reset` command will never restore the robot's display language, preferences, plugin settings, model in use, API URL, API key, system prompt, etc.

4. `/model`: The robot `/model` command allows you to quickly switch between AI models without going through the `/info` menu. Simply use `/model model_name` to switch to a specific model. For example: `/model gpt-5` to switch to GPT-5 or `/model claude-3-opus` to switch to Claude 3 Opus. This command provides a faster way to change models during conversations.

- What to do if Koyeb deployment fails?

Koyeb's free service can be a bit unstable, so deployment failures are pretty common. You might want to try redeploying, and if that doesn't work, consider switching to another platform. 😊

- Why does the default model name reappear after I use CUSTOM_MODELS to delete it, and then check again with the /info command?

If you deployed using `docker-compose.yml`, do not add quotes around the value of `CUSTOM_MODELS`. Incorrect usage: `CUSTOM_MODELS="gpt-5,-gpt-3.5"`, otherwise it will cause environment variable parsing errors, resulting in the default model name reappearing. The incorrect way will be parsed as deleting the `gpt-3.5"` model, which will cause the default model name `gpt-3.5` not to be deleted. The correct way to write it is: `CUSTOM_MODELS=gpt-5,-gpt-3.5`.

The same applies to model groups. Incorrect: `CUSTOM_MODELS="GPT:gpt-5;Claude:claude-3-opus"`. Correct: `CUSTOM_MODELS=GPT:gpt-5;Claude:claude-3-opus`. If your group names or model names contain special characters, be careful with escaping.

- How can I use multiple API providers at the same time, for example, using both Gemini and OpenAI?

This project can only be configured with one API provider at a time. For example, if the `BASE_URL` is set to Gemini's API endpoint, you cannot use OpenAI's API simultaneously. To use multiple providers at the same time, you must use the `uni-api` project. `uni-api` can convert various API formats from different providers into the standard OpenAI format. Since this project exclusively supports the OpenAI API format, using `uni-api` allows you to use models from dozens of different providers simultaneously. It is important to note that "OpenAI format" does not mean you can only use OpenAI's models; many other providers (like Gemini, Groq, Cloudflare, etc.) also support being called via an OpenAI-compatible API format.

- Why did you change the whole foundation of the api key, now i cant have grok and gemini without changing the api?

The developer deleted APIs other than the OpenAI format. Currently, if you want to use other formats of APIs, you must convert them to the OpenAI format through the developer's other project, uni-api. You can configure dozens of different providers to use in the tg bot at the same time through uni-api. The purpose of this is to reduce maintenance costs, as the developer only needs to maintain uni-api to adapt to all the latest features. Of course, gemini officially supports OpenAI format endpoints, for example: `https://generativelanguage.googleapis.com/v1/chat/completions`.

## References

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

The markdown rendering of the message used is another [project](https://github.com/yym68686/md2tgmd) of mine.

duckduckgo AI: https://github.com/mrgick/duck_chat

## Sponsors

We are grateful for the support from the following sponsors:
<!-- $300+$380+¥1200+¥300+$30+$25+$20+¥50 -->
- @fasizhuanqian: 300 USDT

- @ZETA: $380

- @yuerbujin: ¥1200

- @RR5AM: ¥300

- @IKUNONHK: 30 USDT

- @miya0v0: 30 USDT

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
