# ChatGPT 电报机器人

加入[电报群](https://t.me/+_01cz9tAkUc1YzZl)聊天，分享您的用户体验或报告Bug。

[英语](./README.md) | [简体中文](./README.zh-CN.md) | [繁体中文](./README.zh-TW.md)

## ✨ 特点

✅ 支持ChatGPT和GPT4 API

✅ 支持使用DuckDuckGo和Google进行在线搜索🔍。默认提供DuckDuckGo搜索，用户需申请Google搜索的官方API。可以提供GPT以前无法回答的实时信息，如微博热搜、今天某地的天气和某人或新闻的进展。

✅ 支持基于嵌入式向量数据库的文档问答。在搜索中，对于搜索到的PDF，将执行自动向量语义搜索PDF文档，并基于向量数据库提取与PDF相关的内容。支持使用“qa”命令对整个网站进行向量化，使用“sitemap.xml”文件，然后基于向量数据库回答问题，特别适合一些项目的文档网站和维基网站。

✅ 通过聊天窗口中的“info”命令支持在GPT3.5、GPT4和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持隔离对话，不同用户有不同的对话

✅ 支持消息的精确Markdown渲染，使用我的另一个[项目](https://github.com/yym68686/md2tgmd)

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，防止滥用和信息泄漏

✅ 跨平台，随时随地通过电报打破知识障碍

✅ 支持一键Zeabur，Replit部署，真正的零成本，愚蠢的部署，支持kuma反睡眠。还支持Docker，fly.io部署

## 环境变量

| 变量名                 | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (required)** | 电报机器人令牌。在[BotFather](https://t.me/BotFather)上创建机器人以获取BOT_TOKEN。 |
| **WEB_HOOK (required)**  | 每当电报机器人收到用户消息，消息将传递到WEB_HOOK，机器人将监听消息并及时处理接收到的消息。 |
| **API (required)**       | OpenAI或第三方API密钥。                              |
| API_URL（可选）         | 如果使用OpenAI官方API，则无需设置。如果使用第三方API，则需要填写第三方代理网站。默认值是：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选）      | 设置默认的QA模型；默认是:`gpt-3.5-turbo`。该项目可以使用机器人的“info”命令自由切换，原则上无需设置。 |
| NICK（可选）           | 默认为空，NICK是机器人的名称。只有当用户输入以NICK开头的消息时，机器人才会做出响应，否则机器人将对所有消息做出响应。特别是在群聊中，如果没有NICK，机器人将对所有消息作出响应。 |
| PASS_HISTORY（可选）   | 默认为true。机器人记住对话历史，并在下次回复时考虑上下文。如果设置为false，机器人将忘记对话历史，只考虑当前对话。 |
| GOOGLE_API_KEY（可选） | 如果需要使用Google搜索，需要设置它。如果不设置这个环境变量，机器人将默认提供DuckDuckGo搜索。在Google Cloud的[APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com)中创建凭据，API密钥将是凭据页面上的GOOGLE_API_KEY。Google搜索可以查询100次，对轻度使用完全足够。当使用限额达到时，机器人将自动关闭Google搜索。 |
| GOOGLE_CSE_ID（可选）   | 如果需要使用Google搜索，需要与GOOGLE_API_KEY一起设置。在[Programmable Search Engine](https://programmablesearchengine.google.com/)中创建一个搜索引擎，搜索引擎ID是GOOGLE_CSE_ID的值。 |
| 白名单（可选）         | 设置哪些用户可以访问机器人，并将授权使用机器人的用户ID与“,”连接起来。默认值为“None”，这意味着机器人对所有人开放。 |

## Zeabur 远程部署（推荐）

一键部署：

[![在Zeabur上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果需要后续功能更新，建议使用以下部署方法：

首先克隆此存储库，然后注册[Zeabur](https://zeabur.com)。免费配额对轻度使用足够。从您自己的Github存储库导入，设置域名（必须与WEB_HOOK一致）和环境变量，然后重新部署。如果需要后续的功能更新，只需在您自己的存储库中同步此存储库，并在Zeabur中重新部署以获得最新功能。

## Replit 远程部署

[![在Repl.it上运行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

导入GitHub存储库后，设置运行命令

```bash
pip install -r requirements.txt >