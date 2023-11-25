# ChatGPT 电报机器人

加入[电报群](https://t.me/+_01cz9tAkUc1YzZl)聊天，分享您的用户体验或报告错误。

[英语](./README.md) | [简体中文](./README.zh-CN.md) | [繁体中文](./README.zh-TW.md)

## ✨ 特点

✅ 支持GPT3.5和GPT4/GPT4 Turbo API，DALLE 3

✅ 支持在线搜索，使用duckduckgo和Google进行搜索🔍。默认提供DuckDuckGo搜索，用户需要申请使用Google搜索的官方API。它可以提供GPT之前无法回答的实时信息，例如微博热搜今天，某地今天的天气，以及某人或新闻的进展。

✅ 支持基于嵌入式向量数据库的文档QA。在搜索中，对搜索到的PDF进行自动向量语义搜索，并基于向量数据库提取与PDF相关的内容。支持使用“qa”命令将整个网站向量化，使用“sitemap.xml”文件，并基于向量数据库回答问题，特别适用于文档网站和某些项目的维基网站。

✅ 支持在聊天窗口中通过“info”命令在GPT3.5、GPT4和其他模型之间切换

✅ 异步处理消息，多线程回答问题，支持隔离对话，不同用户有不同的对话

✅ 支持消息的精确Markdown渲染，使用我另一个[项目](https://github.com/yym68686/md2tgmd)

✅ 支持流式输出，实现打字机效果

✅ 支持白名单，防止滥用和信息泄漏

✅ 跨平台，在任何地方随时随地通过电报突破知识壁垒

✅ 支持一键Zeabur、Replit部署，真正的零成本，白痴部署，并支持kuma防睡眠。还支持Docker、fly.io部署

## 环境变量

| 变量名                 | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必填)**   | 电报机器人令牌。在[BotFather](https://t.me/BotFather)上创建一个机器人以获取BOT_TOKEN。 |
| **API (必填)**         | OpenAI或第三方API密钥。                                       |
| WEB_HOOK               | 每当电报机器人接收到用户消息时，消息将传递到WEB_HOOK，机器人将监听消息并及时处理接收到的消息。 |
| API_URL（可选）        | 如果您使用OpenAI官方API，无需设置此项。如果使用第三方API，需要填写第三方代理网站。默认值为：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可选）     | 设置默认的QA模型；默认值为：`gpt-3.5-turbo`。可以使用机器人的“info”命令自由切换此项，原则上不需要设置。 |
| NICK（可选）           | 默认为空，NICK是机器人的名称。只有当用户输入的消息以NICK开头时，机器人才会回应，否则机器人将回应任何消息。特别是在群聊中，如果没有NICK，机器人将回应所有消息。 |
| PASS_HISTORY（可选）   | 默认为true。机器人会记住对话历史，下次回复时考虑上下文。如果设置为false，机器人将忘记对话历史，只考虑当前对话。 |
| GOOGLE_API_KEY（可选） | 如果需要使用Google搜索，需要设置它。如果不设置此环境变量，机器人将默认提供duckduckgo搜索。在Google Cloud的[APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com)中创建凭据，API密钥将显示在凭据页面上的GOOGLE_API_KEY处。Google搜索每天最多可以查询100次，对于轻度使用完全足够。当达到使用限制时，机器人将自动关闭Google搜索。 |
| GOOGLE_CSE_ID（可选）  | 如果需要使用Google搜索，需要与GOOGLE_API_KEY一起设置它。在[Programmable Search Engine](https://programmablesearchengine.google.com/)中创建搜索引擎，搜索引擎ID是GOOGLE_CSE_ID的值。 |
| 白名单（可选）         | 设置哪些用户可以访问机器人，并将授权使用机器人的用户ID与','连接。默认值为`None`，表示机器人对所有人开放。 |

## Zeabur远程部署（推荐）

一键部署：

[![在Zeabur上部署](https://zeabur.com/deployed-on-zeabur-dark.svg)](https://zeabur.com?referralCode=yym68686&utm_source=yym68686&utm_campaign=oss)
<!-- [![在Zeabur上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686) -->

如果您需要后续的功能更新，建议使用以下部署方法：

首先分叉此存储库，然后注册[Zeabur](https://zeabur.com)。免费额度足以轻度使用。从您自己的Github存储库导入，设置域名（必须与WEB_HOOK一致）和环境变量，并重新部署。如果需要后续的功能更新，只需在自己的存储库中同步此存储库，然后在Zeabur中重新部署以获取最新的功能。

## Replit远程部署

[![在Repl.it上运行](https://replit.com/badge/github